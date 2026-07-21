import numpy as np
import cv2 as cv
import mediapipe as mp
import math


class YawnDetector():
    def __init__(self, MAR_THRESHOLD=0.5, YAWN_THRESHOLD=10):
        self.YAWN_COUNT = 0
        self.MAR_THRESHOLD = MAR_THRESHOLD
        self.YAWN_THRESHOLD = YAWN_THRESHOLD

    def MAR_calculation(self, face, frame, draw=False):
        h, w, _ = frame.shape

        upper = face.landmark[13]
        lower = face.landmark[14]
        left  = face.landmark[61]
        right = face.landmark[291]

        upper = (int(upper.x*w), int(upper.y*h))
        lower = (int(lower.x*w), int(lower.y*h))
        left  = (int(left.x*w), int(left.y*h))
        right = (int(right.x*w), int(right.y*h))

        vertical = math.hypot(upper[0] - lower[0], upper[1] - lower[1])
        horizontal = math.hypot(left[0] - right[0], left[1] - right[1])
        if horizontal != 0:
            MAR = vertical / horizontal
        else:
            MAR = 0

        if draw is True:
            cv.circle(frame, upper, 3, (0,255,0), -1)
            cv.circle(frame, lower, 3, (0,255,0), -1)
            cv.circle(frame, left, 3, (255,0,0), -1)
            cv.circle(frame, right, 3, (255,0,0), -1)

            cv.line(frame, upper, lower, (0,255,255), 2)
            cv.line(frame, left, right, (0,255,255), 2)

            cv.putText(frame, f"Vertical: {vertical:.2f}", (30,60), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            cv.putText(frame, f"Horizontal: {horizontal:.2f}", (30,90), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            cv.putText(frame, f"MAR: {MAR:.2f}", (30,120), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        

        if MAR > self.MAR_THRESHOLD:
            return True

        return False    

    def yawn_detection(self, face, frame, draw=False):
        yawn_detected = self.MAR_calculation(face, frame, draw)
        print(f"Yawn Detected: {yawn_detected}")
        if yawn_detected:
            self.YAWN_COUNT += 1
        else:
            self.YAWN_COUNT = 0

        if self.YAWN_COUNT >= self.YAWN_THRESHOLD:
            if draw is True:
                cv.putText(frame, "Yawn Detected!", (30,30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            return True
        else:
            return False


mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
drawing = mp.solutions.drawing_utils
cap = cv.VideoCapture(0)


yawn_detector = YawnDetector(MAR_THRESHOLD=0.5, YAWN_THRESHOLD=10)

while True:
    true, frame = cap.read()
    if not true:
        print("Error: Could not read frame from camera.")
        break

    frame = cv.flip(frame, 1)

    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face in results.multi_face_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                face,
                mp_face.FACEMESH_TESSELATION,
                landmark_drawing_spec=drawing.DrawingSpec(
                    color=(0,255,0),
                    thickness=1,
                    circle_radius=1
                ),
                connection_drawing_spec=drawing.DrawingSpec(
                    color=(255,0,0),
                    thickness=1
                )
            )

            yawn_detected = yawn_detector.yawn_detection(face, frame, draw=True)

    
    

    
    cv.imshow("Drowsiness Detection", frame)
    key = cv.waitKey(1) & 0xFF

    if key == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
