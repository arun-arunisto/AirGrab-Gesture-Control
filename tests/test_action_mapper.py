from src.gesture_detector import GestureDetector
from src.action_mapper import ActionMapper
import cv2
from src.sync_portal import start_server


detector = GestureDetector()
mapper = ActionMapper()
start_server()

cap = cv2.VideoCapture(0)



last_action = None

while True:
    success, frame = cap.read()
    frame, gesture, distance = detector.detect_gesture(frame=frame)
    print(gesture, distance)
    action = mapper.perform_action(gesture=gesture, distance_cm=distance)
    
    if action:
        last_action = action
    
    if last_action:
        cv2.putText(frame, last_action, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    cv2.imshow("Action Mapper", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()