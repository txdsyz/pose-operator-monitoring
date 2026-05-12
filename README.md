# Pose Estimation for Operator Action Monitoring

A real-time pose estimation prototype using MediaPipe, 
exploring how operator actions can be detected and classified 
in industrial environments.

## What it does
- Detects 33 body landmarks in real time using a webcam
- Classifies basic actions (e.g. arm raised, upright vs bending)
- Demonstrates a foundation for context-aware operator monitoring

## How to run
pip install mediapipe opencv-python

Download the model file and run pose_detection.py

## Relevance
This prototype relates to operator action analysis in 
human-centric manufacturing, where understanding task 
context and body posture can support AI-driven assistance systems.

## Acknowledgements
Pose estimation model from [MediaPipe](https://github.com/google-ai-edge/mediapipe) by Google.
