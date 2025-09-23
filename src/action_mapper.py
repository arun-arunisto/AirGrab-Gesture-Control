import asyncio
import sys
import os
import subprocess
import pyperclip
from pynput.keyboard import Controller, Key
from src.sync_portal import send_copy, send_paste


class ActionMapper:
    def __init__(self, server_ip="127.0.0.1", port=8765):
        self.last_gesture = None # for tracking previous gesture
        self.backend = self._detect_backend()
        self.keyboard = Controller()
        self.server_ip = server_ip
        self.port = port
    

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
    
    # ------------------------
    # Clipboard handling
    # ------------------------
    def _get_clipboard(self):
        """Cross-platform clipboard read"""
        platform = sys.platform
        session_type = os.environ.get("XDG_SESSION_TYPE", "").lower()

        try:
            if platform.startswith("win"):
                import win32clipboard

                win32clipboard.OpenClipboard()
                data = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                return data
            elif platform == "darwin":
                return subprocess.check_output("pbpaste").decode()
            elif platform.startswith("linux"):
                if session_type == "wayland":
                    return subprocess.check_output(["wl-paste"]).decode()
                else:
                    return subprocess.check_output(["xclip", "-selection", "clipboard", "-o"]).decode()
        except Exception as e:
            print("Clipboard read failed:", e)
            return ""

    def _set_clipboard(self, text):
        """Cross-platform clipboard write"""
        platform = sys.platform
        session_type = os.environ.get("XDG_SESSION_TYPE", "").lower()

        try:
            if platform.startswith("win"):
                import win32clipboard

                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(text)
                win32clipboard.CloseClipboard()
            elif platform == "darwin":
                subprocess.run("pbcopy", text=True, input=text)
            elif platform.startswith("linux"):
                if session_type == "wayland":
                    subprocess.run(["wl-copy"], input=text.encode())
                else:
                    subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode())
        except Exception as e:
            print("Clipboard write failed:", e)
    
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
                self.select_and_copy()
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
        if self.backend == "pynput":
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
        
        #fetching copied content
        copied_text = self._get_clipboard()
        print("Copied text:",copied_text)

        # send to server
        asyncio.run(send_copy(copied_text, self.server_ip, self.port))
    
    def paste(self):
        # fetch from server
        text = asyncio.run(send_paste(self.server_ip, self.port))
        # puting into clipboard locally
        self._set_clipboard(text)
        if self.backend == "pynput":
            # ctrl + v
            with self.keyboard.pressed(Key.ctrl):
                self.keyboard.press("v")
                self.keyboard.release("v")
        elif self.backend == "ydotool":
            #ctrl + v
            subprocess.run(["ydotool", "key", "ctrl+v"])
        



