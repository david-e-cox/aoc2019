#!/usr/bin/python3

import numpy as np
import itertools
 
# Read input file
f=open('input.txt');
input =f.read().splitlines()
f.close()

Nx=len(input[0])
Ny=len(input)
str=""
for line in input:
    str+=line
map = [1 if c=='#' else 0 for c in str]

# Initialize sets
blockedDir=set()
asteroids =set()

# Create set with asteroid coordiantes as a tuple
for x,y in itertools.product(range(Nx),range(Ny)):
        if (map[y*Nx + x]):
            asteroids.add((x,y))

# Check each asteroid as an observing point for others, retain best
maxView=0
for obs in asteroids:
    for loc in asteroids:
        if obs != loc:
            blockedDir.add(int( np.arctan2(obs[0]-loc[0],obs[1]-loc[1]) *1000));
        if len(blockedDir)>maxView:
            maxView=len(blockedDir)
            bestLocation = obs
    blockedDir.clear()
print("Location:{0} has {1:d} asteroids in view".format(bestLocation,maxView))


# Part-B, remove asteroid with viewer/laser mount
asteroids.remove(bestLocation)

# Initialize sets and list
safeSet=set()
locList=[]
angList=[]
viable=[]
radius=[]
cnt=1

while (len(asteroids)>0):
    locList.clear()
    angList.clear()
    # calculate look angles to all asteroids which are not safe due to a prior same-angle block
    for a in asteroids:
        if a not in safeSet:
            locList.append(a)
            vec = (a[0]-bestLocation[0],a[1]-bestLocation[1])
            ang = int(1000*np.arctan2(vec[0],-vec[1])) # Clockwise from noon, milliRadians
            if (ang<0):
                ang+=int(1000*(2*np.pi))
            angList.append(ang)

    # As long as there is something not in safe set
    if len(locList):
        # Find minimum angle, include duplicate look angles
        minAngle = min(angList)
        ndx = [i for i,x in enumerate(angList) if x==minAngle]
        viable.clear()
        for x in ndx:
            viable.append(locList[x])
        # find closest of the duplicates
        radius.clear()
        for loc in viable:
            vector=(loc[0]-bestLocation[0],loc[1]-bestLocation[1])
            radius.append( vector[0]*vector[0] + vector[1]*vector[1] )
                 
        # blow up the close asteroid, remove from full set
        boom = viable[radius.index(min(radius))]
        if cnt in [1,2,3,10,20,50,100,199,200,201,299]:
            print("Removing {0} with blown count {1}".format(boom,cnt))
        asteroids.remove(boom)
        viable.remove(boom)
        
        # add remaining duplicates too safeSet, avoid  untill next-pass
        for x in viable:
            safeSet.add(x)
        # increment counter
        cnt+=1
    # everything left is in safe set, time for 2nd round
    else:
        safeSet.clear()

        













#NOPE::def targetPath(radius):
#NOPE::    mylist=[]
#NOPE::    # top 
#NOPE::    y=-radius
#NOPE::    for x in range(-radius,radius):
#NOPE::        mylist.append((x,y))
#NOPE::    # RightSide    
#NOPE::    x=radius
#NOPE::    for y in range(-radius,radius):
#NOPE::        mylist.append((x,y))
#NOPE::    # Bottom
#NOPE::    y=radius    
#NOPE::    for x in range(radius,-radius,-1):
#NOPE::        mylist.append((x,y))
#NOPE::    # LeftSide    
#NOPE::    x=-radius
#NOPE::    for y in range(radius,-(radius),-1):
#NOPE::        mylist.append((x,y))
#NOPE::
#NOPE::    # Spin around to start straight up
#NOPE::    rotate=[]
#NOPE::    for i in range(len(mylist)):
#NOPE::        cnt=(i+radius)%len(mylist)
#NOPE::        rotate.append(mylist[cnt])
#NOPE::    return(rotate)
#NOPE::

#NOPE::blownCnt=0
#NOPE::done=False
#NOPE::xymap=[]
#NOPE::radius=[]
#NOPE::angle=[]
#NOPE::iScale=10000
#NOPE::
#NOPE::asteroids.remove(bestLocation)
#NOPE::for loc in asteroids:
#NOPE::    xymap.append(loc)
#NOPE::
#NOPE::hitPoints=set()
#NOPE::safeSet=set()
#NOPE::viable=[]
#NOPE::radius=[]
#NOPE::arange=[0, iScale]
#NOPE::
#NOPE::while (not done):
#NOPE::    safeSet.clear()
#NOPE::    for aim in range(0,iScale):
#NOPE::        viable.clear()
#NOPE::        hitPoints.clear()
#NOPE::        aimRad=aim/iScale*2*np.pi
#NOPE::  #      print("{0:f}".format(aimRad*180/np.pi))
#NOPE::        for i in range(1,7):
#NOPE::            hitPoints.add(( i*int( int(1000*np.sin(aimRad))/1000) + bestLocation[0],
#NOPE::                           -i*int( int(1000*np.cos(aimRad))/1000) + bestLocation[1] ))
#NOPE::
#NOPE::        hitPoints.discard(bestLocation)
#NOPE::        
#NOPE::  #      print(hitPoints)
#NOPE::        for x in hitPoints:
#NOPE::            if (x in xymap) and (x not in safeSet):
#NOPE::                viable.append(x)
#NOPE::
#NOPE::        if viable:
#NOPE::            radius.clear()
#NOPE::            for loc in viable:
#NOPE::                vector=(loc[0]-bestLocation[0],loc[1]-bestLocation[1])
#NOPE::                radius.append( vector[0]*vector[0] + vector[1]*vector[1] )
#NOPE::                
#NOPE::            for i,x in enumerate(viable):
#NOPE::                print("{0} {1}".format(x,radius[i]))
#NOPE::
#NOPE::            boom = viable[radius.index(min(radius))]
#NOPE::            xymap.remove(boom)
#NOPE::            viable.remove(boom)
#NOPE::
#NOPE::            # add remaining inline to safe till next-pass list
#NOPE::            vecRef=(boom[0]-bestLocation[0], boom[1]-bestLocation[1])
#NOPE::            for x in viable:
#NOPE::                vec=(x[0]-bestLocation[0], x[1]-bestLocation[1])
#NOPE::                print("---Safe Check--- {} {}".format(vecRef,vec))
#NOPE::                if (vecRef[0]*vec[1] == vecRef[1]*vec[0]):
#NOPE::                    safeSet.add(x)
#NOPE::                    print("Safe {} for boom {}".format(x,boom))
#NOPE::
#NOPE::            # increment count
#NOPE::            blownCnt+=1
#NOPE::            if blownCnt in range(1,12):
#NOPE::                print("Removing {0} with blown count {1}".format(boom,blownCnt))
#NOPE::            # remove that asteroid from the list maps
#NOPE::            if blownCnt>250:
#NOPE::                done=True
#NOPE::                break
#NOPE::                
                
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
