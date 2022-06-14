from time import sleep
import cv2
import pickle
import cvzone
import numpy as np
from threading import Thread
from conexion import Conexion

class Detector():
    
    def __init__(self) -> None:
        self.cap = cv2.VideoCapture('assets/video.avi') #Archivo de video. A manera de emular un stream de CCTV
        self.ancho = 40
        self.alto = 40
        self.hilo = Thread(target=self.actualizar)
        self.lugares = np.empty(92, dtype=int)
        self.conexion = Conexion("jorge","SisTemas")

        with open('Lugares.dat', 'rb') as f: #Cargamos los cajones de los lugares
            self.posList = pickle.load(f)

    def actualizar(self):
        for _ in range(3):
            sleep(3)
            self.conexion.actualizarLugares(self.lugares)

    def checkParkingSpace(self, imgPro):
        spaceCounter = 0
        for i, pos in enumerate (self.posList):

            id = i
            x, y = pos
    
            imgCrop = imgPro[y:y + self.alto, x:x + self.ancho]
            count = cv2.countNonZero(imgCrop)
    
            if count < 200:
                color = (0, 255, 0)
                thickness = 5
                spaceCounter += 1
                self.lugares[i] = 0
            else:
                color = (0, 0, 255) #R:0, G:0, B: 255
                thickness = 2
                self.lugares[i] = 1
    
            cv2.rectangle(self.img, pos, (pos[0] + self.ancho, pos[1] + self.alto), color, thickness)
            cvzone.putTextRect(self.img, str(id), (x, y + self.alto - 3), scale=1,thickness=1, offset=0, colorR=color)
    
        cvzone.putTextRect(self.img, f'Libres: {spaceCounter}/{len(self.posList)}', (80, 30), scale=1,
                            thickness=1, offset=20, colorR=(0,200,0))
    
    def processImage(self, img):

        img_grises = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        img_difuminado = cv2.GaussianBlur(img_grises, (3, 3), 1)
        img_binaria = cv2.adaptiveThreshold(img_difuminado, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 25, 16)
        img_difuminado = cv2.medianBlur(img_binaria, 5)
        kernel = np.ones((3, 3), np.uint8)
        imgDilate = cv2.dilate(img_difuminado, kernel, iterations=1)
        return imgDilate
    
    def start(self):
        self.hilo.start()
        b = True
        while b:
 
            if self.cap.get(cv2.CAP_PROP_POS_FRAMES) == self.cap.get(cv2.CAP_PROP_FRAME_COUNT):
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                #b = False

            _, self.img = self.cap.read()
            #self.img = cv2.imread('assets/img.jpg')
            procImg = self.processImage(self.img)
            #cv2.imshow("Binario", procImg)
            self.checkParkingSpace(procImg) 
            cv2.imshow("Parking", self.img)
            cv2.waitKey(1000)
