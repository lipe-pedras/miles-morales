import cv2
import numpy as np

class Camera:


    def __init__(self) -> None:


        self.cap = cv2.VideoCapture(0)

        #tamanho do corte -> 0.2 == 20% => remove 10% de cada lado do vídeo
        scale = 0.2

        height_min = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale / 2)
        height_max = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) - height_min)

        width_min = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) * scale / 2)
        width_max = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) - width_min)

        # banda de cores
        #laranja 
        orange_max = np.array([20, 255, 255])
        orange_min = np.array([10, 174, 111])

        #vermelho
        red_max = np.array([5, 255, 255])
        red_min = np.array([0, 160, 95])

        #verde
        green_max = np.array([95, 120, 255])
        green_min = np.array([36, 49, 46])

        #amarelo
        yellow_max = np.array([30, 255, 255])
        yellow_min = np.array([20, 120, 113])

        while (self.cap.isOpened()):
            self.ret, self.frame = self.cap.read()
            self.crop = self.frame[height_min:height_max, width_min:width_max]
        
            cv2.imshow("teste", self.crop)
            cv2.imshow("normal", self.frame)

            if cv2.waitKey(1) == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


p1 = Camera()