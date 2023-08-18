import os
import shutil
import cv2

FOCUS_THRESHOLD = 2000
BLURRED_DIR = 'Check'

blur_count = 0
files = [f for f in os.listdir('.') if f.endswith('.jpg')]

try:
   os.makedirs(BLURRED_DIR)
except:
   pass

for infile in files:

   print('Processing file %s ...' % (infile))
   cv_image = cv2.imread(infile)
   
   face_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
   
   COMPET = face_cascade.detectMultiScale(cv_image, 2, 6)


   for C in COMPET:
      x, y, w, h = [ v for v in C ]
      cv2.rectangle(cv_image, (x,y), (x+w,y+h), (255,255,255))
      sub_face = cv_image[y:y+h, x:x+w]
        
   gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

   variance_of_laplacian = cv2.Laplacian(gray, cv2.CV_64F).var()

if variance_of_laplacian < FOCUS_THRESHOLD:
   shutil.move(infile, BLURRED_DIR)
   blur_count += 1
else:
   shutil.move(infile, OK_DIR)

print('Please review any flagged photos for accuracy. Processed %d files. Moved %d into QA, and %d look okay!' % (len(files), blur_count, len(files)-blur_count))