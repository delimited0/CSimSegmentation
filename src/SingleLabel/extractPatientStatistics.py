import numpy as np
import os
import SimpleITK as sitk
import h5py
import torch.nn as nn
import numpy as np
import torch.optim as optim
import torch
import torch.nn.init
from torch.autograd import Variable
import operator
import SimpleITK as sitk

# path_patients = "/Users/kushaagragoyal/Desktop/Independent Study/nerveSeg/nerveh5"
# dict_patient_to_ones = {}

# patients = os.listdir(path_patients)
# for (idx,namepatient) in enumerate(patients):
# 	f=h5py.File(os.path.join(path_patients,namepatient))
# 	dataMR = f['dataMR'].value
# 	dataSeg = f['dataSeg'].value
# 	print ("Patient = ", namepatient)
# 	print ("Mean Value = ", np.mean(dataMR))
# 	print("Number of 1's = ", np.sum(dataSeg))
# 	print ("DataMR shape = ", dataMR.shape)
# 	dataSeg[dataSeg>1] = 1
# 	dict_patient_to_ones[namepatient] = np.sum(dataSeg==1)

# sorted_dict = sorted(dict_patient_to_ones.items(), key = operator.itemgetter(1))
# for item in sorted_dict:
# 	print (item)

ones_dict = {}
path_patients_2 = "/Users/kushaagragoyal/Desktop/Independent Study/nerveSeg/labels/"
patients = os.listdir(path_patients_2)
for (idx,namepatient) in enumerate(patients):
	if(namepatient[0] != 'N'):
		continue
	labelOrg=sitk.ReadImage(path_patients_2 + namepatient)
	labelimg=sitk.GetArrayFromImage(labelOrg)
	print ("labelimg size = ", labelimg.shape)
	labelimg[labelimg > 1] = 1
	w,h,d = labelimg.shape
	ones_dict[namepatient] = (np.sum(labelimg == 1),w*h*d,np.sum(labelimg == 1)*1.0/(w*h*d))
sorted_dict = sorted(ones_dict.items(), key = operator.itemgetter(1))
print ("Patient Name : Number of labelled pixels, Total Pixels, Ratio")
for item in sorted_dict:
	print (item)

## Plot the image ####
#labelOrg = sitk.ReadImage("/Users/kushaagragoyal/Desktop/Independent Study/nerveSeg/labels/NB_P045 FN.nii.gz")
#labelimg = sitk.GetArrayFromImage(labelOrg)
#print(labelimg.shape)
#points = np.where(labelimg>0)
#x_point = list(points[1])
#y_point = list(points[2])
#z_point = list(points[0])
#x_point.append(512)
#x_point.append(0)
#y_point.append(0)
#y_point.append(512)
#z_point.append(0)
#z_point.append(481)

#for i in range(labelimg.shape[0]):
#	for j in range(labelimg.shape[1]):
#		for k in range(labelimg.shape[2]):
#			if(labelimg[i][j][k] > 0):
#				x_point.append(i)
#				y_point.append(j)
#				z_point.append(k)
#	print ("I = ", i)

#from matplotlib import pyplot
#from mpl_toolkits.mplot3d import Axes3D
#import random

#print ("HERE")

#fig = pyplot.figure()
#ax = Axes3D(fig)

#ax.scatter(x_point, y_point, z_point,c = 'r')
#print ("HERE TOO")
#pyplot.show()






