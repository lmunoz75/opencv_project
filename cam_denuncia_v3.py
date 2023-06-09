# Hacer click en la imagen de la cámara en dos puntos distintos
# para crear una zona donde se aplicara el efecto de pixeleado
import cv2
from datetime import datetime

pt1 = (0, 0)
pt2 = (0, 0)
topLeft_clicked = False
botRight_clicked = False

def set_ROI(event, x, y, flags, param):
    global pt1, pt2, topLeft_clicked, botRight_clicked
    
    if event == cv2.EVENT_LBUTTONDOWN:
        if topLeft_clicked and botRight_clicked:
            pt1 = (0, 0)
            pt2 = (0, 0)
            topLeft_clicked = False
            botRight_clicked = False

        if topLeft_clicked == False:
            pt1 = (x, y) 
            topLeft_clicked = True
        elif botRight_clicked == False:
            pt2 = (x, y) 
            botRight_clicked = True
            


def cam_rec_format(image, start_time, color=(0, 0, 0), thick=2):    
    elapsed = f"{datetime.now() - start_time}"[:-3]
    cv2.putText(image, text=elapsed, 
                org=(ww - int(2 * ww / 3) + 40, hh - 40), 
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                fontScale=0.7, color=color, thickness=thick)
    
    cv2.putText(image, text="REC", 
                org=(70, 45), fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                fontScale=0.8, color=color, thickness=thick)

    cv2.putText(image, text="CAM 1", 
            org=(70, hh - 45), fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
            fontScale=0.8, color=color, thickness=thick)    
    
    cv2.line(image, (10, 10), (10, 90), color=color, thickness=thick)
    cv2.line(image, (10, 10), (90, 10), color=color, thickness=thick)
    
    cv2.line(image, (10, hh - 10), (10, hh - 90), color=color, thickness=thick)
    cv2.line(image, (10, hh - 10), (90, hh - 10), color=color, thickness=thick)
    
    cv2.line(image, (ww - 10, 10), (ww - 10, 90), color=color, thickness=thick)
    cv2.line(image, (ww - 10, 10), (ww - 90, 10), color=color, thickness=thick)
    
    cv2.line(image, (ww - 10, hh - 10), (ww - 10, hh - 90), color=color, thickness=thick)
    cv2.line(image, (ww - 10, hh - 10), (ww - 90, hh - 10), color=color, thickness=thick)
    
    cv2.rectangle(image, (ww - 70, 20), (ww - 30, 40), color=color, thickness=thick)
    cv2.rectangle(image, (ww - 30, 25), (ww - 20, 35), color=color, thickness=thick)
    cv2.rectangle(image, (ww - 65, 26), (ww - 56, 34), color=color, thickness=-1)
    cv2.rectangle(image, (ww - 52, 26), (ww - 43, 34), color=color, thickness=-1)
    
    seconds = int(elapsed.split(":")[-1][:2])
    if seconds % 2 == 0:
        cv2.circle(image, (44, 36), 12, color=(0, 0, 255), thickness=-1)
            
    return image


cv2.namedWindow("Video")
cv2.setMouseCallback("Video", set_ROI)

cap = cv2.VideoCapture(0)
ww, hh = int(cap.get(3)), int(cap.get(4))
w, h = int(ww/16), int(hh/16)
start_rec_time = datetime.now()

while True:
    ret, frame = cap.read()
    
    if ret:
        # Se gira la imagen en el eje vertical
        out = cv2.flip(frame, 1)
        
        # Se pixelea la imagen en el ROI
        if topLeft_clicked and botRight_clicked:
            ROI = out[pt1[1]:pt2[1], pt1[0]:pt2[0], :]
            roi_hh, roi_ww, _ = ROI.shape
            roi_h, roi_w = int(roi_hh/25), int(roi_ww/25)
        
            ROI = cv2.resize(ROI, (roi_w, roi_h), interpolation=cv2.INTER_AREA)
            ROI = cv2.resize(ROI, (roi_ww, roi_hh), interpolation=cv2.INTER_AREA)
            
            out[pt1[1]:pt2[1], pt1[0]:pt2[0], :] = ROI
            
        # Se le da formato de camara de grabacion a la imagen
        out = cam_rec_format(out, color=(0, 0, 255), start_time=start_rec_time)
        
        cv2.imshow("Video", out)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()

