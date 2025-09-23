### 📌 **Project: AirGrab Gesture Control**

A Python-based **gesture recognition system** to perform copy-paste actions and remote clipboard sync between Windows and Ubuntu using **MediaPipe**, **OpenCV**, and **Sockets**.

---

### ✅ **Project Roadmap**

#### **Phase 1: Gesture Detection & Distance**

* [X] Setup Python virtual environment.
* [X] Install dependencies (`opencv-python`, `mediapipe`, `pyautogui`, `pyperclip`).
* [X] Implement **Open Hand detection**.
* [X] Implement **Full Grab (Fist) detection**.
* [X] Display gesture feedback on screen.
* [X] Calculate the distance b/w screen and hand
* [X] Implement **Move Closer** or **Move Further**
* [X] Display distance log on screen.

### Phase 2: Action Mapping

* [X] Define gesture → action transitions (copy & paste).
* [X] Implement **cross-platform action mapper**:

  * Detect OS (`sys.platform`).
  * On Linux, detect display server (`XDG_SESSION_TYPE` = `"x11"` or `"wayland"`).
  * Pick backend:

    * Windows → `pynput`
    * Linux + Xorg → `pynput`
    * Linux + Wayland → `ydotool`
    * macOS → `pynput`
* [X] Map gestures:

  * OPEN → GRAB → **COPY (Ctrl+A, Ctrl+C)**
  * GRAB → OPEN → **PASTE (Ctrl+V)**
* [X] Add testing stubs in `tests/test_action_mapper.py`.
* [X] Map **Grab → Copy**, **Open Hand → Paste** using `pyautogui`.
* [X] Test on **Windows** and **Ubuntu**.

#### **Phase 3: Remote Clipboard Sync**

* [X] Build **Socket Server** (Ubuntu) and **Client** (Windows).
* [X] Send copied text from Windows → Ubuntu.
* [X] Auto-paste into **Gedit** or **Notepad**.

#### **Phase 4: Packaging & Deployment**

* [X] Create `requirements.txt`.
* [ ] Add **setup.py** for easy installation.
* [ ] Add **screenshots** and **usage guide** to `README.md`.
* [ ] Push code to **GitHub repository**.

#### **Phase 5: Advanced Features**

* [ ] Add **swipe gestures** for scrolling.
* [ ] Multi-hand support.
* [ ] Optional: **Depth camera integration** (Intel RealSense).
* [ ] Package as a **cross-platform desktop app** using PyInstaller.

---

### ✅ **Tech Stack**

* **Language:** Python (version 3.11.5)
* **Libraries:** MediaPipe, OpenCV, pyautogui, pyperclip
* **Networking:** Python Sockets
* **UI Framework:** Tkinter / PyQt
* **Platform:** Windows & Ubuntu

---

### ✅ **Repository Structure**

```
airgrab-gesture-control/
│
├── README.md
├── requirements.txt
├── src/
│   ├── main.py                # Entry point
│   ├── gesture_detector.py    # Handles MediaPipe detection
│   ├── action_mapper.py       # Maps gestures to actions (copy/paste) 
│   └── sync_portal.py         # Handles socket communication
├── tests/
    ├── test_action_mapper.py  
    ├── test_sync_portal.py              
    └── test_gesture.py

```

---
