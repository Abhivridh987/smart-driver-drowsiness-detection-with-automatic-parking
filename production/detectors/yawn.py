import cv2 as cv
import math
#hello

class YawnDetector:
    def __init__(self, MAR_THRESHOLD=0.3, YAWN_THRESHOLD=10):
        self.YAWN_COUNT = 0
        self.MAR_THRESHOLD = MAR_THRESHOLD
        self.YAWN_THRESHOLD = YAWN_THRESHOLD

    def MAR_calculation(self, face, frame, draw=False):
        h, w, _ = frame.shape

        upper = face.landmark[13]
        lower = face.landmark[14]
        left = face.landmark[61]
        right = face.landmark[291]

        upper = (int(upper.x*w), int(upper.y*h))
        lower = (int(lower.x*w), int(lower.y*h))
        left = (int(left.x*w), int(left.y*h))
        right = (int(right.x*w), int(right.y*h))

        vertical = math.hypot(
            upper[0] - lower[0],
            upper[1] - lower[1]
        )

        horizontal = math.hypot(
            left[0] - right[0],
            left[1] - right[1]
        )

        if horizontal != 0:
            MAR = vertical / horizontal
        else:
            MAR = 0

        if draw:
            cv.circle(frame, upper, 3, (0, 255, 0), -1)
            cv.circle(frame, lower, 3, (0, 255, 0), -1)
            cv.circle(frame, left, 3, (255, 0, 0), -1)
            cv.circle(frame, right, 3, (255, 0, 0), -1)

            cv.line(frame, upper, lower, (0, 255, 255), 2)
            cv.line(frame, left, right, (0, 255, 255), 2)

            cv.putText(
                frame,
                f"Vertical: {vertical:.2f}",
                (30, 60),
                cv.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv.putText(
                frame,
                f"Horizontal: {horizontal:.2f}",
                (30, 90),
                cv.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv.putText(
                frame,
                f"MAR: {MAR:.2f}",
                (30, 120),
                cv.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        return MAR > self.MAR_THRESHOLD

    def yawn_detection(self, face, frame, draw=False):

        mouth_open = self.MAR_calculation(
            face,
            frame,
            draw
        )

        if mouth_open:
            self.YAWN_COUNT += 1
        else:
            self.YAWN_COUNT = 0

        if self.YAWN_COUNT >= self.YAWN_THRESHOLD:

            if draw:
                cv.putText(
                    frame,
                    "Yawn Detected!",
                    (30, 30),
                    cv.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2
                )

            return True

        return False