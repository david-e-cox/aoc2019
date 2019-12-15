#!/usr/bin/python3

def runProgram(mem,ptrPair,panelMap,robotXYD):
    # robotXYD vector is [X-coordiante, Y-coordinate, Direction, [GridSize] ]
    nGridX=robotXYD[3][0]
    nGridY=robotXYD[3][1]
    
    # First move is a paint move
    paintNow=True  # Toggle value for sequential output calls
    panelHistory=set()  # coordinate history, only length is needed
    
    # Parameter Length for each opCode
    pLength=[-1,3,3, 1,1, 2,2, 3,3, 1 ]

    #Initialize
    done=False

    # Absolute and Relative pointers from state
    ptr=ptrPair[0]
    ptrRelative=ptrPair[1]

    # Parse instructions and mode
    opCode="{0:05d}".format(mem[ptr])
    mode=[ int(m) for m in [opCode[2],opCode[1],opCode[0]] ]
    inst=int(opCode[3:])
    
    # Catch halt
    if (inst==99):
        done=True

    # Main execution loop    
    while (not done):

        # Intialize with values (used in debugging)
        Param=[-9999,-9999,-9999]
        Paddr=[-9999,-9999,-9999]
        jumpIteration=False
            
        for i in range(0,pLength[inst]):
            # Set params for position(0) or immediate(1) modes
            if mode[i]==0:
                Param[i]=mem[mem[ptr+i+1]]
                # Address is needed for output/writes
                Paddr[i]=mem[ptr+i+1]
            elif mode[i]==1:
                Param[i]=mem[ptr+i+1]
                Paddr[i]=ptr+i+1  # Unused?
            elif mode[i]==2:
                Param[i]=mem[mem[ptr+i+1]+ptrRelative]
                # Address is needed for output/writes
                Paddr[i]=mem[ptr+i+1]+ptrRelative
            else:
                print("Unrecongized Mode: {0:d}".format(mode[i]))

        # Execute instructions
        if (inst==1): # Add
            mem[Paddr[2]] = Param[0]+Param[1]

        elif (inst==2): # Multiply
            mem[Paddr[2]] = Param[0]*Param[1]
            
        elif (inst==3): # Set Input
            mem[Paddr[0]] = panelMap[robotXYD[0]+nGridX*robotXYD[1]]

        elif (inst==4): # Write Output
            # Paint and Move Robot, sequential commands 
            moveTable=[ (0,-1), (1,0), (0,1), (-1,0) ]
            if paintNow==True:
                panelHistory.add( (robotXYD[0],robotXYD[1]))
                paintNow=False
                if Param[0]==1:
                    panelMap[robotXYD[0]+nGridX*robotXYD[1]]=1
                elif Param[0]==0:
                    panelMap[robotXYD[0]+nGridX*robotXYD[1]]=0
                else:
                    printf("ERROR in Paint")
            else:  # Set direction and move
                paintNow=True
                if Param[0]==1:
                    robotXYD[2]+=1
                elif Param[0]==0:
                    robotXYD[2]-=1
                else:
                    printf("ERROR in Move")
                robotXYD[2]=robotXYD[2]%4
                robotXYD[0]+=moveTable[robotXYD[2]][0]
                robotXYD[1]+=moveTable[robotXYD[2]][1]
                
        elif (inst==5): #Jump if true
            if(Param[0]):
                ptr=Param[1]
                jumpIteration=True
                
        elif (inst==6): #Jump if false
            if( not Param[0]):
                ptr=Param[1]
                jumpIteration=True
                
        elif (inst==7): # <
            if (Param[0]<Param[1]):
                mem[Paddr[2]]=1
            else:
                mem[Paddr[2]]=0

        elif (inst==8): # =
            if (Param[0]==Param[1]):
                mem[Paddr[2]]=1
            else:
                mem[Paddr[2]]=0

        elif (inst==9): # relative base pointer update
            ptrRelative+=Param[0]

        # update run pointer
        if ( not jumpIteration):
            ptr+=pLength[inst]+1
            
        # update instructions and parameter modes
        opCode="{0:05d}".format(mem[ptr])
        mode=[ int(m) for m in [opCode[2],opCode[1],opCode[0]] ]
        inst=int(opCode[3:])
        
        # Handle halt condition
        if inst==99:
            done=True

    # Finished execution return state
    # The full machine state is the memory, the run-pointers
    return([len(panelHistory),-1,mem,[ptr,ptrRelative]])



# Read input file
f=open('input.txt');
inCode =[int(val) for val in f.read().split(',')];
f.close()

# Parameters, Part A
ptrPair=[0,0]
nGridX=180
nGridY=180
xStart=89
yStart=89

# Initialize with program and empty memory
panelMap = [int(0) for val in range(0,nGridX*nGridY)]
robotXYD = [xStart,yStart,0,[nGridX,nGridY]]
memory   = [int(0) for val in range(0,4096)]
cnt=0
for val in inCode:
    memory[cnt]=int(val)
    cnt+=1

outA=runProgram(memory, ptrPair, panelMap, robotXYD)
print("Solution to Part A is {0:d}".format(outA[0]))

# Parameters, Part B
ptrPair=[0,0]
nGridX=50
nGridY=8
xStart=5
yStart=1
panelMap = [int(0) for val in range(0,nGridX*nGridY)]
panelMap[xStart+yStart*nGridX]=1
robotXYD = [xStart,yStart,0,[nGridX,nGridY]]
memory   = [int(0) for val in range(0,4096)]
cnt=0
for val in inCode:
    memory[cnt]=int(val)
    cnt+=1

outB=runProgram(memory, ptrPair, panelMap, robotXYD)
# Visualize painted ship
print("Solution to Part B is:")
symbTable='^>v<'
for y in range(0,nGridY):
    for x in range (0,nGridX):
        if (panelMap[x+y*nGridX] == 1):
            print("#",end='')
        elif panelMap[x+y*nGridX]==0:
            print(".",end='')
    print()


