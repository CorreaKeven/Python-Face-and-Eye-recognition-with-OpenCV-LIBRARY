import cv2

vetor_imagem = cv2.imread("reuniao.jpg");
cv2.imshow("Foto de uma reuniao", vetor_imagem)
print(vetor_imagem)
vetor_imagem_pb = cv2.cvtColor(vetor_imagem, cv2.COLOR_BGR2GRAY)
cv2.imshow("Foto de uma reuniao pb", vetor_imagem_pb)
print(vetor_imagem_pb)
classificador=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
faces = classificador.detectMultiScale(vetor_imagem_pb)
print(faces)
