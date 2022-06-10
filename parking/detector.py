from time import sleep
import cv2
import pickle
import sys
import cvzone
import numpy as np
from threading import Thread
from conexion import Conexion

class Detector():
    
    def __init__(self) -> None:
        self.cap = cv2.VideoCapture('assets/Parking.mp4') #Archivo de video. A manera de emular un stream de CCTV
        self.ancho = 107
        self.alto = 48
        self.hilo = Thread(target=self.actualizar)
        self.lugares = np.empty(69, dtype=int)
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
            count = cv2.countNonZero(imgCrop) #Contamos los píxeles blancos dentro del cajón
    
            if count < 900: #Si contamos menos de 900 puntos, diremos que el lugar está vacío
                color = (0, 255, 0)
                thickness = 5
                spaceCounter += 1
                self.lugares[i] = 0
            else:
                color = (0, 0, 255) #R:0, G:0, B: 255
                thickness = 2
                self.lugares[i] = 1
    
            cv2.rectangle(self.img, pos, (pos[0] + self.ancho, pos[1] + self.alto), color, thickness)
            cvzone.putTextRect(self.img, str(id), (x, y + self.alto - 3), scale=1, #Para mostrar los pixeles
                               thickness=2, offset=0, colorR=color)
    
        cvzone.putTextRect(self.img, f'Libres: {spaceCounter}/{len(self.posList)}', (80, 30), scale=1,
                            thickness=1, offset=20, colorR=(0,200,0))
    
    def start(self):
        self.hilo.start()
        while True:
 
            if self.cap.get(cv2.CAP_PROP_POS_FRAMES) == self.cap.get(cv2.CAP_PROP_FRAME_COUNT):
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0) #Repetimos el video para fines demostrativos

            success, self.img = self.cap.read()
            imgGray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY) #No nos interesa trabajar con color, convertimos a escala de grises
            imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1) #Aplicamos difuminado gaussiano para suavizar bordes
            imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, #Convertimos a imagen "binaria"(bordes)
                                                cv2.THRESH_BINARY_INV, 25, 16)
            imgMedian = cv2.medianBlur(imgThreshold, 5)#De nuevo, suavizamos más, ahora sobre la imagen binaria
            kernel = np.ones((3, 3), np.uint8)
            imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)#Hacemos más anchos los píxeles de detección
        
            self.checkParkingSpace(imgDilate) #Llamamos al método de detección
            cv2.imshow("Image", self.img)
            # cv2.imshow("ImageBlur", imgBlur) #Imagen con difuminado gaussiano
            #cv2.imshow("ImageThres", imgMedian) #Imagen binaria
            cv2.waitKey(20) #Añadimos delay para que el video no se muestre en cámara rápida
