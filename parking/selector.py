import pickle, cv2, sys

class Selector():

    def __init__(self) -> None:
        
        self.ancho, self.alto = 107, 48
        self.lugares = 0
        self.ctrl_loop = True
        try:
            with open('Lugares.dat', 'rb') as f:
                self.listaLugares = pickle.load(f)
        except:
            self.listaLugares = []
            

    def mouseClick(self, events, x, y, flags, params): #Flags y params para que no de warnings

        if events == cv2.EVENT_LBUTTONDOWN: #Al dar click derecho
            self.lugares += 1
            self.listaLugares.append((x, y))#Agregamos el cuadro a los lugares

        if events == cv2.EVENT_RBUTTONDOWN: #Al dar click derecho
            for i, pos in enumerate(self.listaLugares):
                x1, y1 = pos
                if x1 < x < x1 + self.ancho and y1 < y < y1 + self.alto:
                    self.listaLugares.pop(i) #Borramos el lugar

        if events == cv2.EVENT_MOUSEWHEEL:
            self.ctrl_loop = False
    
        with open('Lugares.dat', 'wb') as f: #Escribimos los cambios
            pickle.dump(self.listaLugares, f)
    
    def start(self):

        while self.ctrl_loop:
            img = cv2.imread('assets/Parking.png')
            for pos in self.listaLugares:
                cv2.rectangle(img, pos, (pos[0] + self.ancho, pos[1] + self.alto), (255, 0, 255), 2)
        
            cv2.imshow("Image", img)
            cv2.setMouseCallback("Image", self.mouseClick)
            cv2.waitKey(1)
