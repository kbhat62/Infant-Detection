import sys
import cv2.cv as cv
from optparse import OptionParser

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
        print "time taken for detection = %gms"%(t/(cv.GetTickFrequency()*1000.))
        scan_image = 1
        if faces:
            for ((x,y,w,h),n) in faces:
                pt1=(int(x*image_scale),int(y*image_scale))
                pt2=(int((x+w)*image_scale),int((y+h)*image_scale))
                sub_face = img[int(y*image_scale):int((y+h)*image_scale),int(x*image_scale):int((x+w)*image_scale)]
                cv.SaveImage(str("/home/pi/Documents/Recognise_test_sample/images/")+".jpg",sub_face)
                cv.Rectangle(img,pt1,pt2,cv.RGB(255,0,0),3,8,0)
                scan_image =scan_image+1

        cv.ShowImage("Input Image",img)
        cv.SaveImage("detected_faces.jpg",img)



cascade=cv.Load("face.xml")

image = cv.LoadImage("im.jpg",1)
detect_and_draw(image,cascade)

