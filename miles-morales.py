import cv2
import numpy as np

class Camera:


    def __init__(self) -> None:
        self.cap = cv2.VideoCapture(0)

        while (self.cap.isOpened()):
            self.ret, self.frame = self.cap.read()
            self.crop = self.cut()

            cv2.imshow("teste", self.crop)
            cv2.imshow("normal", self.frame)

            if cv2.waitKey(1) == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


    def cut(self):

        self.scale = 0.2

        height_min = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * self.scale / 2)
        height_max = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) - height_min)

        width_min = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) * self.scale / 2)
        width_max = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) - width_min)
        
        return self.frame[height_min:height_max, width_min:width_max]


p1 = Camera()