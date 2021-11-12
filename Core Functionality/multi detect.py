import cv2 as cv 
import numpy as np
import paddlehub as hub
import mysql.connector
from datetime import datetime

#create a detector
face_recognizer = cv.face.LBPHFaceRecognizer_create()

#Load model for mask detection 123 and then face model
module = hub.Module(name="pyramidbox_lite_server_mask")
face_landmark = hub.Module(name="face_landmark_localization")
face_landmark.set_face_detector_module(hub.Module(name="ultra_light_fast_generic_face_detector_1mb_320"))
face_recognizer.read('model.yml')

#MYSQL Db connection using xampp
mydb=mysql.connector.connect(
		host = "localhost",
		user = "root",
		password = "",
		database = "attendance"
	)

mycursor=mydb.cursor()

#used to detect mask takes frame as input as dictionary gives out coordinate of the face and status mask
def detect_mask(frame):
    input_dict = {"data" : [frame]}
    results = module.face_detection(data=input_dict) #mask detection happens here
    coo_list = []
    label_list = []
    
    try:
        label = results[0]['data'][0]['label']
    except IndexError:
        coo_list.append([0,0,0,0])
        label_list.append(None)
        
    
    n = len(results[0]['data']) #number of people
    
    print(len(results[0]['data'])) 
    # print(results)== [{'data': [{'label': 'NO MASK', 'confidence': 0.8142542243003845, 'top': 260, 'bottom': 480, 'left': 427, 'right': 637}], 'path': 'ndarray_time=1600594684633122.0'}]
    
    for i in range(n):
        label = results[0]['data'][i]['label'] #mask status
        x1 = int(results[0]['data'][i]['left']) #coordinates
        y1 = int(results[0]['data'][i]['top'])
        x2 = int(results[0]['data'][i]['right'])
        y2 = int(results[0]['data'][i]['bottom'])
        rect = [x1,y1,x2,y2]
        coo_list.append(rect)
        label_list.append(label)
        
    print(coo_list, label_list)
    return coo_list, label_list

def cut_mask(frame, rect):
	
    x1 = rect[0]
    y1 = rect[1]
    x2 = rect[2]
    y2 = rect[3]
    y2_0 = y2-int((y2-y1)/1.8) #face is cut in half
    cut_img = frame[y1:y2_0, x1:x2]
    if x1 <= 0 or y1<= 0:
        return None
    else:
        return cv.cvtColor(cut_img, cv.COLOR_BGR2GRAY)
    

def predict(frame, rect):
    eye = cut_mask(frame, rect)
    if eye is not None:
        #Predict face
        results = face_recognizer.predict(eye)
        print(results[0])
        print(results[1])
        #Confidence threshold
        confi = results[1]
        if results[1] < 70:
            label_text = face_recognizer.getLabelInfo(results[0])
        else:
            label_text = 'stranger'
        return confi, label_text
    else:
        return 1000, 'not whole face'    

def draw_rectangle(img, rect):
    x1 = int(rect[0])
    y1 = int(rect[1])
    x2 = int(rect[2])
    y2 = int(rect[3])
    cv.rectangle(img, (x1, y1), (x2, y2), (128, 128, 0), 2)

def draw_text(img, text, x,y):
    cv.putText(img, text, (x, y), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

cap = cv.VideoCapture(0, cv.CAP_DSHOW)
url = "demo.mp4"
cap.open(url)


while True:
    ret, frame = cap.read()
    rect, label = detect_mask(frame) #rect is list of coordinates
    
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    
    for i in range(len(rect)): #number of people in frame = len(rect)
        draw_rectangle(frame, rect[i])
        draw_text(frame, label[i],rect[i][0],rect[i][1])
        if face_recognizer != 0:
            confi , name_label = predict(frame, rect[i])
            if (confi <= 70):
                draw_text(frame, "1683", rect[i][2],rect[i][3])
                sql = "REPLACE INTO child (info_id, attendance, date1, entry_time, exit_time, mask_status) VALUES (%s, %s, CURDATE(), %s,NULL, %s)"
                val = (name_label, "PRESENT", current_time, label[i])
                mycursor.execute(sql, val)
                mydb.commit()
                   
    cv.imshow('mask detction', frame)
    if cv.waitKey(3) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()