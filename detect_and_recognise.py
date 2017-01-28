# USAGE
# python detect_and_recognise.py --training images/training --testing images/testing

# import the necessary packages
from pyimagesearch.localbinarypatterns import LocalBinaryPatterns
from sklearn.svm import LinearSVC
from imutils import paths
import argparse
import sys
import cv2
import cv2.cv as cv
from send_sms import send_sms
import re


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--training", required=True,
	help="path to the training images")
ap.add_argument("-e", "--testing", required=True, 
	help="path to the tesitng images")
args = vars(ap.parse_args())

# initialize the local binary patterns descriptor along with
# the data and label lists
desc = LocalBinaryPatterns(24, 8)
data = []
labels = []

# import pdb; pdb.set_trace()
# loop over the training images
for imagePath in paths.list_images(args["training"]):
	# load the image, convert it to grayscale, and describe it
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	hist = desc.describe(gray)

	# extract the label from the image path, then update the
	# label and data lists
	labels.append(imagePath.split("/")[-2])
	data.append(hist)

# train a Linear SVM on the data
model = LinearSVC(C=100.0, random_state=42)
model.fit(data, labels)

# Training code has ended here.

def recognise(args):
    # loop over the testing images
    for imagePath in paths.list_images(args["testing"]):
        # load the image, convert it to grayscale, describe it,
        # and classify it
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hist = desc.describe(gray)
        prediction = model.predict(hist)[0]

        # display the image and the prediction
        cv2.putText(image, prediction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1.0, (0, 0, 255), 3)
        cv2.imshow("Image", image)
        print prediction
        if re.search(r'adult', prediction, flags=re.I):
			message = "Recognised {person_type}".format(person_type=prediction)
			send_sms(message=message)
			exit(0)

# Detection code starts here.

min_size=(20,20)
image_scale=2
haar_scale=1.2
min_neighbors=2
haar_flags=0

def detect_and_draw(img,cascade):
    gray=cv.CreateImage((img.width,img.height),8,1)
    small_img=cv.CreateImage((cv.Round(img.width/image_scale),cv.Round(img.height/image_scale)),8,1)
    cv.CvtColor(img,gray,cv.CV_BGR2GRAY)
    cv.Resize(gray,small_img,cv.CV_INTER_LINEAR)
    cv.EqualizeHist(small_img,small_img)

    if(cascade):
        t=cv.GetTickCount()
        faces=cv.HaarDetectObjects(small_img,cascade,cv.CreateMemStorage(0),haar_scale,min_neighbors,haar_flags,min_size)
        t=cv.GetTickCount()-t
      
        scan_image = 1
        if faces:
            for ((x,y,w,h),n) in faces:
                pt1=(int(x*image_scale),int(y*image_scale))
                pt2=(int((x+w)*image_scale),int((y+h)*image_scale))
                sub_face = img[int(y*image_scale):int((y+h)*image_scale),int(x*image_scale):int((x+w)*image_scale)]
                cv.SaveImage('/home/pi/Documents/Recognise_test_sample/images/testing/'+str(scan_image)+".jpg",sub_face)
                cv.Rectangle(img,pt1,pt2,cv.RGB(255,0,0),3,8,0)
                scan_image = scan_image+1
               
        cv.ShowImage("video",img)
        cv.SaveImage("detected_faces.jpg",img)
        
       
                    
      
cascade=cv.Load("face.xml")
input_name=0
if input_name==0:
    capture=cv.CreateCameraCapture(int(input_name))
else:
    capture=None

cv.NamedWindow("video",1)
width=160*2
height=120*2

if width is None:
    width = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH))
else:
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)

if height is None:
    height=int(cv.GetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT))
else:
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height)

if capture:
    frame_copy=None
    while True:
        frame=cv.QueryFrame(capture)
        if not frame:
            cv.WaitKey(0)
            break
        if not frame_copy:
            frame_copy=cv.CreateImage((frame.width,frame.height),cv.IPL_DEPTH_8U,frame.nChannels)
        if frame.origin == cv.IPL_ORIGIN_TL:
                cv.Copy(frame,frame_copy)
        else:
            cv.Flip(frame,frame_copy,0)

        detect_and_draw(frame_copy,cascade)
        recognise(args)
        if cv.WaitKey(10) == 27 and cv2.waitKey(0) == 27:
            break
else:
    image = cv.LoadImage(input_name,1)
    detect_and_draw(image,cascade)
    cv.WaitKey(0)

cv.DestroyWindow("video")

# Detection code ends here.



