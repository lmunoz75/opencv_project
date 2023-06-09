import cv2
from datetime import datetime

COLOR_GRAY = (238, 234, 234)
COLOR_BLUE = (219, 85, 96)

cap = cv2.VideoCapture(0)
ww, hh = int(cap.get(3)), int(cap.get(4))
w, h = int(ww/16), int(hh/16)

while True:
    ret, frame = cap.read()
    
    if ret:
        out = cv2.flip(frame, 1)
        out = cv2.resize(out, (w, h), interpolation=cv2.INTER_AREA)
        out = cv2.resize(out, (ww, hh), interpolation=cv2.INTER_AREA)
        
        hora_actual_str = f"{datetime.now():%H:%M:%S}"
        cv2.rectangle(out, pt1=(ww - int(ww / 4), hh - 40), 
                      pt2=(ww - 30, hh - 5), 
                      color=COLOR_BLUE, thickness=-1)
        cv2.putText(out, text=hora_actual_str, 
                    org=(ww - int(ww / 4) + 10, hh - 15), 
                    fontFace=cv2.FONT_HERSHEY_COMPLEX, 
                    fontScale=0.75, color=COLOR_GRAY, thickness=2)
 
        cv2.imshow("Video", out)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()
