import pickle, cv2, math

class Selector():

    def __init__(self) -> None:
        
        self.ancho, self.alto = 40, 40
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
    
    def draw_angled_rec(self, x0, y0, width, height, angle, img):

        _angle = angle * math.pi / 180.0
        b = math.cos(_angle) * 0.5
        a = math.sin(_angle) * 0.5
        pt0 = (int(x0 - a * height - b * width),
            int(y0 + b * height - a * width))
        pt1 = (int(x0 + a * height - b * width),
            int(y0 - b * height - a * width))
        pt2 = (int(2 * x0 - pt0[0]), int(2 * y0 - pt0[1]))
        pt3 = (int(2 * x0 - pt1[0]), int(2 * y0 - pt1[1]))

        cv2.line(img, pt0, pt1, (255, 0, 255), 3)
        cv2.line(img, pt1, pt2, (255, 0, 255), 3)
        cv2.line(img, pt2, pt3, (255, 0, 255), 3)
        cv2.line(img, pt3, pt0, (255, 0, 255), 3)
    
    def start(self):

        while self.ctrl_loop:
            img = cv2.imread('assets/img.jpg')
            for pos in self.listaLugares:
                #self.draw_angled_rec(pos[0], pos[1], self.ancho, self.alto, 30, img)
                cv2.rectangle(img, pos, (pos[0] + self.ancho, pos[1] + self.alto), (255, 0, 255), 2)
                        
            cv2.imshow("Image", img)
            cv2.setMouseCallback("Image", self.mouseClick)
            cv2.waitKey(1)