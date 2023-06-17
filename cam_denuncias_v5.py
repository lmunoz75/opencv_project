import cv2
from datetime import datetime

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def insert_logo(image, logo_file, size=80):
    img_logo = cv2.imread(logo_file)
    img_logo = cv2.resize(img_logo, (size, size))
    img_logo_gray = cv2.cvtColor(img_logo, cv2.COLOR_BGR2GRAY)
    tresh, mask = cv2.threshold(img_logo_gray, 128, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    
    ROI_fondo = image[-(30+size):-30, -(30+size):-30, :]
    frente = cv2.bitwise_and(img_logo, img_logo, mask=mask_inv)
    fondo = cv2.bitwise_and(ROI_fondo, ROI_fondo, mask=mask)
    image[-(30+size):-30, -(30+size):-30, :] = cv2.add(frente, fondo)
    
    return image


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


def pixelate_face(image):
    global face_cascade
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)
    
    for x, y, w, h in faces:
        ROI = image[y-50:y+h+50, x-25:x+w+25, :]
        roi_hh, roi_ww, _ = ROI.shape
        roi_h, roi_w = int(roi_hh/16), int(roi_ww/16)
        
        ROI = cv2.resize(ROI, (roi_w, roi_h), interpolation=cv2.INTER_AREA)
        ROI = cv2.resize(ROI, (roi_ww, roi_hh), interpolation=cv2.INTER_AREA)
        image[y-50:y+h+50, x-25:x+w+25, :] = ROI
    
    return image     


cap = cv2.VideoCapture(0)
ww, hh = int(cap.get(3)), int(cap.get(4))
start_rec_time = datetime.now()

while True:
    ret, frame = cap.read()
    
    if ret:
        out = cv2.flip(frame, 1)
        out = pixelate_face(out)
        out = cam_rec_format(out, color=(0, 0, 255), start_time=start_rec_time)
        out = insert_logo(out, ".\\img\\incognito_logo.jpg", size=50)
        
        cv2.imshow("Video", out)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()
