import cv2 as cv
import mediapipe as mp

from detectors.eye_closure import EyeClosureDetector
from detectors.yawn import YawnDetector
print("a")
from communication.sender import Sender

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


ESP_32_IP = "192.168.4.1"
PORT = 5000
print("a")
sender = Sender(ESP_32_IP, PORT)
print("b")
try:
    print("ac")
    sender.connect()
    print("d")
    print("Connected to ESP32")
    print("e")
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

                message = f"Eyes Closed: {eyes_closed} | Duration: {blink_duration:.2f}s | Yawn: {yawn_detected}" + "\n"
                print(message)

                sender.send(message)
                response = sender.response()
                print(f"Response from ESP32: {response}")
                

        cv.imshow("Drowsiness Detection", frame)

        key = cv.waitKey(1) & 0xFF

        if key == ord('q'):
            break
except Exception as e:
    print(f"An error occurred: \n{e}")

finally:
    sender.close()
    print("Connection closed")
    cap.release()
    cv.destroyAllWindows()

