#%%
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time

base_options = python.BaseOptions(model_asset_path='pose_landmarker.task')
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE
)
detector = vision.PoseLandmarker.create_from_options(options)

current_step = 0
hold_start_time = None  # Record the time when the object comes to a stop
HOLD_DURATION = 3       # Pause for 3 seconds

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = detector.detect(mp_image)

    if result.pose_landmarks:
        lm = result.pose_landmarks[0]

        for landmark in lm:
            h, w, _ = frame.shape
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

        arm_up = lm[15].y < lm[11].y    # Wrist higher than shoulder
        arm_down = lm[15].y > lm[11].y  # Wrist lower than shoulder

        # Step 1: Raise the arm
        if current_step == 0:
            if arm_up:
                current_step = 1
                hold_start_time = time.time()

        # Step 2: Hold for 3 seconds
        elif current_step == 1:
            if arm_up:
                elapsed = time.time() - hold_start_time
                remaining = HOLD_DURATION - elapsed
                cv2.putText(frame, f"Hold... {remaining:.1f}s",
                            (50, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                if elapsed >= HOLD_DURATION:
                    current_step = 2
            else:
                # If the person put hand down and restarted the timer
                hold_start_time = time.time()

        # Step 3: Lower the arms
        elif current_step == 2:
            if arm_down:
                current_step = 3

        # 显示步骤进度
        steps = ["1. Raise arm", "2. Hold 3s", "3. Lower arm"]
        for i, name in enumerate(steps):
            color = (0, 255, 0) if i < current_step else (100, 100, 100)
            cv2.putText(frame, name, (50, 80 + i*40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        if current_step == 3:
            cv2.putText(frame, "Complete!", (50, 220),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Pose Detection', frame)
    if current_step == 3:
            cv2.putText(frame, "", (50, 220),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "Press R to restart", (50, 270),  # ← 加这行提示
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.imshow('Pose Detection', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('r'):
        current_step = 0
        hold_start_time = None

cap.release()
cv2.destroyAllWindows()
