import cv2 as cv
import numpy as np
import paddlehub as hub


cap = cv.VideoCapture(0, cv.CAP_DSHOW)
#url = "http://192.168.29.110:8080/video"
#cap.open(url)

#create a detector
face_recognizer = cv.face.LBPHFaceRecognizer_create()

#Load model for mask detection 123 and then face model
module = hub.Module(name="pyramidbox_lite_server_mask")
face_landmark = hub.Module(name="face_landmark_localization")
face_landmark.set_face_detector_module(hub.Module(name="ultra_light_fast_generic_face_detector_1mb_320"))
#face_recognizer.read('model.yml')

#used to detect mask takes frame as input as dictionary gives out coordinate of the face and status mask
def detect_mask(frame):
    input_dict = {"data" : [frame]}
    results = module.face_detection(data=input_dict) #mask detection happens here
    
    try:
        label = results[0]['data'][0]['label']
    except IndexError:
        return (0,0,0,0), None
        
    # print(results) == [{'data': [{'label': 'NO MASK', 'confidence': 0.8142542243003845, 'top': 260, 'bottom': 480, 'left': 427, 'right': 637}], 'path': 'ndarray_time=1600594684633122.0'}]
    
    if results !=[]:
        label = results[0]['data'][0]['label'] #mask status
        x1 = int(results[0]['data'][0]['left']) #coordinates
        y1 = int(results[0]['data'][0]['top'])
        x2 = int(results[0]['data'][0]['right'])
        y2 = int(results[0]['data'][0]['bottom'])
        rect = (x1,y1,x2,y2) #rect is tuple
        return rect, label
    else:
        return (0,0,0,0), None
    
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
        print (x1,x2)
        return cv.cvtColor(cut_img, cv.COLOR_BGR2GRAY)
    

def user_list():
    label = 0
    while True:
        name = face_recognizer.getLabelInfo(label)
        if len(name) !=0:
            print ('label:', label, 'name:', name)
        else:
            name = input('input user'+str(label)+'name')
            face_recognizer.setLabelInfo(label, name)
            return label
        label +=1
    
    return None

while True:

    print("prepare data")
    faces = []
    labels = []
    label = user_list()
    for num in range(0,300):
        rec, frame = cap.read()
        rect ,mask_label = detect_mask(frame)
        cut_img = cut_mask(frame,rect)
        cv.imshow("f", frame)
        if cv.waitKey(1) == ord('q'):
            break
        if cut_img is None:
            cv.imwrite('dataset/0/'+str(num)+'.jpg', cut_img)
        
        #Add faces to the face list and add corresponding tags ie name or id
        faces.append(cut_img)
        labels.append(label)
    print("training..")
    if faces is None:
        print ('error:lose face')
    else:
        face_recognizer.update(faces, np.array(labels))
        face_recognizer.write('model.yml')
        print("SUCCESS!")     
        
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()      
print("Application Closed")