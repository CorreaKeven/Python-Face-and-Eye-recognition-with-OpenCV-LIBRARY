from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QPixmap
import time
import cv2
##import serial

##micro = serial.Serial(port='COM12', baudrate=115200, timeout=.1)


valor_escala_face = 1.05
valor_escala_olhos = 1.0007

img_original = cv2.imread("reuniao.jpg")
cv2.imwrite("colorida.jpg", img_original)
classificador_faces = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
classificador_olhos = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

img_pb = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
cv2.imwrite("pb.png", img_pb)


faces = classificador_faces.detectMultiScale(img_pb,
                                           scaleFactor = valor_escala_face,
                                           minNeighbors = 3,
                                           minSize = (80,80),
                                           flags = cv2.CASCADE_SCALE_IMAGE)


olhos = classificador_olhos.detectMultiScale(img_pb,
                                            scaleFactor= valor_escala_olhos,
                                            minNeighbors=3,
                                            maxSize=(35,35))


def func_mostra_colorida():
    janela.imagem.setPixmap(QPixmap("colorida.jpg"))
 
def func_mostra_pb():
    janela.imagem.setPixmap(QPixmap("pb.jpg"))
    
#identifica  faces e olhos
def func_mostra_detectada():
    janela.imagem.setPixmap(QPixmap("colorida_identificada.png"))
    janela.imagem.setPixmap(QPixmap("colorida_identificada_olhos.png"))
    print(faces)
    guarda_faces = len(faces)
    guarda_olhos = len(olhos)
    teste_face = ("Faces:" + str(guarda_faces))
    teste_olhos = ("Olhos:" + str(guarda_olhos))
    valores_coletados = (guarda_faces,guarda_olhos )
    print(teste_face)
    print(teste_olhos)
    print(valores_coletados)
    
#flag - que envia quantidade de olhos e faces para o lcd
    janela.lcdNumber.display(guarda_faces)
    janela.lcdNumber2.display(guarda_olhos)

def func_atualiza_vizinhos1():
    valor_escala_face = janela.slider.value()/100
    print(valor_escala_face)
   
    classificador_faces = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = classificador_faces.detectMultiScale(img_pb,
                                                 scaleFactor = valor_escala_face,
                                                 minNeighbors = 3,
                                                 minSize = (90,90),
                                                 flags = cv2.CASCADE_SCALE_IMAGE)

    for (x, y, w, h) in faces:
        cv2.rectangle(img_original, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cv2.imwrite("colorida_identificada.png", img_original)
        janela.ImagemCam.setPixmap(QPixmap("colorida_identificada.png"))
       

def func_atualiza_vizinhos2():
    valor_escala_olhos = janela.slider2.value()/100
    print(valor_escala_olhos)

    classificador_olhos = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
    olhos = classificador_olhos.detectMultiScale(img_pb,
                                                 scaleFactor = valor_escala_olhos,
                                                 minNeighbors = 3,
                                                 maxSize=(35,35))

                                                 
   
    for (x, y, w, h) in olhos:
        cv2.rectangle(img_original, (x, y), (x+w, y+h),  (0, 255, 255), 2)
        cv2.imwrite("colorida_identificada_olhos.png", img_original)
        janela.ImagemCam.setPixmap(QPixmap("colorida_identificada_olhos.png"))


#comunicação serial
##micro.write(bytes(valores_coletados, 'utf-8'))
##micro.close()
 
app = QtWidgets.QApplication([])
janela = uic.loadUi("janela_t3.ui")
janela.imagem2.setPixmap(QPixmap("logo.png"))
janela.pushButton_1.clicked.connect(func_mostra_detectada)
janela.slider.valueChanged.connect(func_atualiza_vizinhos1)
janela.slider.valueChanged.connect(func_atualiza_vizinhos2)

janela.show()
app.exec()
