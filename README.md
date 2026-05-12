# Cognitive Support Prototype

> A lightweight, edge-deployed computer vision prototype designed to simulate context-aware guidance and cognitive support in human-centric manufacturing environments.

##  Overview
In modern manufacturing, intelligent systems must do more than just track task progress—they must adapt to the operator's cognitive state. **Cognitive Support** is a real-time prototype built with Python and Google MediaPipe. It acts as an **intelligent operator interface** that tracks physical assembly/scanning gestures while continuously monitoring the operator's attention and cognitive load. 


### 1. The Ideal Workflow (Focused)
<img width="123" height="123" alt="1" src="https://github.com/user-attachments/assets/3654ccc8-7f34-4130-a1ba-7d9f3017d61d" />


* **Status:** `Focused` (Green)
* **Behavior:** When the operator maintains visual attention on the workspace, the system smoothly tracks the skeletal mechanics, updating the task progress with positive visual reinforcement.

### 2. Grace Period (0 - 5 Seconds)
![Glancing State](2.png)
* **Status:** `Glancing` (Yellow) / `Task Paused`
* **Behavior:** If the operator briefly looks away (e.g., to check a physical manual or grab a different tool), the system tolerates this as a normal action. The task progress is simply **paused** with a non-intrusive yellow indicator, avoiding "alarm fatigue."

### 3. Soft Reminder (5 - 10 Seconds)
![Distracted State](3.png)
* **Status:** `Distracted 6s` (Orange) / `Please focus`
* **Behavior:** If the distraction persists beyond the acceptable grace period, the system escalates to an orange warning. This serves as a **context-aware nudge**, gently reminding the operator to return their attention to the active task zone.

### 4. Hard Lockout & Manual Override (> 10 Seconds)
![Locked State](4.png)
* **Status:** `SYSTEM LOCKED` (Red) / `FATIGUE DETECTED`
* **Behavior:** A critical safety feature for Industry 5.0. If the operator's gaze is diverted for over 10 seconds, the system assumes severe cognitive offloading, fatigue, or an emergency. The UI turns red, the task is completely aborted, and a **Hard Lockout** is triggered. The operator must physically acknowledge the alert by pressing 'R' to restart, ensuring they have regained full situational awareness.

## ✨ Key Features & HCI Principles
*   **Context-Aware Task Workflow:** Uses a state machine to track operator hand mechanics (e.g., raising a scanner/tool) to progress through a standardized task.
*   **Cognitive Attention Monitoring:** Utilizes skeletal and facial landmarks (Pitch and Yaw heuristics) to estimate gaze and head pose in real-time.
*   **Positive Recovery Feedback:** If the operator refocuses during a soft warning, the system provides a 2-second green visual flash to reassure the user that the system state is restored.
*   **Manual Override:** After a Hard Lockout, the system refuses to auto-resume, bridging AI capabilities with rigorous Industrial HCI safety standards.

## 🎥 Demo
[![Watch the Demo](https://img.youtube.com/vi/[YOUR_YOUTUBE_VIDEO_ID]/maxresdefault.jpg)](https://youtu.be/[YOUR_YOUTUBE_VIDEO_ID])
*(Click the image to watch the full interaction demonstration)*

## 🛠️ Technical Stack
*   **Computer Vision:** OpenCV (Rendering & UI simulation)
*   **Edge AI Model:** Google MediaPipe (Pose Landmarker, Tasks API)
*   **Language:** Python 3.10+
*   **Execution:** Real-time processing (No cloud dependency, suitable for Edge Computing deployment)

## 🚀 How to Run
1. Clone the repository:
   ```bash
   git clone [https://github.com/](https://github.com/)[Your-Username]/CogniGuard.git
   cd CogniGuard
