# Masked Face Attendance 
By Aparnam Saini, Issha Sethi, Karan Dogra, Kriti Singh, Rohini Sharma

# Objective

Our project aims to perform facial recognition even if the user is wearing a face mask by using the uncovered portion 
(portions which are not covered by the mask which is the upper half of the face) of their faces as to form our data set which is to be used for creating and updating the model 
the dataset for training the model. Also, we are using a texture based Facial recognition algorithm ie LBPH facial recognition algorithm for the task as it doesn’t focuses on 
the facial features such as. At the same time our objective is to mark the attendance even if an individual is wearing a face mask or not with no human interference.

# Prerequisites

1. [Paddlepaddle](https://www.paddlepaddle.org.cn/)
2. [Paddlehub](https://www.paddlepaddle.org.cn/hub/scene/maskdetect)
3. opencv-contrib-python
4. Flask
5. Numpy

# Hardware Requirements
1. Webcam with 720p output (can be hardwired or wireless)
2. Tablet Screen 
3. Server (In order to host the project)

# Setup Guide

1. Install Paddlepaddle (It is recommended to be done in Adminstrator mode)
<pre><code>pip install paddlepaddle</code></pre>
2. Install Paddlehub (It is recommended to be done in Adminstrator mode)
<pre><code>pip install paddlehub</code></pre>
3. Install Flask
<pre><code>pip install flask</code></pre>
4. Install MySQL-Connector
<pre><code>pip install mysql-connector-python</code></pre>
5. Uninstall opencv-python <b>Note: Make sure opencv-python is not present in the environment or the system, if it is present</b>
<pre><code>pip uninstall opencv-python</code></pre>
6. Install opencv-contrib-python
<pre><code>pip install opencv-contrib-python</code></pre>
7. Import the Database into the MySQL server(like Xampp)
<pre><code>SQL structure/attendance-main.sql</code></pre>
8. You can setup your IP and PORT for the system in app.py it is by-default set to 127.0.0.1:5000
<pre><code>app.run(IP = "ip_address", PORT = "pord_id")</code></pre>
9. Once App.py is running(via IDE or CMD), open a browser and search for the IP.

# Mask Detection
This is performed using PyramidBox-Lite is a lightweight model developed based on Baidu's paper. The model is based on the backbone network FaceBoxes. This is part of paddlehub 
module/package.It has a strong response to common problems such as illumination, mask occlusion, expression changes, scale changes and Robustness.This is used to get the 
coordinates of the faces within the frame obtained by the camera and status of the mask.

![Mask Detection Example](https://github.com/MIETDevelopers/P9_SocialDistMonitering_Karan_Kriti_Aparnam_Rohini_Issha/blob/7799715e35574e3272568d5d5ade443b86db29df/Sample%20Images/d.png?raw=true)
# Masked Face Recognition
Next step in our project will be the face recognition with the help of texture based face recognition algorithm/technique called LBPH face recognition algorithm.It stands for 
Local Binary Patterns Histogram algorithm. It is based on local binary operator. It is widely used in facial recognition due to its computational simplicity and discriminative 
power. It is best performed on a grayscale image which reduces the processing load and complexity. Continues comparison of adjacent pixels is performed to obtain a texture version of image. This image is divided  into a grid . Each box is stored into the model in the form of histograms. For our project only upper half of the face is used as lower part will be covered with a maskWhen a person comes in the frame for recognition this process is repeated and two sets of histograms are compared to get suitable result 
i.e. ID and corresponding confidence.


![Masked Face Recognition Example](https://github.com/MIETDevelopers/P9_SocialDistMonitering_Karan_Kriti_Aparnam_Rohini_Issha/blob/6001b75973e014c06e826b81f519f1312eb996ae/Sample%20Images/itled.png?raw=true)




