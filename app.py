import cv2 as cv                      #to use computer vision ie opencv-contrib-python
import numpy as np                    #to work with array
import paddlehub as hub               #for mask and face detection
from datetime import datetime,timedelta         #to use current date and time
from flask import Flask, render_template, request, Response #add flask and features
import mysql.connector

#intialize Flask app
app = Flask(__name__)

#connect with MySQL database(use Xampp)
mydb=mysql.connector.connect(
		host = "localhost",
		user = "root",
		password = "",
		database = "attendance-main"
	)
mycursor=mydb.cursor(buffered=True)

#intialize a object to perform face recognition
face_recognizer = cv.face.LBPHFaceRecognizer_create()

#Load model for 1st for mask detection 2nd and 3rd for face detection and 4 then face model created by the User
module = hub.Module(name="pyramidbox_lite_server_mask")
face_landmark = hub.Module(name="face_landmark_localization")
face_landmark.set_face_detector_module(hub.Module(name="ultra_light_fast_generic_face_detector_1mb_320"))
face_recognizer.read('model.yml')

#used to detect mask status and face takes frame as input as dictionary gives out coordinate of the face and status mask
def detect_mask(frame):
    input_dict = {"data" : [frame]}
    results = module.face_detection(data=input_dict) #mask detection happens here
    #results == [{'data': [{'label': 'NO MASK', 'confidence': 0.8142542243003845, 'top': 260, 'bottom': 480, 'left': 427, 'right': 637}], 'path': 'ndarray_time=1600594684633122.0'}]
    coo_list = []
    label_list = [] 
    
    #to exception handling index out range caused when no person in view
    try:
        label = results[0]['data'][0]['label']
    except IndexError:
        coo_list.append([0,0,0,0])
        label_list.append(None)
        
    
    n = len(results[0]['data']) # n = number of people in frame
    
    print(len(results[0]['data'])) # print number of users in frame
    
    
    for i in range(n):
        label = results[0]['data'][i]['label'] #mask status
        x1 = int(results[0]['data'][i]['left']) #coordinate
        y1 = int(results[0]['data'][i]['top'])
        x2 = int(results[0]['data'][i]['right'])
        y2 = int(results[0]['data'][i]['bottom'])
        rect = [x1,y1,x2,y2]  #coordinates are put in rect in the form of list
        coo_list.append(rect) #coolist is nested list
        label_list.append(label)
        
    print(coo_list, label_list)
    return coo_list, label_list

#we take input as the frame and the coordinates of the face and gives out cropped frame which is gray scalled
def cut_mask(frame, rect):
    x1 = rect[0]
    y1 = rect[1]
    x2 = rect[2]
    y2 = rect[3]
    y2_0 = y2-int((y2-y1)/1.8) 
    cut_img = frame[y1:y2_0, x1:x2] #cut frame to get new_frame above the mask
    if x1 <= 0 or y1<= 0:
        return None
    else:
        return cv.cvtColor(cut_img, cv.COLOR_BGR2GRAY) #return in grayscale form
    

#face recognition occurs here; takes input as frame and coordinates of the full face
def predict(frame, rect):
    eye = cut_mask(frame, rect) #eye contains above mask image(grayscale)
    if eye is not None:
        #Predict face
        results = face_recognizer.predict(eye) 
        print(results[0]) # ID is indexed per face 0,1,2...
        print(results[1]) # confidence ie value = comparison of histograms from facemodel and current frame  
        #Confidence threshold
        confi = results[1]
        if results[1] < 70:
            label_text = face_recognizer.getLabelInfo(results[0]) #label text contain actual name like karan or 1605
        else:
            label_text = 'stranger'
        return confi, label_text
    else:
        return 1000, 'not whole face'    

#used to draw rectangles around the face in video output
def draw_rectangle(img, rect):
    x1 = int(rect[0])
    y1 = int(rect[1])
    x2 = int(rect[2])
    y2 = int(rect[3])
    cv.rectangle(img, (x1, y1), (x2, y2), (128, 128, 0), 2)

# Add text to video output
def draw_text(img, text, x,y):
    cv.putText(img, text, (x, y), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
 
# main for masked face attendance Entry    
def gen():
    #Video stream generator function.
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    #url = "/video" #will contain URL to the target Entery IP cam
    #cap.open(url)

    # Read until video is completed
    while(cap.isOpened()):
      # Capture frame-by-frame
        ret, frame = cap.read() #ret is boolean to check if any output is coming or not
        if ret == True:
            rect, label = detect_mask(frame) #rect is coo_list and label is label_list
    
            now = datetime.now() 
            current_time = now.strftime("%H:%M") # format of hr and min
            
            for i in range(len(rect)):
                draw_rectangle(frame, rect[i])
                draw_text(frame, label[i],rect[i][0],rect[i][1])
                if face_recognizer != 0:
                    confi , name_label = predict(frame, rect[i])
                    if (confi <= 70):
                        draw_text(frame, name_label, rect[i][2],rect[i][3])
                        draw_text(frame, "Marked", 0,50)
                        sql = "INSERT IGNORE INTO child (info_id, attendance, date1, entry_time, mask_status) VALUES (%s, %s, CURDATE(), %s, %s)"
                        val = (name_label, "PRESENT", current_time, label[i])
                        mycursor.execute(sql, val)
                        mydb.commit()
            
            frame = cv.resize(frame, (0,0), fx=1.4, fy=1.4) 
            img = cv.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
        else: 
            break

#main for masked face attendace Exit
def gen_exit():
    #Video streaming generator function.
    cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    #url = "/video" #will contain URL to the target Exit IP cam
    #cap.open(url)
    
    # Read until video is completed
    while(cap.isOpened()):
      # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            rect, label = detect_mask(frame)
    
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            
            for i in range(len(rect)):
                draw_rectangle(frame, rect[i])
                draw_text(frame, label[i],rect[i][0],rect[i][1])
                if face_recognizer != 0:
                    confi , name_label = predict(frame, rect[i])
                    if (confi < 70):
                        draw_text(frame, name_label, rect[i][2],rect[i][3])
                        draw_text(frame, "Marked", 0,50)
                        sql = "REPLACE INTO exit1 (info_id, date1, exit_time, mask_status) VALUES (%s,CURDATE(), %s, %s)"
                        val = (name_label, current_time, label[i])
                        mycursor.execute(sql, val)
                        mydb.commit()
            
            frame = cv.resize(frame, (0,0), fx=1.4, fy=1.4) 
            img = cv.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
        else: 
            break
    

#web portal on flask

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        signup = request.form
        username = signup['username']
        password = signup['password']
        mycursor.execute("select * from login where email='"+username+"' and password='"+password+"'")
        acc = mycursor.fetchall()
        if acc:
            pri = str(acc[0][4])
            if pri == 'Admin':
                return render_template("dashboard.html")
            else:
                id = str(acc[0][0])
                mycursor.execute("SELECT * FROM `child` WHERE info_id='"+id+"'ORDER BY date1 DESC")
                data = mycursor.fetchall()
                
                return render_template('studdash.html', data=data)
        else:
            return render_template("login.html")     
    mydb.commit()
    
    
@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        signup = request.form
        id = signup['id']
        username = signup['username']
        email = signup['email']
        password = signup['password']
        access = signup['access']
        dept = signup['dept']
        
        mycursor.execute("SELECT 1 FROM info WHERE id='"+id+"'")
        if mycursor.rowcount == 1:
            return render_template("signup.html", data = "User Already Exists!" )
        else:
            sql1 = "INSERT INTO info (id, username, email, department) VALUES (%s, %s, %s, %s);"
            val1 = (id, username,email, dept)
            mycursor.execute(sql1, val1)
            mydb.commit()
        
            sql2 = "INSERT INTO login (id, email, password, username, Access) VALUES (%s, %s, %s, %s, %s);"
            val2 = (id, email,password, username, access)
            mycursor.execute(sql2, val2)
            mydb.commit()

        return render_template("signup.html", data = "New User Added!")
    else:
        return render_template("signup.html")
        
    mydb.commit()

@app.route('/logout',methods=['GET'])
def logout():
	return render_template("login.html")

#Line graph for daily attendance trends
@app.route('/dashboard',methods=['GET'])
def dashboard():
    mycursor.execute("SELECT date1, COUNT(attendance) AS val FROM child GROUP BY date1 ORDER BY date1 ASC")
    list = mycursor.fetchall()
    x_list = [] #contains dates for graph X axis
    y_list = [] #contains list of total attendace for that day 

    for i in range(len(list)):
        x_list.append(list[i][0])
        y_list.append(list[i][1])
    
    line_labels = x_list
    line_values = y_list
    return render_template('dashboard.html', title='Graph for Attendance Marked Daily', max=20, labels=line_labels, values=line_values)

#Line graph for total attendance by the months through the years
@app.route('/month',methods=['GET'])
def month():
    mycursor.execute("SELECT MONTH(date1) as val1, COUNT(attendance) from child GROUP BY val1 order by val1")
    list = mycursor.fetchall()
    x_list = []
    y_list = []

    print(list[1][0])

    for i in range(len(list)):
        x_list.append(list[i][0])
        y_list.append(list[i][1])
    
    line_labels=x_list
    line_values=y_list
    return render_template('dashboard.html', title='Graph for Attendance Marked Monthly', max=20, labels=line_labels, values=line_values)


#Bar graph for mask violations per user
@app.route('/violate',methods=['GET'])
def violate():
    mycursor.execute("SELECT info_id, sum(case when mask_status = 'NO MASK' then 1 else 0 end) AS no_mask FROM child GROUP BY info_id ORDER BY info_id ASC")
    list = mycursor.fetchall()
    x_list = []
    y_list = []

    for i in range(len(list)):
        x_list.append(list[i][0])
        y_list.append(list[i][1])
    
    line_labels=x_list
    line_values=y_list
    return render_template('month.html', title='Mask Violations Per User', max=15, labels=line_labels, values=line_values)

#Bar graph for total Attendace per user
@app.route('/studgraph',methods=['GET'])
def studgraph():
    mycursor.execute("SELECT info_id, COUNT(attendance) FROM child GROUP BY info_id ORDER BY info_id ASC")
    list = mycursor.fetchall()
    x_list = []
    y_list = []

    print(list[1][0])
    for i in range(len(list)):
        x_list.append(list[i][0])
        y_list.append(list[i][1])
    
    line_labels=x_list
    line_values=y_list
    return render_template('month.html', title='Total Attendance Per User', max=15, labels=line_labels, values=line_values)

#table for user list
@app.route('/userList',methods=['GET'])
def userList():
    mycursor.execute("SELECT * FROM info")
    data = mycursor.fetchall()
    
    return render_template('userList.html', data=data)

#table for Daily attendace logs
@app.route('/dailylogs',methods=['GET']) 
def dailylogs():
    mycursor.execute("SELECT * FROM child ORDER BY date1 DESC, entry_time desc")
    data = mycursor.fetchall()
    
    return render_template('dailylogs.html', data = data )

#table for total attendace and violations per user
@app.route('/totalatt',methods=['GET'])
def totalatt():
    mycursor.execute("SELECT info_id, COUNT(attendance) AS attendance,sum(case when mask_status = 'NO MASK' then 1 else 0 end) AS no_mask FROM child GROUP BY info_id ORDER BY info_id ASC")
    data = mycursor.fetchall()
    
    return render_template('totalatt.html', data = data )

#table for entery exit times
@app.route('/entexit',methods=['GET'])
def entexit():
    mycursor.execute("SELECT child.info_id,child.date1,child.entry_time ,exit1.exit_time FROM child, exit1 WHERE child.info_id = exit1.info_id AND child.date1 = exit1.date1 ORDER BY 2,1")
    data = mycursor.fetchall()
    
    mycursor.execute("SELECT date1 FROM child")
    list = mycursor.fetchall()
    d = []
    for i in range(len(list)):
        d.append(list[i][0])

    date_set = set(d[0] + timedelta(x) for x in range((d[-1] - d[0]).days))

    holi = sorted(date_set - set(d))
    
    return render_template('entexit.html', data = data, holi = holi )


#for Entery live cam
@app.route('/livecam_enter',methods=['GET'])
def livecam_enter():
    #Video streaming home page.
    return render_template('livecam.html')
@app.route('/video_feed',methods=['GET'])
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag.
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')


#for Exit
@app.route('/livecam_exit',methods=['GET'])
def livecam_exit():
    #Video streaming home page.
    return render_template('livecamexit.html')
@app.route('/video_feed_exit',methods=['GET'])
def video_feed_exit():
    #Video streaming route. Put this in the src attribute of an img tag.
    return Response(gen_exit(),mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(debug=True)
#app.run() #In order to use the live stream functionality properly you have to give IP and port of the HOST server
