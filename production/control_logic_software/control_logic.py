class Control_logic():
    def __init__(self):
        pass
    def response(self, yawn_detected, eyes_closed, blink_rate):
        if eyes_closed and blink_rate > 4:
            return 1
        elif eyes_closed and blink_rate > 1.5:
            return 2
        elif yawn_detected:
            return 3
        
        return 0