# Hand-Control System: Gesture-Based PC Control

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?style=for-the-badge&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.x-red?style=for-the-badge&logo=googles-fuchsia)

---

## Project Overview

The **Hand-Control System** is a **Computer Vision-based Human-Computer Interaction (HCI)** project that utilizes **Machine Learning** to translate hand gestures into operating system control commands. The goal is to provide an alternative, ergonomic, and **hands-free** (contactless) way to manage basic PC functions.

The system tracks hands in real-time via the webcam, identifies the position and state of **21 landmarks** (key reference points) on each hand, and executes system actions based on predefined gestures. 

---

## Objective

To enable contactless interaction with the computer by translating hand movements and positions into system commands (such as increasing/decreasing volume, suspending the device, or controlling screen brightness), thereby promoting an alternative and ergonomic form of control.

---

## Features and Mapped Gestures

The system recognizes and executes the following actions on the Linux operating system:

| Gesture (Single Hand) | Detection Criteria | Executed Function |
| :--- | :--- | :--- |
| **Open Hand** | All five fingers (Thumb, Index, Middle, Ring, Pinky) are raised. | Suspend PC (`systemctl suspend`). |
| **Index Finger** | Only the Index Finger is raised. | Increase Volume. |
| **Middle Finger** | Only the Middle Finger is raised. | Decrease Volume. |
| **Thumb** | Only the Thumb is raised. | Decrease Screen Brightness. |
| **Thumb + Index** | Thumb and Index Finger are raised ("L" sign). | Increase Screen Brightness. |

---

## ⚙️ Technologies

| Category | Technology | Project Use |
| :--- | :--- | :--- |
| **Computer Vision** | **MediaPipe Hands** | ML model for tracking 21 3D hand landmarks. |
| **Image Processing** | **OpenCV (`cv2`)** | Video capture, frame preprocessing (mirroring), and graphical interface display. |
| **Audio Control** | **`pulsectl`** | Low-level interface for controlling PulseAudio volume on Linux. |
| **System Control** | **`os.system` / `brightnessctl`** | Execution of system commands (suspend, control brightness). |
| **Environment** | **Python 3.11+ (pyenv)** | Programming language and version management via Pyenv. |

---

## Installation

This project requires a specific Python environment due to historical incompatibilities of **MediaPipe** with the latest Python versions (such as Python 3.13 on Arch Linux). Using **`pyenv`** to manage the correct Python version is highly recommended.

### Prerequisites

1.  **Install System Dependencies:**
    ```bash
    sudo pacman -S bazel gtk3 # bazel and gtk3 are necessary for compilation/display
    ```
2.  **Install pyenv** 

### 1. Configure the Virtual Environment

Create a new virtual environment using a compatible Python version (3.11 is the most stable for MediaPipe):

```bash
pyenv install 3.11
pyenv virtualenv 3.11 hands_env
pyenv activate hands_env
