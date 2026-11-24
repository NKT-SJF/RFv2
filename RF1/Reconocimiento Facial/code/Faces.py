#pip install opencv-contrib-python, imutils, serial, requests, time
import cv2 as cv
import os
import imutils
import time
import sys

#inputs
name = sys.argv[1] if len(sys.argv) > 1 else "PersonaDesconocida"
path = r'C:\Users\THN_LAB\Desktop\RF1\Reconocimiento Facial\Data'

#Creación de carpeta
personPath = path + "/" + name
if not os.path.exists(personPath):
    print(f"Carpeta creada: {personPath}")
    os.makedirs(personPath)

#Cargar video
#cap = cv.VideoCapture("rtsp://admin:admin@10.50.4.191/cam/realmonitor?channel=1&subtype=0",cv.CAP_FFMPEG)
cap = cv.VideoCapture(0,cv.CAP_DSHOW)
if not cap.isOpened():
    print("Error: No se pudo abrir el video. Verifique la ruta...")
    exit()

#Cargar clasificador Haar
os.chdir(os.path.dirname(__file__))
faceClassif = cv.CascadeClassifier(
    cv.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

if faceClassif.empty():
    print("ERROR: No se pudo cargar Haar Cascade")
    exit()

print("Clasificador Haar cargado correctamente")

#Variables para la detección
count = 0
cant = 0
ultimoGuardado = time.time()

#Procesando el video
print('Procesando video, presione "ESC" para salir...')
while True:
    ret, frame = cap.read()
    if not ret: 
        print("Fin del video o error al leer el frame")
        break

    #Redimensionar y convertir a escala de grises
    frame = imutils.resize(frame,width=640)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    auxframe = frame.copy()

    #Detección de caras
    faces = faceClassif.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in faces:
        cv.rectangle(frame, (x,y), (x+w,y+h),(0,255,0),2)
        
        #Guardar imagen si ha pasado x segundos
        if time.time() - ultimoGuardado >= 0.3:
            rostro = auxframe[y:y+h,x:x+w]
            rostro = cv.resize(rostro,(150,150), interpolation=cv.INTER_CUBIC)
            cv.imwrite(personPath + '/rostro_{}.jpg'.format(cant),rostro)
            cant += 1
            count += 1
            ultimoGuardado = time.time()

    cv.imshow('frame',frame)

    k = cv.waitKey(1)
    if k == 27 or count >=400 :
        break

cap.release()
cv.destroyAllWindows()