#%%
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time

# Upper-body skeleton connections
UPPER_BODY_CONNECTIONS = [
    (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),
    (0, 1), (1, 2), (2, 3), (0, 4), (4, 5), (5, 6), (3, 7), (6, 8)
]

# Init MediaPipe model
base_options = python.BaseOptions(model_asset_path='pose_landmarker.task')
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO
)
detector = vision.PoseLandmarker.create_from_options(options)

# System states
current_step = 0
hold_start_time = None
HOLD_DURATION = 3
accumulated_time = 0

distraction_start_time = None
recovery_message_end_time = 0

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    timestamp_ms = int(time.time() * 1000)
    result = detector.detect_for_video(mp_image, timestamp_ms)

    # Default UI state
    head_status = "Focused"
    head_color = (0, 255, 0)
    warning_text = ""
    is_recovering = False

    if result.pose_landmarks:
        lm = result.pose_landmarks[0]

        # Draw skeleton
        for c in UPPER_BODY_CONNECTIONS:
            p1, p2 = lm[c[0]], lm[c[1]]
            cv2.line(frame,
                     (int(p1.x * w), int(p1.y * h)),
                     (int(p2.x * w), int(p2.y * h)),
                     (255, 255, 255), 2)

        for i in range(17):
            p = lm[i]
            cv2.circle(frame,
                       (int(p.x * w), int(p.y * h)),
                       4, (0, 255, 255), -1)

        # Key points
        nose = lm[0]
        left_ear, right_ear = lm[7], lm[8]

        # Attention detection
        ear_mid_y = (left_ear.y + right_ear.y) / 2
        is_looking_down = nose.y > ear_mid_y + 0.05

        ear_mid_x = (left_ear.x + right_ear.x) / 2
        face_width = abs(left_ear.x - right_ear.x)
        is_looking_aside = abs(nose.x - ear_mid_x) > face_width * 0.3

        is_distracted = is_looking_down or is_looking_aside

        # Attention monitoring
        if current_step >= 0:
            if is_distracted:
                if distraction_start_time is None:
                    distraction_start_time = time.time()

                d = time.time() - distraction_start_time

                if d > 10:
                    current_step = -1
                    distraction_start_time = None
                    hold_start_time = None
                    accumulated_time = 0

                elif d > 5:
                    head_status = f"Distracted {int(d)}s"
                    head_color = (0, 165, 255)
                    warning_text = "Please focus"

                else:
                    head_status = "Glancing"
                    head_color = (0, 255, 255)
                    warning_text = "Paused"
            else:
                # Recovery logic
                if distraction_start_time is not None:
                    if time.time() - distraction_start_time > 5:
                        recovery_message_end_time = time.time() + 2
                    distraction_start_time = None

                if time.time() < recovery_message_end_time:
                    is_recovering = True
                    head_status = "FOCUS RECOVERED"
                    head_color = (0, 255, 0)
                else:
                    head_status = "Focused"
                    head_color = (0, 255, 0)

        # Arm detection
        left_up = lm[15].y < lm[11].y
        right_up = lm[16].y < lm[12].y
        arm_up = left_up or right_up
        arm_down = not left_up and not right_up

        # State machine
        if current_step == -1:
            head_status = "SYSTEM LOCKED"
            head_color = (0, 0, 255)

        elif current_step == 0:
            if arm_up:
                current_step = 1
                hold_start_time = time.time()
                accumulated_time = 0

        elif current_step == 1:
            if arm_up:
                if not is_distracted:
                    now = time.time()
                    accumulated_time += (now - hold_start_time)
                    hold_start_time = now

                    remaining = max(0, HOLD_DURATION - accumulated_time)
                    cv2.putText(frame,
                                f"Processing... {remaining:.1f}s",
                                (50, 160),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.8, (0, 255, 255), 2)
                else:
                    hold_start_time = time.time()
                    cv2.putText(frame,
                                warning_text,
                                (50, 160),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.8, head_color, 3)

                if accumulated_time >= HOLD_DURATION:
                    current_step = 2
            else:
                hold_start_time = time.time()
                accumulated_time = 0

        elif current_step == 2:
            if arm_down:
                current_step = 3

        # Top status bar
        cv2.rectangle(frame, (0, 0), (w, 40), (30, 30, 30), -1)
        cv2.putText(frame,
                    f"Status: {head_status}",
                    (20, 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, head_color, 2)

        # Recovery highlight
        if is_recovering:
            cv2.rectangle(frame, (0, 0), (w, h), (0, 255, 0), 10)

        if current_step == -1:
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 255), -1)
            cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)

            cv2.putText(frame,
                        "FATIGUE DETECTED - TASK STOPPED",
                        (50, 200),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 0, 255), 3)

            cv2.putText(frame,
                        "Press R to restart",
                        (50, 260),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 255, 255), 2)

        else:
            steps = ["1. Raise Tool", "2. Hold Focus", "3. Lower Tool"]

            for i, s in enumerate(steps):
                color = (0, 255, 0) if i < current_step else (100, 100, 100)
                thickness = 2 if i == current_step else 1
                cv2.putText(frame,
                            s,
                            (50, 80 + i * 35),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            color,
                            thickness)

            if current_step == 3:
                cv2.putText(frame,
                            "TASK COMPLETE",
                            (50, 220),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 255, 0), 2)

    cv2.imshow('Industrial XR Task', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

    if key == ord('r'):
        current_step = 0
        accumulated_time = 0
        distraction_start_time = None
        hold_start_time = None
        recovery_message_end_time = 0

cap.release()
cv2.destroyAllWindows()