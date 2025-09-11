from src.gesture_detector import GestureDetector
import cv2

detector = GestureDetector()

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    frame, gesture = detector.detect_gesture(frame)

    if gesture == "FULL GRAB":
        cv2.putText(frame, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    elif gesture == "OPEN HAND":
        cv2.putText(frame, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    elif gesture == "UNKNOWN":
        cv2.putText(frame, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    
    cv2. imshow("Gesture Detection", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
