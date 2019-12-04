#!/usr/bin/python3

# prints a ascii map
# useful only for first demo problem
def printMap(S):
    cnt=0;
    for j in range(10,-10,-1):
        print("\n");
        for  i in range(-10,10):
            if "{0:d},{1:d}".format(i,j) in S:
                print('o ',end='')
                cnt+=1
            else:
                print('* ',end='')
    print("\n")
    

# Generate a set with the coordinates of all points along the map path
# "here" tracks corner points at direction changes
def genCoords(map):
    here=[0,0]
    coords=set();
    for move in map:
        dist=int(move[1:])+1;
        
        if (move[0]=='L'):
            for i in range(1,dist):
                coords.add("{0:d},{1:d}".format(here[0]-i, here[1]));
            here=[here[0]-i,here[1]];
        elif (move[0]=='R'):
            for i in range(1,dist):
                coords.add("{0:d},{1:d}".format(here[0]+i, here[1]));
            here=[here[0]+i,here[1]];
        elif (move[0]=='D'):
            for i in range(1,dist):
                coords.add("{0:d},{1:d}".format(here[0], here[1]-i));
            here=[here[0],here[1]-i];
        elif (move[0]=='U'):
            for i in range(1,dist):
                coords.add("{0:d},{1:d}".format(here[0], here[1]+i));
            here=[here[0],here[1]+i];
        else:
            printf("Something went wrong...");
            exit(-1)
    return(coords)


#Reusing Part-A, but not adding coordinates to a set.
#Just checking for target and if found returning the
#step count to that point, it's ugly but...
def steps2Target(map,targetPt):
    stepCnt=0
    here=[0,0]
    for move in map:
        dist=int(move[1:])+1;
        if (move[0]=='L'):
            for i in range(1,dist):
                stepCnt+=1;
                if targetPt == "{0:d},{1:d}".format(here[0]-i, here[1]):
                    return(stepCnt)
            here=[here[0]-i,here[1]];
        elif (move[0]=='R'):
            for i in range(1,dist):
                stepCnt+=1;
                if targetPt == "{0:d},{1:d}".format(here[0]+i, here[1]):
                    return(stepCnt)
            here=[here[0]+i,here[1]];
        elif (move[0]=='D'):
            for i in range(1,dist):
                stepCnt+=1;
                if targetPt == "{0:d},{1:d}".format(here[0], here[1]-i):
                    return(stepCnt)
            here=[here[0],here[1]-i];
        elif (move[0]=='U'):
            for i in range(1,dist):
                stepCnt+=1;
                if targetPt == "{0:d},{1:d}".format(here[0], here[1]+i):
                    return(stepCnt)            
            here=[here[0],here[1]+i];
        else:
            printf("Something went wrong...");
            exit(-1);
    return(-1)

# Read input file
f=open('input.txt');
mapA =[val for val in f.readline().strip().split(',')];
mapB =[val for val in f.readline().strip().split(',')];
f.close()

# Example Cases
#mapA = "R8,U5,L5,D3".split(',')
#mapB = "U7,R6,D4,L4".split(',')
#mapA = "R75,D30,R83,U83,L12,D49,R71,U7,L72".split(',')
#mapB = "U62,R66,U55,R34,D71,R55,D58,R83".split(',')
#mapA = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(',')
#mapB = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(',')

A=genCoords(mapA)
B=genCoords(mapB)
#printMap(A)
#printMap(B)

# Find all crossings
X=A.intersection(B)

# setup upper bounds
minDist =100000;
minSteps=100000;

# Check each wire crossing
for crossing in X:
    strList=crossing.split(',')

# For closest crossing to origin
    dist=abs(int(strList[0]))+abs(int(strList[1]))
    if dist<minDist:
        minDist=dist

# For least total (A+B) steps from origin
    stepTotal=steps2Target(mapA,crossing)+steps2Target(mapB,crossing)
    if stepTotal<minSteps:
        minSteps=stepTotal

print("Solution to Part A is {0:d}".format(minDist))
print("Solution to Part B is {0:d}".format(minSteps))




    



