#!/usr/bin/python3
import curses


def runProgram(mem,ptrPair):
    # Problem specific variables
    programCtr=0;
    score=0
    cmd=[]
    moveDir=0
    lastX=20

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
            if programCtr<3:
                moveDir=0
            mem[Paddr[0]]=moveDir
            programCtr+=1
            #keyPress=stdscr.getkey()
            #if keyPress=='s':
            #    mem[Paddr[0]] = 0
            #elif keyPress=='d':
            #    mem[Paddr[0]] = moveDir
            #else:
            #    mem[Paddr[0]] = 0
                
        elif (inst==4): # Write Output
            #print("Output is {}".format(Param[0]))
            cmd.append(Param[0])
            if len(cmd)%3==0:
                if cmd[0]<0:
                    score=cmd[2]
                    
                #printScreen(cmd)
                if cmd[2]==4 and cmd[0]>=0:
                    moveDir=0
                    if  (cmd[0]-lastX)>0:
                        moveDir=1
                    elif(cmd[0]-lastX)<0:
                        moveDir=-1
                    lastX=cmd[0]
                cmd=[]
            
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
    return([score,-1,mem,[ptr,ptrRelative]])

def printScreen(cmdList):
    gameSymbol=[' ','#','+','T','o']
    if cmdList[0]>=0:
        pad.addch(cmdList[1],cmdList[0],gameSymbol[cmdList[2]])
        pad.refresh(0,0,5,5,30,50)
    else:
        score=str(cmdList[2])
        cnt=0
        for c in score:
            pad.addch(0,20+cnt,c)
            cnt+=1

## Read input file
f=open('input.txt');
inCode =[int(val) for val in f.read().split(',')];
f.close()

# Allocate empty memory, and restart memory
memory = [int(0) for val in range(0,8192)];
ptrPair=[0,2048]
cnt=0
for val in inCode:
    memory[cnt]=int(val)
    cnt+=1
#Quarters
memory[0]=2

# Uncomment to run visuals,
# Also uncomment printScreen() call

#stdscr=curses.initscr()
#pad = curses.newpad(40,60)

out=runProgram(memory, ptrPair)
#curses.endwin()
print("Solution to part B is {0:d}".format(out[0]))

