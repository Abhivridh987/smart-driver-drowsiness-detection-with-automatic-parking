import cv2 as cv
import mediapipe as mp

from detectors.eye_closure import EyeClosureDetector
from detectors.yawn import YawnDetector

mp_face = mp.solutions.face_mesh
drawing = mp.solutions.drawing_utils

face_mesh = mp_face.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv.VideoCapture(0)

eye_closure_detector = EyeClosureDetector(
    EAR_THRESHOLD=0.22,
    EYE_CLOSED_THRESHOLD=1
)

yawn_detector = YawnDetector(
    MAR_THRESHOLD=0.3,
    YAWN_THRESHOLD=10
)

while True:

    success, frame = cap.read()
    if not success:
        print("Error: Could not read frame from camera.")
        break

    frame = cv.flip(frame, 1)
    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face in results.multi_face_landmarks:
            drawing.draw_landmarks(
                frame,
                face,
                mp_face.FACEMESH_TESSELATION,
                landmark_drawing_spec=drawing.DrawingSpec(
                    color=(0, 255, 0),
                    thickness=1,
                    circle_radius=1),
                connection_drawing_spec=drawing.DrawingSpec(
                    color=(255, 0, 0),
                    thickness=1)
            )

            eyes_closed, blink_duration = (
                eye_closure_detector.eye_closure_detection(
                    face,
                    frame,
                    draw=True
                )
            )

            yawn_detected = yawn_detector.yawn_detection(
                face,
                frame,
                draw=True
            )

            print(
                f"Eyes Closed: {eyes_closed} | "
                f"Duration: {blink_duration:.2f}s | "
                f"Yawn: {yawn_detected}"
            )


    # -----------------------------
    # Display
    # -----------------------------

    cv.imshow("Drowsiness Detection", frame)

    key = cv.waitKey(1) & 0xFF

    if key == ord('q'):
        break


# -----------------------------
# Cleanup
# -----------------------------

cap.release()
cv.destroyAllWindows()