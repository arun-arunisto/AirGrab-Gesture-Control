import cv2
import mediapipe as mp
import math

class GestureDetector:
    def __init__(self, max_hands=1, detection_confidence=0.7, focal_length=30, known_width=8.0):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(max_num_hands=max_hands, min_detection_confidence=detection_confidence)
        self.focal_length = focal_length
        self.known_width = known_width
    
    def _pixel_distance(self, a, b, img_w, img_h):
        """
        Convert normalized coords to pixel distance.
        """
        x1, y1 = int(a.x * img_w), int(a.y * img_h)
        x2, y2 = int(b.x * img_w), int(b.y * img_h)
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def _distance(self, a, b):
        """
        Calculate Euclidean distance between two landmarks
        """
        return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)
    
    def detect_gesture(self, frame):
        """
        Process frame and return gesture status.
        """
        h, w, _ = frame.shape
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        gesture, distance_cm = None, None
        if results.multi_hand_landmarks:
            for handlms in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, handlms, self.mp_hands.HAND_CONNECTIONS)

                # palm width = distance between index base and pinky base
                perceived_width = self._pixel_distance(handlms.landmark[5], handlms.landmark[17], w, h)
                
                distance_cm = (self.known_width*self.focal_length)/perceived_width
                # print(distance_cm)
                tips = [8, 12, 16, 20] # index, Middle, Ring, Pinky tips
                bases = [5, 9, 13, 17] # base joints

                distances = [self._distance(handlms.landmark[tip], handlms.landmark[base])for tip, base in zip(tips, bases)]
                # print(distances)
                # conditions to check if its a full grab or open hand
                if all(d < 0.08 for d in distances):
                    gesture = "FULL GRAB"
                elif all(d > 0.2 for d in distances):
                    gesture = "OPEN HAND"
                else:
                    gesture = "UNKNOWN"
        return frame, gesture, distance_cm
    
