import sys
import os
import subprocess
from pynput.keyboard import Controller, Key


class ActionMapper:
    def __init__(self):
        self.last_gesture = None # for tracking previous gesture
        self.backend = self._detect_backend()
        self.keyboard = Controller()
    

    def _detect_backend(self):
        """
        Detect os + display server and return back
        """
        platform = sys.platform
        if platform.startswith("win"):
            return "pynput"
        elif platform == "darwin":
            return "pynput" #macOS
        elif platform.startswith("linux"):
            session_type = os.environ.get("XDG_SESSION_TYPE", "").lower()
            if session_type == "wayland":
                return "ydotool"
            else:
                return "pynput" # assume xorg
        return "pynput" #fallback
    
    def perform_action(self, gesture, distance_cm=None):
        """
        Trigger actions based on gesture transitions.
        """
        print("backend:",self.backend)
        action = None
        if distance_cm and distance_cm >= 1.5 and distance_cm <= 2.5:
            # if open_hand -> full_grab ---> (select all + copy)
            print("last gesture:", self.last_gesture, "current gesture:", gesture)
            if self.last_gesture == "OPEN HAND" and gesture == "FULL GRAB":
                self.select_and_cut()
                action = "SELECT & COPY"
            
            # if full_grab -> open hand ---> paste
            if self.last_gesture == "FULL GRAB" and gesture == "OPEN HAND":
                self.paste()
                action = "PASTE"
            
            #  updating state
            if gesture != "UNKNOWN":
                self.last_gesture = gesture
        elif distance_cm and distance_cm > 2.5:
            action = "MOVE CLOSER"
        elif distance_cm and distance_cm < 1.5:
            action = "MOVE FURTHER"
        return action
    
    # it will select all the content from text editor
    def select_and_copy(self):
        if self.backend == "pynnput":
            # ctrl + A
            with self.keyboard.pressed(Key.ctrl):
                self.keyboard.press("a")
                self.keyboard.release("a")
            
            # ctrl + C
            with self.keyboard.pressed(Key.ctrl):
                self.keyboard.press("c")
                self.keyboard.release("c")
        elif self.backend == "ydotool":
            #ctrl + A
            subprocess.run(["ydotool", "key", "ctrl+a"])
            #ctrl + c
            subprocess.run(["ydotool", "key", "ctrl+c"])
    
    def paste(self):
        if self.backend == "pynput":
            # ctrl + v
            with self.keyboard.pressed(Key.ctrl):
                self.keyboard.press("v")
                self.keyboard.release("v")
        elif self.backend == "ydotool":
            #ctrl + v
            subprocess.run(["ydotool", "key", "ctrl+v"])
        



