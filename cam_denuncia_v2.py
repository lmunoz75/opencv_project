import cv2
from datetime import datetime

def cam_rec_format(image, start_time, color=(0, 0, 0), thick=2):
    """
    cam_rec_format: Funcion que retorna una imagen con el formato de una cámara

    Parameters
    ----------
    image : numpy.ndarray
        Arreglo numpy con la imagen de formatear.
    start_time : datetime, opcional
        El tiempo inicial de la grabacion.
    color : tuple, opcional
        El color de los objetos gráficos. El valor por defecto es (0, 0, 0).
    thick : int, opcional
        El ancho del trazo de los objetos gráficos. El valor por defecto es 2.

    Returns
    -------
    image : numpy.ndarray
        Arreglo con la imagen formateada.

    """
    
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

cap = cv2.VideoCapture(0)
ww, hh = int(cap.get(3)), int(cap.get(4))
w, h = int(ww/16), int(hh/16)
start_rec_time = datetime.now()

while True:
    ret, frame = cap.read()
    
    if ret:
        out = cv2.flip(frame, 1)
        out = cv2.resize(out, (w, h), interpolation=cv2.INTER_AREA)
        out = cv2.resize(out, (ww, hh), interpolation=cv2.INTER_AREA)
        out = cam_rec_format(out, color=(0, 0, 255), start_time=start_rec_time)
        
        cv2.imshow("Video", out)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()
