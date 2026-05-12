# Pose Estimation for Operator Action Monitoring

A real-time pose estimation prototype using MediaPipe, exploring how 
operator actions and task workflows can be monitored in industrial environments.

## What it does
- Detects 33 body landmarks in real time using a webcam
- Tracks a multi-step workflow with timing requirements:
  - Step 1: Raise arm
  - Step 2: Hold position for 3 seconds
  - Step 3: Lower arm
- Visual progress indicator shows completed and remaining steps
- Press R to restart the workflow, Q to quit

## How to run
pip install mediapipe opencv-python

Download the pose landmarker model:
https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task

Save it as pose_landmarker.task in the same folder, then run:
pose_detection.py
<img width="344" height="477" alt="68724f349029621b5e0a733b2e049af4" src="https://github.com/user-attachments/assets/21d2dfc1-153e-41cf-9b77-40117ef43173" />


## Relevance
This prototype demonstrates a foundation for context-aware operator 
monitoring in human-centric manufacturing. Understanding task progress 
and body posture in real time is a core requirement for AI-driven 
assistance systems in Industry 5.0 environments.

## Acknowledgements
Pose estimation model from [MediaPipe](https://github.com/google-ai-edge/mediapipe) by Google.
