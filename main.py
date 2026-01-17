import cv2
import numpy as np

ROAD_WIDTH_PX = 550  
REAL_ROAD_WIDTH_M = 3.5 

PIXELS_PER_METER = ROAD_WIDTH_PX / REAL_ROAD_WIDTH_M 

def detect_potholes_with_measurements(image_path):
    img = cv2.imread(image_path)
    if img is None: return

    height, width = img.shape[:2]
    if width > 600:
        scale = 600 / width
        img = cv2.resize(img, (0, 0), fx=scale, fy=scale)

        global PIXELS_PER_METER
        PIXELS_PER_METER = PIXELS_PER_METER * scale
    
    display_img = img.copy()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    edges = cv2.Canny(blurred, 30, 150)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilated = cv2.dilate(edges, kernel, iterations=3)
    closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel, iterations=3)

    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    count = 0
    for cnt in contours:
        area_px = cv2.contourArea(cnt)
        
        if area_px > 300:
            hull = cv2.convexHull(cnt)
            if cv2.contourArea(hull) == 0: continue
            solidity = float(area_px) / cv2.contourArea(hull)
            
            if solidity > 0.6:
                x, y, w, h = cv2.boundingRect(cnt)
                aspect = float(w) / h
                
                if 0.3 < aspect < 3.5:
                    count += 1
                    
                    area_m2 = area_px / (PIXELS_PER_METER ** 2)

                    label = f"{area_m2:.2f} m2"

                    cv2.drawContours(display_img, [cnt], -1, (0, 255, 0), 2)
                    cv2.rectangle(display_img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    
                    cv2.putText(display_img, label, (x, y - 5), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    print(f"Total Detected: {count}")
    cv2.imshow("Pothole Area Measurement", display_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

detect_potholes_with_measurements("demo.png")