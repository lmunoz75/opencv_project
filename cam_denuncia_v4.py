import cv2
from datetime import datetime

pt1 = (0, 0)
pt2 = (0, 0)
topLeft_clicked = False
botRight_clicked = False

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


def pixelate_ROI(image, color):
    global pt1, pt2, topLeft_clicked, botRight_clicked
    
    if topLeft_clicked and botRight_clicked:
        ROI = image[pt1[1]:pt2[1], pt1[0]:pt2[0], :]
        roi_hh, roi_ww, _ = ROI.shape
        roi_h, roi_w = int(roi_hh/16), int(roi_ww/16)
        
        ROI = cv2.resize(ROI, (roi_w, roi_h), interpolation=cv2.INTER_AREA)
        ROI = cv2.resize(ROI, (roi_ww, roi_hh), interpolation=cv2.INTER_AREA)
        
        cv2.putText(image, text="Pixeleado Activo", 
                    org=(pt1[0], pt1[1] - 10), 
                    fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, 
                    fontScale=0.6, color=color, thickness=1)
        
        image[pt1[1]:pt2[1], pt1[0]:pt2[0], :] = ROI
        
    return image     


cv2.namedWindow("Video")
cv2.setMouseCallback("Video", set_ROI)

cap = cv2.VideoCapture(0)
ww, hh = int(cap.get(3)), int(cap.get(4))
start_rec_time = datetime.now()

while True:
    ret, frame = cap.read()
    
    if ret:
        out = cv2.flip(frame, 1)
        out = pixelate_ROI(out, color=(0, 0, 255))
        out = cam_rec_format(out, color=(0, 0, 255), start_time=start_rec_time)
        out = insert_logo(out, ".\\img\\incognito_logo.jpg", size=100)
        
        cv2.imshow("Video", out)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()
