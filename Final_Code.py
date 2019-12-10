_#Importing packages
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
from pyimagesearch.transform import four_point_transform
from skimage.filters import threshold_local
import argparse
import imutils
from PIL import Image
from scipy.misc import imresize
from keras.models import Model
import h5py
import keras

datafile=open(r'C:\\Users\\BLUETECH\\Desktop\\ITSP\\DataRead.csv','a')
statusfile=open(r'C:\\Users\\BLUETECH\\Desktop\\ITSP\\FormStatus.txt','w')

def alphabet( path ):
	image = Image.open(path)
	image = image.convert('L')
	resized = imresize(image , (30,30))
	array = np.array(resized)
	array = 255-array
            array=array/255
            array=array[np.newaxis,:,:,np.newaxis]
	pred  = model_alphabets.predict(array)
	pred  = np.argmax(pred[0])
	return chr(pred+65)

def digit(path) :
	image = Image.open(path)
	image = image.convert('L')
	resized = imresize(image , (30,30))
	array = np.array(resized)
	array = 255-array
            array=array/255
            array=array[np.newaxis,:,:,np.newaxis]
	pred  = model_digits.predict(array)
	pred  = np.argmax(pred[0])
           return chr(pred+48)


nameCorr=[]      #1 for correct(all boxes found)
fNameCorr=[]
mobNoCorr=[]
pMobNoCorr=[]
nameFilled=[]       #0 for filled, 1 for empty
fNameFilled=[]
mobNoFilled=[]
pMobNoFilled=[]
allNames=[[]]
allFNames=[[]]
allMobNo=[[]]
allPMobNo=[[]]
formstatus=[]        # 0 for correct, 1 for manual, 2 for unfilled

model_alphabets = keras.models.load_model(r'C:\\Users\\BLUETECH\\Desktop\\ITSP\\document-scanner\\alphabet_classifier.h5')
model_digits = keras.models.load_model(r'C:\\Users\\BLUETECH\\Desktop\\ITSP\\document-scanner\\digits_classifier.h5')

#Opening from Google drive and storing in Scanned
search_dir = r"C:\Users\\BLUETECH\\Google Drive (1)\\Google Photos\2018"
os.chdir(search_dir)
files= filter(os.path.isfile,os.listdir(search_dir))
files=[os.path.join(search_dir,f)for f in files]
files.sort(key=lambda x:os.path.getmtime(x))

formstatus=np.zeros(len(files),dtype=int)
nameFilled=np.ones(len(files),dtype=int)
fNameFilled=np.ones(len(files),dtype=int)
pMobNoFilled=np.ones(len(files),dtype=int)
mobNoFilled=np.ones(len(files),dtype=int)
allNames=np.empty((len(files),20),dtype=np.unicode_)
allFNames=np.empty((len(files),20),dtype=np.unicode_)
allMobNo=np.empty((len(files),10),dtype=np.unicode_)
allPMobNo=np.empty((len(files),10),dtype=np.unicode_)

mo = 0
while (mo < len(files)):
	file1=files[len(files) - mo-1]
	image = cv2.imread(file1)
	ratio = image.shape[0] / 500.0
	orig = image.copy()
	image = imutils.resize(image, height = 500)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 75, 200)
	cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
	screenCnt=0

	for c in cnts:					# loop over the contours
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)

		if len(approx) == 4:
			screenCnt = approx
			break

	if len(approx) != 4:
		mo = mo+1
		continue
	cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
	warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
	warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
	T = threshold_local(warped, 11, offset = 10, method = "gaussian")
	warped = (warped > T).astype("uint8") * 255
	cv2.imwrite(r'C:\Users\\BLUETECH\\Desktop\\ITSP\\scanned\\' + str(mo) + '.png' ,warped)
	mo = mo+1

#Opening scanned files
search_dir = "C:\\Users\\BLUETECH\\Desktop\\ITSP\\scanned"
os.chdir(search_dir)
files= filter(os.path.isfile,os.listdir(search_dir))
files=[os.path.join(search_dir,f)for f in files]
nameCorr=[]
fNameCorr=[]
mobNoCorr=[]
pMobNoCorr=[]
for mo in range(len(files)):             #opens each file from scanned folder
    path="c:\\Users\\BLUETECH\\Desktop\\ITSP\\scanned\\"+str(mo)+".png"
    im = cv2.imread(path)
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blurred=cv2.GaussianBlur(imgray,(5,5),0)
    ret,thresh = cv2.threshold(blurred, 127,255,0)
    image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contour_square=[]
    name1=[]
    name2=[]
    fName1=[]
    fName2=[]
    mobNo=[]
    pMobNo=[]
    for i in contours:
        if (cv2.contourArea(i) >20000) and (cv2.contourArea(i) <40000) :
            contour_square.append(i)
    for i in range(len(contour_square)):            #divides into arrays
        x,y,w,h=cv2.boundingRect(contour_square[i])
        if(y<=700):
            name1.append(contour_square[i])
        elif(y<=850):
            name2.append(contour_square[i])
        elif(y<=1300):
            fName1.append(contour_square[i])
        elif(y<=1500):
            fName2.append(contour_square[i])
        elif(y<=1850):
            mobNo.append(contour_square[i])
        else:
            pMobNo.append(contour_square[i])
    name1=sorted(name1,key=lambda x:(tuple(x[x[:,:,0].argmin()][0])[0]))
    name2=sorted(name2,key=lambda x:(tuple(x[x[:,:,0].argmin()][0])[0]))
    fName1=sorted(fName1,key=lambda x:(tuple(x[x[:,:,0].argmin()][0])[0]))
    fName2=sorted(fName2,key=lambda x:(tuple(x[x[:,:,0].argmin()][0])[0]))
    mobNo=sorted(mobNo,key=lambda x:(tuple(x[x[:,:,0].argmin()][0])[0]))
    pMobNo=sorted(pMobNo,key=lambda x:(tuple(x[x[:,:,0].argmin()][0])[0]))
    name=[]
    fname=[]
    name=np.append(name1,name2)
    fName=np.append(fName1,fName2)

#stores cropped images with correct name
    if(len(name)==20):
        nameCorr.append(1)
        for i in range(len(name)):
            x,y,w,h=cv2.boundingRect(name[i])
            crop_img=im[y+5:y+h-3,x+5:x+w-5]
            cv2.imwrite(r'C:\Users\\BLUETECH\\Desktop\\ITSP\\cropped\\' + 'file' +str(mo) + "_" + 'name_'+str(i) + '.png',crop_img)
    else:
        nameCorr.append(0)
        formstatus[mo]=1
    if(len(fName)==20):
        fNameCorr.append(1)
        for i in range(len(fName)):
            x,y,w,h=cv2.boundingRect(fName[i])
            crop_img=im[y+5:y+h-3,x+5:x+w-5]
            cv2.imwrite(r'C:\Users\\BLUETECH\\Desktop\\ITSP\\cropped\\' + 'file' +str(mo) + "_" + 'fname_'+str(i) + '.png',crop_img)
    else:
        fNameCorr.append(0)
        formstatus[mo]=1
    if(len(mobNo)==10):
        mobNoCorr.append(1)
        for i in range(len(mobNo)):
            x,y,w,h=cv2.boundingRect(mobNo[i])
            crop_img=im[y+5:y+h-3,x+5:x+w-5]
            cv2.imwrite(r'C:\Users\\BLUETECH\\Desktop\\ITSP\\cropped\\' + 'file' +str(mo) + "_" + 'mobno_'+str(i) + '.png',crop_img)
    else:
        mobNoCorr.append(0)
        formstatus[mo]=1
    if(len(pMobNo)==10):
        pMobNoCorr.append(1)
        for i in range(len(pMobNo)):
            x,y,w,h=cv2.boundingRect(pMobNo[i])
            crop_img=im[y+5:y+h-3,x+5:x+w-5]
            cv2.imwrite(r'C:\Users\\BLUETECH\\Desktop\\ITSP\\cropped\\' + 'file' +str(mo) + "_" + 'pmobno_'+str(i) + '.png',crop_img)
    else:
        pMobNoCorr.append(0)
        formstatus[mo]=1

#checking for empty box
for mo in range(len(files)):
	if(nameCorr[mo]==1):
		nameEmptyCount=0
		for i in range(20):
			path='C:\\Users\\BLUETECH\\Desktop\\ITSP\\cropped\\file'+str(mo)+'_'+'name_'+str(i)+'.png'
			im=cv2.imread(path)
			imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
			resized=imresize(imgray,(30,30))
			count=0
			for k in range(0,30):
				for j in range(0,30):
					if resized[k][j]<255:
						count=count+1
			if(count<20):
				nameEmptyCount=nameEmptyCount+1
				allNames[mo][i]=' '
		if(nameEmptyCount==20):
			nameFilled[mo]=1
			formstatus[mo]=2
		else:
			nameFilled[mo]=0
	if(fNameCorr[mo]==1):
		fNameEmptyCount=0
		for i in range(20):
			path='C:\\Users\\BLUETECH\\Desktop\\ITSP\\cropped\\file'+str(mo)+'_'+'fname_'+str(i)+'.png'
			im=cv2.imread(path)
			imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
			resized=imresize(imgray,(30,30))
			count=0
			for k in range(0,30):
				for j in range(0,30):
					if resized[k][j]<255:
						count=count+1
			if(count<20):
				fNameEmptyCount=fNameEmptyCount+1
				allFNames[mo][i]=' '
		if(fNameEmptyCount==20):
			fNameFilled[mo]=1
			formstatus[mo]=2
		else:
			fNameFilled[mo]=0
	if(mobNoCorr[mo]==1):
		mobNoEmptyCount=0
		for i in range(10):
			path='C:\\Users\\BLUETECH\\Desktop\\ITSP\\cropped\\file'+str(mo)+'_'+'mobno_'+str(i)+'.png'
			im=cv2.imread(path)
			imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
			resized=imresize(imgray,(30,30))
			count=0
			for k in range(0,30):
				for j in range(0,30):
					if resized[k][j]<255:
						count=count+1
			if(count<20):
				mobNoEmptyCount=mobNoEmptyCount+1
				allMobNo[mo][i]=' '
		if(mobNoEmptyCount>0):
			mobNoFilled[mo]=1
			formstatus[mo]=2
		else:
			mobNoFilled[mo]=0
	if(pMobNoCorr[mo]==1):
		pMobNoEmptyCount=0
		for i in range(10):
			path='C:\\Users\\BLUETECH\\Desktop\\ITSP\\cropped\\file'+str(mo)+'_'+'pmobno_'+str(i)+'.png'
			im=cv2.imread(path)
			imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
			resized=imresize(imgray,(30,30))
			count=0
			for k in range(0,30):
				for j in range(0,30):
					if resized[k][j]<255:
						count=count+1
			if(count<20):
				pMobNoEmptyCount=pMobNoEmptyCount+1
				allPMobNo[mo][i]=' '
		if(pMobNoEmptyCount>0):
			pMobNoFilled[mo]=1
			formstatus[mo]=2
		else:
			pMobNoFilled[mo]=0

#reading cropped letters
for mo in range(len(files)):
	if (nameCorr[mo]==1 and nameFilled[mo]==0):
		for i in range(20):
			if(allNames[mo][i]!=' '):
				path=r'C:\\Users\\BLUETECH\\Desktop\\ITSP\\cropped\\file'+str(mo)+'_name_'+str(i)+'.png'
				allNames[mo][i]=alphabet(path)
	if(nameCorr[mo]==0):
		for i in range(20):
			allNames[mo][i]=' '
	if(fNameCorr[mo]==1 and fNameFilled[mo]==0):
		for i in range(20):
			if(allFNames[mo][i]!=' '):
				path=r'C:\\Users\\BLUETECH\\Desktop\\ITSP\\cropped\\file'+str(mo)+'_fname_'+str(i)+'.png'
				allFNames[mo][i]=alphabet(path)
	if(fNameCorr[mo]==0):
		for i in range(20):
			allFNames[mo][i]=' '
	if(mobNoCorr[mo]==1 and mobNoFilled[mo]==0):
		for i in range(10):
			path=r'C:\\Users\\BLUETECH\\Desktop\\ITSP\\cropped\\file'+str(mo)+'_mobno_'+str(i)+'.png'
			allMobNo[mo][i]=digit(path)
	if(mobNoFilled[mo]==1):
		for i in range(10):
			allMobNo[mo][i]=' '
	if(mobNoCorr[mo]==0):
		for i in range(10):
			allMobNo[mo][i]=' '
	if(pMobNoCorr[mo]==1 and pMobNoFilled[mo]==0):
		for i in range(10):
			path=r'C:\\Users\\BLUETECH\\Desktop\\ITSP\\cropped\\file'+str(mo)+'_pmobno_'+str(i)+'.png'
			allPMobNo[mo][i]=digit(path)
	if(pMobNoFilled[mo]==1):
		for i in range(10):
			allPMobNo[mo][i]=' '
	if(pMobNoCorr[mo]==0):
		for i in range(10):
			allPMobNo[mo][i]=' '

#writing into files
for mo in range(len(files)):
	for i in range(20):
		datafile.write(str(allNames[mo][i]))
	datafile.write(',')
	for i in range(20):
		datafile.write(str(allFNames[mo][i]))
	datafile.write(',')
	for i in range(10):
		datafile.write(str(allMobNo[mo][i]))
	datafile.write(',')
	for i in range(10):
		datafile.write(str(allPMobNo[mo][i]))
	datafile.write('\n')
	statusfile.write(str(formstatus[mo]))
	if(mo!=len(files)-1):
		statusfile.write(',')

statusfile.close()
datafile.close()
