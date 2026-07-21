import numpy as np
import cv2 as cv
import mediapipe as mp
import math
import time

class EyeClosureDetector:
    def __init__(self, EAR_THRESHOLD=0.22, EYE_CLOSED_THRESHOLD=1):
        self.EYE_CLOSED_COUNT = 0
        self.EAR_THRESHOLD = EAR_THRESHOLD
        self.EYE_CLOSED_THRESHOLD = EYE_CLOSED_THRESHOLD
        self.START_TIMER = None

    def EAR_calculation(self, face, frame, draw=False):
        h, w, _ = frame.shape

        p1 = face.landmark[33]
        p2 = face.landmark[160]
        p3 = face.landmark[158]
        p4 = face.landmark[133]
        p5 = face.landmark[153]
        p6 = face.landmark[144]

        p1 = (int(p1.x*w), int(p1.y*h))
        p2 = (int(p2.x*w), int(p2.y*h))
        p3 = (int(p3.x*w), int(p3.y*h))
        p4 = (int(p4.x*w), int(p4.y*h))
        p5 = (int(p5.x*w), int(p5.y*h))
        p6 = (int(p6.x*w), int(p6.y*h))

        vertical1 = math.hypot(p2[0]-p6[0], p2[1]-p6[1])
        vertical2 = math.hypot(p3[0]-p5[0], p3[1]-p5[1])
        horizontal = math.hypot(p1[0]-p4[0], p1[1]-p4[1])

        if horizontal != 0:
            EAR = (vertical1 + vertical2) / (2 * horizontal)
        else:
            EAR = 0

        if draw:
            for p in [p1, p2, p3, p4, p5, p6]:
                cv.circle(frame, p, 3, (0, 255, 0), -1)

            cv.line(frame, p2, p6, (255, 0, 0), 2)
            cv.line(frame, p3, p5, (255, 0, 0), 2)
            cv.line(frame, p1, p4, (0, 0, 255), 2)

            cv.putText(frame, f"EAR: {EAR:.2f}",
                       (30, 150),
                       cv.FONT_HERSHEY_SIMPLEX,
                       0.7,
                       (0,255,0),
                       2)

        return EAR < self.EAR_THRESHOLD

    def eye_closure_detection(self, face, frame, draw=False):

        eye_closed = self.EAR_calculation(face, frame, draw)

        if eye_closed:
            if self.START_TIMER is None:
                self.START_TIMER = time.time()
            self.EYE_CLOSED_COUNT += 1
        else:
            self.START_TIMER = None
            self.EYE_CLOSED_COUNT = 0

        if self.EYE_CLOSED_COUNT >= self.EYE_CLOSED_THRESHOLD:
            blink_duration = time.time() - self.START_TIMER
            if draw:
                cv.putText(
                    frame,
                    f"Eyes Closed - Blink Duration: {blink_duration:.2f}s",
                    (30,30),
                    cv.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,0,255),
                    2
            )

            return (True, blink_duration)
        else:
            return (False, 0)



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


eye_closure_detector = EyeClosureDetector(EAR_THRESHOLD=0.22, EYE_CLOSED_THRESHOLD=1)


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

            blink_detected, blink_duration = eye_closure_detector.eye_closure_detection(face, frame, draw=True)
            print(f"Blink Detected: {blink_detected}, Duration: {blink_duration:.2f}s")

    cv.imshow("Drowsiness Detection", frame)
    key = cv.waitKey(1) & 0xFF

    if key == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
