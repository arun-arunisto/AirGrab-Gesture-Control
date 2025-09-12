### 📌 **Project: AirGrab Gesture Control**

A Python-based **gesture recognition system** to perform copy-paste actions and remote clipboard sync between Windows and Ubuntu using **MediaPipe**, **OpenCV**, and **Sockets**.

---

### ✅ **Project Roadmap**

#### **Phase 1: Gesture Detection & Distance**

* [ ] Setup Python virtual environment.
* [ ] Install dependencies (`opencv-python`, `mediapipe`, `pyautogui`, `pyperclip`).
* [ ] Implement **Open Hand detection**.
* [ ] Implement **Full Grab (Fist) detection**.
* [ ] Display gesture feedback on screen.
* [ ] Calculate the distance b/w screen and hand
* [ ] Implement **Move Closer** or **Move Further**
* [ ] Display distance log on screen.

### Phase 2: Action Mapping

* [ ] Define gesture → action transitions (copy & paste).
* [ ] Implement **cross-platform action mapper**:

  * Detect OS (`sys.platform`).
  * On Linux, detect display server (`XDG_SESSION_TYPE` = `"x11"` or `"wayland"`).
  * Pick backend:

    * Windows → `pynput`
    * Linux + Xorg → `pynput`
    * Linux + Wayland → `ydotool`
    * macOS → `pynput`
* [ ] Map gestures:

  * OPEN → GRAB → **COPY (Ctrl+A, Ctrl+C)**
  * GRAB → OPEN → **PASTE (Ctrl+V)**
* [ ] Add testing stubs in `tests/test_action_mapper.py`.
* [ ] Map **Grab → Copy**, **Open Hand → Paste** using `pyautogui`.
* [ ] Test on **Windows** and **Ubuntu**.

#### **Phase 3: Remote Clipboard Sync**

* [ ] Build **Socket Server** (Ubuntu) and **Client** (Windows).
* [ ] Send copied text from Windows → Ubuntu.
* [ ] Auto-paste into **Gedit** or **Notepad**.

#### **Phase 4: GUI & Settings**

* [ ] Create **Start/Stop detection** GUI (Tkinter or PyQt).
* [ ] Add **IP configuration field** for remote sync.
* [ ] Add status indicators (Connected / Disconnected).

#### **Phase 5: Packaging & Deployment**

* [ ] Create `requirements.txt`.
* [ ] Add **setup.py** for easy installation.
* [ ] Add **screenshots** and **usage guide** to `README.md`.
* [ ] Push code to **GitHub repository**.

#### **Phase 6: Advanced Features**

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
│   ├── clipboard_sync.py      # Handles socket communication
│   └── utils.py               # Helper functions
├── assets/
│   └── screenshots/           # UI previews
├── tests/
    └── test_gesture.py

```

---
