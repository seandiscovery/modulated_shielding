from tkinter import *
from tkinter import filedialog as fd
import csv
import re
import os
import matplotlib.pyplot as plt
import math
import numpy as np

#Allow user to select TOPAS csv file
testIn=Tk()
testIn.lift()
infile=fd.askopenfile(title="Please select TOPAS CSV file to normalize")
testIn.destroy()

infileStr = os.path.realpath(infile.name)

filePath, fileName = os.path.split(infileStr)
fileNameNoExt = os.path.splitext(fileName)[0]

#Specify the center of the bin containing the center of the source
#bin width/2 + source center in X, Y, Z
#source center for Y will actually be the tandem radius (0.3 cm) plus 0.5 cm
binWidthSim = 0.05 #bin width in cm
YOffsetSim = 0.04 #distance from tandem surface we want to normalize to in cm
TandemRadius = 0.3 #tandem radius in cm
SourceOffsetZ = -0.5 #source position set in simulation in cm

#calculate dose for a given dwell time
numHistories = 1000000000
dwellTime = 200.0
particlesPerSec = 370000000000


normalizationPoint = -0.05 - TandemRadius

SourceCenterZ = round(SourceOffsetZ + binWidthSim/2,2)
SourceCenterX = round(binWidthSim/2,2)
SourceCenterY = round(-YOffsetSim - TandemRadius + binWidthSim/2,2)

print(SourceCenterZ)
print(SourceCenterX)
print(SourceCenterY)

#Specify if the file to be run is for an unblocked source, and specify normalization value for other simulations 
unblocked = True
unblockedVal = 1.090801379177719e-05 #2.141184268111829e-06
#4.135480935474334e-07 Yt-169
#2.032628344750265e-06 Ir-192
#1.957781478267862e-06 v5 with Ir-192

#Define arrays for collecting various values for plots
allDataArray = []
YZArray_Y = []
YZArray_Z = []
YZArray_Dose = []
XProfile_X = []
XProfile_Dose = []

XYArray_X = []
XYArray_Y = []
XYArray_Dose = []

XProf_X = []
XProf_Dose = []

minValXY = -1.5
maxValXY = 1.5
minValYZ = -5
maxValYZ = -1

with open(infileStr, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    #start by getting the dose grid information and number of bins from the TOPAS header   
    for row in reader:
        
        if "#" in row[0]:
            
            if "X" in row[0]:
                doseGridXStr = row[0]
                doseGridX = (re.findall(r'[-+]?(?:\d*\.\d+|\d+)', doseGridXStr))
                binSizeX = float(doseGridX[1])
                numBinsX = float(doseGridX[0])
                lengthX = binSizeX*numBinsX
                CenterXBin = numBinsX/2
                centerXBin = -(numBinsX*binSizeX)/2 + (binSizeX*int(math.floor(numBinsX/2)))
                #print(centerXBin)
                
            if "Y" in row[0]:
                doseGridYStr = row[0]
                doseGridY = (re.findall(r'[-+]?(?:\d*\.\d+|\d+)', doseGridYStr))
                numBinsY = float(doseGridY[0])
                binSizeY = float(doseGridY[1])
                lengthY = binSizeY*numBinsY
                CenterYBin = numBinsY/2
                centerYBin = -(numBinsY*binSizeY)/2 + (binSizeY*int(math.floor(numBinsY/2)))
                
            if "Z" in row[0]:
                doseGridZStr = row[0]
                doseGridZ = (re.findall(r'[-+]?(?:\d*\.\d+|\d+)', doseGridZStr))
                numBinsZ = float(doseGridZ[0])
                binSizeZ = float(doseGridZ[1])
                lengthZ = binSizeZ*numBinsZ
                CenterZBin = numBinsZ/2
                centerZBin = -(numBinsZ*binSizeZ)/2 + (binSizeZ*int(math.floor(numBinsZ/2)))
            
        else:
            
            binCenterX_Left = -(numBinsX*binSizeX)/2 + (binSizeX*float(row[0]))
            binCenterX_Right = binCenterX_Left+binSizeX
            binCenterX = round((binCenterX_Left+binCenterX_Right)/2, 2)
            
            binCenterY_Left = -(numBinsY*binSizeY)/2 + (binSizeY*float(row[1]))
            binCenterY_Right = binCenterY_Left+binSizeY
            binCenterY = round((binCenterY_Left+binCenterY_Right)/2, 2)
            
            binCenterZ_Left = -(numBinsZ*binSizeZ)/2 + (binSizeZ*float(row[2]))
            binCenterZ_Right = binCenterZ_Left+binSizeZ
            binCenterZ = round((binCenterZ_Left+binCenterZ_Right)/2, 2)
            
            #-2.25 for z for tandem and 1.3 for normalization point for y
            #surface of tandem at 0.3
            if binCenterX == SourceCenterX:
                YZArray_Y.append(binCenterY)
                YZArray_Z.append(binCenterZ)
                YZArray_Dose.append(float(row[3]))
                
                if binCenterY == normalizationPoint and binCenterZ == SourceCenterZ:
                    if unblocked == True:
                        normalizationValue = float(row[3])
                    
                    else:
                        normalizationValue = unblockedVal

            if binCenterZ == SourceCenterZ:
                XYArray_X.append(binCenterX)
                XYArray_Y.append(binCenterY)
                #if np.sqrt(binCenterY*binCenterY + binCenterX*binCenterX) < TandemRadius:
                #    XYArray_Dose.append(float(0.0))
                #else:
                XYArray_Dose.append(float(row[3]))
                
                if binCenterY == SourceCenterY:
                    #XProf_X.append(binCenterX)
                    #XProf_Dose.append(float(row[3]))
            
                    XProfile_X.append(binCenterX)
                    XProfile_Dose.append(float(row[3]))
            
            if len(row) == 4:
                allDataArray.append([binCenterX, binCenterY, binCenterZ, row[3]])
            else:
                continue
        
print(normalizationValue)

for val in range(len(XYArray_Dose)):
    XYArray_Dose[val] = 100 * float(XYArray_Dose[val])/normalizationValue
    #XYArray_Dose[val] = float(XYArray_Dose[val])/10
    #XYArray_Dose[val] = (float(XYArray_Dose[val])/numHistories) * particlesPerSec * dwellTime * 100
    
for val2 in range(len(YZArray_Dose)):
    YZArray_Dose[val2] = 100 * float(YZArray_Dose[val2])/normalizationValue
    #YZArray_Dose[val2] = float(YZArray_Dose[val2])/10
    #YZArray_Dose[val2] = (float(YZArray_Dose[val2])/numHistories) * particlesPerSec * dwellTime * 100
    
for val3 in range(len(XProfile_Dose)):
    XProfile_Dose[val3] = 100 * float(XProfile_Dose[val3])/normalizationValue
    XProfile_X[val3] = float(XProfile_X[val3])*10

#with open('v4_test.csv', 'w', encoding='UTF8', newline='') as outfile:

#    writer = csv.writer(outfile)    
#    writer.writerow(['X', 'Dose'])
    
#    for val3 in range(len(XProfile_Dose)):
#        XProfile_Dose[val3] = 100 * float(XProfile_Dose[val3])/normalizationValue
        #XProf_Dose[val3] = float(XProf_Dose[val3])/10
        #XProf_Dose[val3] = (float(XProf_Dose[val3])/numHistories) * particlesPerSec * dwellTime * 100
#        writer.writerow([float(XProfile_X[val3]), XProfile_Dose[val3]])

#outfile.close()

#counts,xbins,ybins,image = plt.hist2d(XYArray_X, XYArray_Y, bins=int(numBinsX), weights=XYArray_Dose, cmap='jet', alpha=0, vmin = 100, vmax = 900)
#plt.contour(counts.transpose(), extent=[xbins[0], xbins[-1], ybins[0], ybins[-1]], linewidths=2, cmap='jet', levels=[50, 100, 250, 300, 400, 500, 600, 800, 900])
counts,xbins,ybins,image = plt.hist2d(XYArray_X, XYArray_Y, bins=int(numBinsX), weights=XYArray_Dose, cmap='jet', alpha=0, vmin = 20, vmax = 200)
plt.contour(counts.transpose(), extent=[xbins[0], xbins[-1], ybins[0], ybins[-1]], linewidths=2, cmap='jet', levels=[40, 70, 80, 90, 95, 100, 150])
plt.ylabel("Y (cm)")
plt.xlabel("X (cm)")
plt.xlim(minValXY, maxValXY)
plt.ylim(minValXY, maxValXY)
#plt.xlim(0, 0.45)
#plt.ylim(0, 0.45)
plt.title(fileNameNoExt)
plt.colorbar()
plt.show()


plt.scatter(XProfile_X, XProfile_Dose, marker='.')
#plt.scatter(ZProfile_Z, ZProfile_Dose, marker='.')
plt.ylim([0, 120])
plt.xlim([0, 10])
plt.show()

#counts2,xbins2,ybins2,image2 = plt.hist2d(YZArray_Z, YZArray_Y, bins=int(numBinsZ), weights=YZArray_Dose, cmap='jet', alpha=0.75, vmin = 70, vmax = 500)
#plt.contour(counts2.transpose(), extent=[xbins2[0], xbins2[-1], ybins2[0], ybins2[-1]], linewidths=2, cmap='jet', levels=[70, 80, 100, 150, 200, 450])
#plt.ylabel("Y (cm)")
#plt.xlabel("Z (cm)")
##plt.xlim(-5, 0)
#plt.ylim(minValXY, maxValXY)
#plt.title(fileNameNoExt)
#plt.colorbar()
#plt.show()

