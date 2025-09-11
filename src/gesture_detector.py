import cv2
import mediapipe as mp
import math

class GestureDetector:
    def __init__(self, max_hands=1, detection_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(max_num_hands=max_hands, min_detection_confidence=detection_confidence)
    
    def _distance(self, a, b):
        """
        Calculate Euclidean distance between two landmarks
        """
        return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)
    
    def detect_gesture(self, frame):
        """
        Process frame and return gesture status.
        """
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        gesture = None
        if results.multi_hand_landmarks:
            for handlms in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, handlms, self.mp_hands.HAND_CONNECTIONS)

                tips = [8, 12, 16, 20] # index, Middle, Ring, Pinky tips
                bases = [5, 9, 13, 17] # base joints

                distances = [self._distance(handlms.landmark[tip], handlms.landmark[base])for tip, base in zip(tips, bases)]
                print(distances)
                # conditions to check if its a full grab or open hand
                if all(d < 0.08 for d in distances):
                    gesture = "FULL GRAB"
                elif all(d > 0.2 for d in distances):
                    gesture = "OPEN HAND"
                else:
                    gesture = "UNKNOWN"
        return frame, gesture
    
