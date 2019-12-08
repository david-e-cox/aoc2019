#!/usr/bin/python3
import numpy as np

# Read input file
f=open('input.txt');
inImage = f.read().rstrip();
f.close()
nCols=25
nRows=6

#inImage = "0222112222120000"
#nCols=2
#nRows=2

def printImage(image):
    nRows=6
    nCols=25
    print("")
    for row in range(0,nRows):
        print("    ",end="")
        for col in range(0,nCols):
            if (image[row,col]==0):
                print(".",end="")
            elif (image[row,col]==1):
                print("8",end="")
        print("")

imageMap=np.zeros([nRows,nCols,int(len(inImage)/nRows/nCols)])
nLayers = int(len(inImage)/nRows/nCols)
cnt=0
for lay in range(0,nLayers):
    for row in range(0,nRows):
        for col in range(0,nCols):
              imageMap[row,col,lay]=inImage[cnt]
              cnt+=1
zMin=1000
for lay in range(0,nLayers):
    ndx=np.where(imageMap[:,:,lay]==0)
    zCount=len(ndx[0])
    if (zCount<zMin):
        zMin=zCount
        lMin=lay
#        print("{0:d} {1:d}".format(zMin,lMin))
ndx1=np.where(imageMap[:,:,lMin]==1)
ndx2=np.where(imageMap[:,:,lMin]==2)
print("Solution to Part A is {0:d}".format(len(ndx1[0])*len(ndx2[0])))

image=-1*np.ones([nRows,nCols],dtype='int32')

for row in range(0,nRows):
    for col in range(0,nCols):
        for lay in range(nLayers-1,-1,-1):
            if (imageMap[row,col,lay]==0):
                image[row,col]=0

            if (imageMap[row,col,lay]==1):
                image[row,col]=1

print("Solution to part B is")                
printImage(image)


    
        
        
        
    
