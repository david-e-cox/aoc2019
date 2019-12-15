#!/usr/bin/python3

import numpy as np
import itertools
import fractions

# Read input file


#moonPos = np.array([ [-1,0,2],[2,-10,-7],[4,-8,8],[3,5,-1]],dtype=int)
#moonPos  = np.array([ [-8,-10,0],[5,5,10],[2,-7,3],[9,-8,-3]],dtype=int)
moonPos = np.array([ [3,-6,6],[10,7,-9],[-3,-7,9],[-8,0,4]],dtype=int)
moonVel  = np.array([ [0,0,0],[0,0,0],[0,0,0],[0,0,0]] ,dtype=int)

stateHistory=set();
done=False
moonPos0=moonPos.copy()
moonVel0=moonVel.copy()
moonPeriodXYZ=np.zeros([3,1],dtype=int)

cnt=0;
doneSet=set()
while (not done):
    cnt+=1;
    for mSelf,mOther in itertools.product(range(4),range(4)):
        posDelta = moonPos[mSelf] - moonPos[mOther]
        moonVel[mSelf]+=[-1 if v else 0 for v in posDelta>0]
        moonVel[mSelf]+=[+1 if v else 0 for v in posDelta<0]

    moonPos+=moonVel
    potNrg=np.sum(np.abs(moonPos),axis=1)
    kinNrg=np.sum(np.abs(moonVel),axis=1)
    totNrg=np.sum(potNrg*kinNrg)
    if (cnt==1000):
        print("Solution to part A: Total Energy is {0:d}".format(totNrg))
    dPos=moonPos-moonPos0
    dVel=moonVel-moonVel0
    # Find period for dimensions x,y,z independently, must repeat for all moons
    for j in range(0,3):
        if np.max(np.abs(dPos[:,j]))==0 and np.max(np.abs(dVel[:,j]))==0 and j not in doneSet:
            moonPeriodXYZ[j]=cnt
            print("   State repeat at all moons, axis:{0:d}, cnt:{1:d}".format(j,cnt))
            doneSet.add(j)

    if len(doneSet)==3:
        print("Part B: with octave take least-common-multiple (lcm) of these \n  {}".format(moonPeriodXYZ.tolist()))
        done=True




