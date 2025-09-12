import keyboard


class ActionMapper:
    def __init__(self):
        self.last_gesture = None # for tracking previous gesture
    
    def perform_action(self, gesture, distance_cm=None):
        """
        Trigger actions based on gesture transitions.
        """
        action = None
        if distance_cm and distance_cm >= 1.5 and distance_cm <= 2.5:
            # if open_hand -> full_grab ---> (select all + copy)
            print("last gesture:", self.last_gesture, "current gesture:", gesture)
            if self.last_gesture == "OPEN HAND" and gesture == "FULL GRAB":
                action = "COPY"
            
            # if full_grab -> open hand ---> paste
            if self.last_gesture == "FULL GRAB" and gesture == "OPEN HAND":
                action = "PASTE"
            
            #  updating state
            if gesture != "UNKNOWN":
                self.last_gesture = gesture
        elif distance_cm and distance_cm > 2.5:
            action = "MOVE CLOSER"
        elif distance_cm and distance_cm < 1.5:
            action = "MOVE FURTHER"
        return action

