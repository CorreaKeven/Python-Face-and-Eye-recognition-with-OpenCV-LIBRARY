from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QPixmap
import cv2
import serial
import time

arduino = serial.Serial(port='COM10', baudrate=9600, timeout=.1)
print("Comunicação  via arduino")

valor_escala_face = 1.05
valor_escala_olhos = 1.007


img_original = cv2.imread("reuniao.png")
cv2.imwrite("colorida.png", img_original)

img_pb = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
cv2.imwrite("pb.png", img_pb)

classificador_faces = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
classificador_olhos = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

faces = classificador_faces.detectMultiScale(img_pb,
                                           scaleFactor = valor_escala_face,
                                           minNeighbors = 3,
                                           minSize = (50,50))

olhos = classificador_olhos.detectMultiScale(img_pb,
                                            scaleFactor= valor_escala_olhos,
                                            minNeighbors=3,
                                            maxSize=(40,40),
                                             minSize=(30,30))

                                             

print(olhos)    
for (x, y, w, h) in faces:
    cv2.rectangle(img_original, (x, y), (x+w, y+h), (255, 0, 0), 5)
    cv2.imwrite("colorida_identificada.png", img_original)     
for (x, y, w, h) in olhos:
    cv2.rectangle(img_original,(x,y), (x+w, y+h) ,(0, 255, 255), 2)
    cv2.imwrite("colorida_identificada.png", img_original)
                                           

def func_mostra_foto():
    janela.imagem.setPixmap(QPixmap("reuniao.png"))
 
def func_mostra_detectada():
    janela.imagem.setPixmap(QPixmap("colorida_identificada.png"))
##  janela.imagem.setPixmap(QPixmap("colorida_identificada_olhos.png"))
    guarda_faces = len(faces)
    guarda_olhos = len(olhos)   
    guarda_dados =[guarda_faces, guarda_olhos]
    print(guarda_dados)
    dadosStr = str(guarda_dados).strip('[]') ##Remove spaces at the beginning and at the end of the string:
    print(dadosStr)
    janela.lcdNumber.display(guarda_faces)
    janela.lcdNumber1.display(guarda_olhos)
    arduino.write(bytes(dadosStr, 'utf-8'))
    
   

def func_atualiza_faces():
    valor_escala_face = janela.slider.value()/100
    print(valor_escala_face)
    classificador_faces = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = classificador_faces.detectMultiScale(img_pb,
                                                 scaleFactor = valor_escala_face,
                                                 minNeighbors = 3,
                                                 minSize = (50,50))
    for (x, y, w, h) in faces:
        cv2.rectangle(img_original, (x, y), (x+w, y+h), (255, 0, 255), 2)
        cv2.imwrite("colorida_identificada.png", img_original)
        janela.imagem.setPixmap(QPixmap("colorida_identificada.png"))
        

    
def func_atualiza_olhos():
    valor_escala_olhos = janela.slider1.value()/100
    print(valor_escala_olhos)
    classificador_olhos = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
    olhos = classificador_olhos.detectMultiScale(img_pb,
                                                 scaleFactor = valor_escala_olhos,
                                                 minNeighbors = 3,
                                                 maxSize=(40,40),
                                                 minSize=(25,25))
    for (x, y, w, h) in olhos:
        cv2.circle(img_original,(x+(w//2),y+(h//2)), w//2 ,(0, 0, 255), 2)
        cv2.imwrite("colorida_identificada.png", img_original)
        janela.imagem.setPixmap(QPixmap("colorida_identificada.png"))

    
def func_Fecha_porta():
    arduino.close()
    janela.close()
    
 
app = QtWidgets.QApplication([])
janela = uic.loadUi("janela_t3.ui")
janela.imagem2.setPixmap(QPixmap("logo.png"))
janela.pushButton_1.clicked.connect(func_mostra_foto)
janela.pushButton_2.clicked.connect(func_mostra_detectada)
janela.pushButton_3.clicked.connect(func_Fecha_porta)
janela.slider.valueChanged.connect(func_atualiza_faces)
janela.slider1.valueChanged.connect(func_atualiza_olhos)
janela.show()
app.exec()
