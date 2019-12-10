#!/usr/bin/python3

import itertools

def runProgram(mem,ptrPair,inputValue):
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
                mem[Paddr[0]] = inputValue

            
        elif (inst==4): # Write Output
            #print("Output is {0:d}".format(Param[0]))
            ptr+=pLength[inst]+1
            return([0,Param[0],mem,[ptr,ptrRelative]])
            
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
    return([-1,-1,mem,[ptr,ptrRelative]])



# Read input file
f=open('input.txt');
inCode =[int(val) for val in f.read().split(',')];
f.close()

#inCode = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
#inCode = [1102,34915192,34915192,7,4,7,99,0]
#inCode = [104,1125899906842624,99]

# Initialize with program and empty memory
memory = [int(0) for val in range(0,4096)];
cnt=0;
ptrPair=[0,0]
for val in inCode:
    memory[cnt]=int(val)
    cnt+=1

# Print solutions
outA=runProgram(memory, ptrPair,1)
print("Solution to Part A is {0:d}".format(outA[1]))
outB=runProgram(memory, ptrPair,2)
print("Solution to Part B is {0:d}".format(outB[1]))



