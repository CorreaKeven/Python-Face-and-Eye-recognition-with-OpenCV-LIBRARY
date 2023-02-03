from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QPixmap

import cv2

valor_escala = 1.05


####################################webcam
captura_video = cv2.VideoCapture(0)
######################################

classificador_faces = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
faces = classificador_faces.detectMultiScale(img_pb,
                                       scaleFactor = valor_escala,
                                       minNeighbors = 3,
                                       minSize = (20,20),
                                       flags = cv2.CASCADE_SCALE_IMAGE)

classificador_olhos=cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
olhos = classificador_olhos.detectMultiScale(img_pb)
    
def func_inicia_captura():
##    janela.imagem.setPixmap(QPixmap("pb.png"))
    cv2.imshow("Video On-line",frame)
##  captura_video = cv2.VideoCapture(0)

def func_atualiza_rosto():
    valor_escala = janela.slider.value()/100
    classificador = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = classificador.detectMultiScale(img_pb,
                                           scaleFactor = valor_escala,
                                           minNeighbors = 3,
                                           minSize = (20,20),
                                           flags = cv2.CASCADE_SCALE_IMAGE)
##    print (faces)
    for (x, y, w, h) in faces:
        cv2.rectangle(img_original, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cv2.imwrite("colorida_identificada.png", img_original)
        janela.imagem.setPixmap(QPixmap("colorida_identificada.png"))
        
def func_atualiza_olhos():
    valor_escala2 = janela.slider1.value()/100
    classificador_olhos=cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
    olhos = classificador_olhos.detectMultiScale(img_pb,
                                                 scaleFactor = valor_escala2,
                                                 minNeighbors = 3,
                                                 minSize = (35,35),
                                                 flags = cv2.CASCADE_SCALE_IMAGE)
##    print (olhos)
    for (x, y, w, h) in olhos:
        cv2.rectangle(img_original2,
                  (x, y),
                  (x+w,y+h),
                  (255, 0, 0),
                  5)
        janela.imagem.setPixmap(QPixmap("colorida_identificada_olhos.png"))


while True:
    
    ok,frame = captura_video.read()
    print(ok)
    img_pb2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = classificador_faces.detectMultiScale(img_pb2,
                                       scaleFactor = 1.1,
                                       minNeighbors = 3,
                                       minSize = (110,110),
                                       flags = cv2.CASCADE_SCALE_IMAGE)
    olhos = classificador_olhos.detectMultiScale(img_pb2,
                                                 scaleFactor = 1.1,
                                                 minNeighbors = 6,
                                                 minSize = (15,15))
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
    for (x, y, w, h) in olhos:
        cv2.circle(frame,(x+(w//2), y+(h//2)), w//2 ,(0, 0, 255),2)
 
    cv2.imshow("Video On-line",frame)
    if cv2.waitKey(1) &0xFF==ord('a'):#ord retorna valor unicode  'a'=>0110.0001&1111.1111=0110.0001
       break
    
    app = QtWidgets.QApplication([])
    janela = uic.loadUi("janela_t3.ui")
    janela.imagem2.setPixmap(QPixmap("logo.png"))
    janela.pushButton_1.clicked.connect(func_inicia_captura)
    janela.slider.valueChanged.connect(func_atualiza_rosto)
    janela.slider1.valueChanged.connect(func_atualiza_olhos)
    
    
    captura_video.release()
##    cv2.destroyAllWindows()
##    janela.show()
    app.exec()  
