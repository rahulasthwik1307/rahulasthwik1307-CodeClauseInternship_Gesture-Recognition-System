# 🖐️ Gesture Control for Hill Climb Racing

## 📌 Overview

This is a real-time hand gesture recognition system that simulates keyboard inputs to control a game (specifically, Hill Climb Racing). Using a webcam, the system detects hand gestures (fist and open palm) and maps them to keyboard arrow keys.

---

## 🚀 Features

* **Real-Time Hand Tracking** using MediaPipe
* **Gesture Recognition** for two hand gestures:

  * **Fist** → Brake (Left Arrow)
  * **Open Hand** → Gas (Right Arrow)
* **Visual Feedback**:

  * Colored gesture banner (Red = Brake, Green = Gas)
  * FPS counter
  * Key state display
  * Instruction overlay
* **Keyboard Emulation** using `ctypes` and a custom `directkeys.py`
* **Compatible with Windows OS**

---

## 🛠️ Tech Stack

* **Language:** Python
* **Computer Vision:** OpenCV
* **Hand Tracking:** MediaPipe
* **Keyboard Emulation:** ctypes (Windows)

---

## 📦 Dependencies

Install the required libraries using pip:

```bash
pip install opencv-python mediapipe numpy
```

> Also ensure your `directkeys.py` is placed in the same folder.

---

## ▶️ How It Works

1. Captures webcam video using OpenCV
2. Uses MediaPipe to track hand landmarks
3. Classifies gestures:

   * 4+ folded fingers = Fist → Brake (Left Arrow)
   * 3+ extended fingers = Open Hand → Gas (Right Arrow)
4. Updates key states only when needed to avoid key spamming
5. Displays FPS, gesture, and key states in real time

---

## 📂 File Structure

```
├── main.py              # Main gesture detection script
├── directkeys.py        # Handles low-level key press simulation
```

---

## 🎮 Use Case: Hill Climb Racing

Control your vehicle using hand gestures:

* **Fist** = Brake (hold hand in fist)
* **Open Hand** = Gas (extend all fingers)
* **Neutral** = No input (hands down or unknown gesture)

---

## 🖥️ Instructions

* Run `main.py`
* Keep your hand visible in front of the webcam
* Use gestures to control gameplay
* Press `q` to quit the application

---

