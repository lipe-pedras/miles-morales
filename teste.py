import cv2
import numpy as np

class Color:
    def __init__(self, name, min_range, max_range):
        self.name = name
        self.min = np.array(min_range)
        self.max = np.array(max_range)
        self.has = False
        self.pixels = 0

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        scale = 0.2

        height_min = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale / 2)
        height_max = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) - height_min)

        width_min = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) * scale / 2)
        width_max = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) - width_min)

        self.colors = [
            Color("Orange", [21, 89, 116], [8, 255, 255]),
            Color("Red", [170, 105, 125], [179, 255, 255]),
            Color("Green", [84, 113, 60], [101, 255, 150]),
            Color("Yellow", [20, 120, 113], [30, 255, 255])
        ]

        while self.cap.isOpened():
            self.ret, self.frame = self.cap.read()
            self.crop = self.frame[height_min:height_max, width_min:width_max]
            cv2.imshow("teste", self.crop)
            self.detect()
            self.print_status()

            if cv2.waitKey(1) == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def detect(self):
        kernel = np.ones((5, 5), np.uint8)
        threshold = 5000

        for color in self.colors:
            hsv = cv2.cvtColor(self.crop, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, color.min, color.max)
            mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel=kernel)
            color.pixels = np.sum(mask[:, :] > 0)

            if color.pixels > threshold:
                color.has = True
            else:
                color.has = False

    def print_status(self):
        max_pixels = 0
        max_color = None

        for color in self.colors:
            if color.pixels > max_pixels:
                max_pixels = color.pixels
                max_color = color

        if max_color is not None:
            print(f"Color: {max_color.name} - Pixels: {max_color.pixels}")
