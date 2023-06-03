import cv2
import numpy as np


class Orange:

    #laranja 
    max = np.array([8, 255, 255])
    min = np.array([21, 89, 116])
    has = False
    pixels = 0


class Red:
    #vermelho
    max = np.array([179, 255, 255])
    min = np.array([170, 105, 125])
    has = False
    pixels = 0


class Green:

    #verde
    max = np.array([101, 255, 150])
    min = np.array([84, 113, 60])
    has = False
    pixels = 0


class Yellow:

    #amarelo
    max = np.array([30, 255, 255])
    min = np.array([20, 120, 113])
    has = False
    pixels = 0


class Camera:


    def __init__(self) -> None:


        self.cap = cv2.VideoCapture(0)

        #tamanho do corte -> 0.2 == 20% => remove 10% de cada lado do vídeo
        scale = 0.2

        height_min = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale / 2)
        height_max = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) - height_min)

        width_min = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) * scale / 2)
        width_max = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) - width_min)


        while (self.cap.isOpened()):
            self.ret, self.frame = self.cap.read()
            self.crop = self.frame[height_min:height_max, width_min:width_max]
        
            cv2.imshow("teste", self.crop)

            self.detect()

            for color in [Orange, Green, Red, Yellow]:
                if color.has == True:
                     print(color)


            if cv2.waitKey(1) == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


    def detect(self):

        colors = [Yellow, Green, Red, Orange]
        kernel = np.ones((5, 5), np.uint8)
        threshold = 5000

        for color in colors:
            #conversão de bgr (padrão do cv) para hsv (padrão usado na detecção)
            hsv = cv2.cvtColor(self.crop, cv2.COLOR_BGR2HSV)

            #matriz com a cor desejada
            mask = cv2.inRange(hsv, color.min, color.max)
            mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel=kernel)
            

            color.pixels = np.sum(mask[:,:] > 0)


            if color.pixels > threshold:
                    color.has = True
            else:
                    color.has = False


p1 = Camera()