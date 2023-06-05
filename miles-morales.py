import cv2
import numpy as np

class Orange:
    # laranja 
    max = np.array([8, 255, 255])
    min = np.array([21, 89, 116])
    has = False
    pixels = 0

class Red:
    # vermelho
    max = np.array([179, 255, 255])
    min = np.array([170, 105, 125])
    has = False
    pixels = 0

class Green:
    # verde
    max = np.array([101, 255, 150])
    min = np.array([84, 113, 60])
    has = False
    pixels = 0

class Yellow:
    # amarelo
    max = np.array([30, 255, 255])
    min = np.array([20, 120, 113])
    has = False
    pixels = 0

# dictionary of each subtitle colour
color_subtitles = {
    Orange: "Laranja",
    Red: "Vermelho",
    Green: "Verde",
    Yellow: "Amarelo"
}

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            self.crop = frame

            self.detect()

            self.check_colors()

            # Show the frame with contours
            cv2.imshow("frame", frame)

            if cv2.waitKey(1) == ord("q"):
                break
                
        self.cap.release()
        cv2.destroyAllWindows()

    def detect(self):
        colors = [Yellow, Green, Red, Orange]
        kernel = np.ones((5, 5), np.uint8)
        threshold = 5000

        for color in colors:
            # Convert BGR (default format in OpenCV) to HSV (used for color detection)
            hsv = cv2.cvtColor(self.crop, cv2.COLOR_BGR2HSV)

            # Create a mask with the desired color range
            mask = cv2.inRange(hsv, color.min, color.max)
            mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel=kernel)
            
            color.pixels = np.sum(mask[:, :] > 0)

            if color.pixels > threshold:
                color.has = True
            else:
                color.has = False

            # Find contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Draw contours on the frame
            cv2.drawContours(self.crop, contours, -1, (0, 0, 0), 2)

            # Adding subtitles to the countours
            for contour in contours:
                if len(contour) >= 4: #check if the contour is a rectangle    
                    x, y, w, h = cv2.boundingRect(contour)
                    color_name = color_subtitles[color] 
                    
                    # Centering subtitles:
                    text_size, _ = cv2.getTextSize(color_name, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)

                    # Calculus of the central position:
                    text_x = x + (w - text_size[0]) // 2
                    text_y = y + (h - text_size[1]) // 2    
                        
                    cv2.putText(self.crop, color_name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2, cv2.LINE_AA)

    def check_colors(self):
        # Condition if more than one color is detected
        if sum([Orange.has, Red.has, Green.has, Yellow.has]) > 1:
            print("More than one color has been detected!")

            for color1 in [Orange, Red, Green, Yellow]:
                for color2 in [Orange, Red, Green, Yellow]:
                    # Condition to avoid comparing a class with itself
                    if not (color1 == color2):
                        if color1.has and color2.has:
                            # Parameter for priority
                            if color1.pixels > color2.pixels:
                                color2.has = False
                                print(f"{color2} set to False")
                            else:
                                color1.has = False
                                print(f"{color1} set to False")
                    # Remove later
                    else:
                        print(color1, color2)
        else:
            # Continue normal execution
            pass

    

p1 = Camera()
p1.run()
