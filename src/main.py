import argparse
from .sync_portal import start_server
from .action_mapper import ActionMapper
from .gesture_detector import GestureDetector
import cv2

class Main:
    def __init__(self):
        self.detector = GestureDetector()
        self.cap = cv2.VideoCapture(0)
    
    def run_server(self, host: str, port: int):
        """
        starting the sync portal
        """
        print(f"[SYNC PORTAL] Server running on ws://{host}:{port}")
        mapper = ActionMapper(host, port)
        start_server(host, port)
        last_action = None

        while True:
            success, frame = self.cap.read()
            frame, gesture, distance = self.detector.detect_gesture(frame=frame)
            print(f"[ACTION & DISTANCE] {gesture} {distance}")
            action = mapper.perform_action(gesture=gesture, distance_cm=distance)

            if action:
                last_action = action
            
            if last_action:
                cv2.putText(frame, last_action, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            cv2.imshow("Action Mapper", frame)
            if cv2.waitKey(1) == ord("q"):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()
    
    def run_client(self, server_ip:str, port: int):
        """
        Starting the client
        """
        print(f"[SYNC PORTAL] Client connected to ws://{server_ip}:{port}")
        mapper = ActionMapper(server_ip=server_ip, port=port)
        last_action = None
        while True:
            success, frame = self.cap.read()
            frame, gesture, distance = self.detector.detect_gesture(frame=frame)
            print(f"[ACTION & DISTANCE] {gesture} {distance}")
            action = mapper.perform_action(gesture=gesture, distance_cm=distance)
            print(f"[ACTION & DISTANCE] {gesture} {distance}")
            if action:
                last_action = action
            
            if last_action:
                cv2.putText(frame, last_action, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            cv2.imshow("Action Mapper", frame)
            if cv2.waitKey(1) == ord("q"):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync portal Runner")
    parser.add_argument("mode", choices=["server", "client"], help="Run as server or client")
    parser.add_argument("--host", default="0.0.0.0", help="Server host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8765, help="Port (default: 8765)")
    parser.add_argument("--server-ip", default="127.0.0.1", help="Server IP for client mode")

    args = parser.parse_args()
    program = Main()
    if args.mode == "server":
        program.run_server(args.host, args.port)
    else:
        program.run_client(args.server_ip, args.port)
    
