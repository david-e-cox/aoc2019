#!/usr/bin/python3

import itertools

def runProgram(mem,ptr,phaseSet,inputValue):
    # Parameter Length for each opCode
    pLength=[-1,3,3, 1,1, 2,2, 3,3 ]

    #Initialize
    done=False
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
            else:
                Param[i]=mem[ptr+i+1]
                
        # Execute instructions
        if (inst==1): # Add
            mem[Paddr[2]] = Param[0]+Param[1]

        elif (inst==2): # Multiply
            mem[Paddr[2]] = Param[0]*Param[1]
            
        elif (inst==3): # Set Input
            if (not phaseSet):
                mem[Paddr[0]] = inputValue[0]
                phaseSet=1
            else:
                mem[Paddr[0]] = inputValue[1]
            
        elif (inst==4): # Write Output
            #print("Output is {0:d}".format(Param[0]))
            ptr+=pLength[inst]+1
            return([Param[0],mem,ptr,phaseSet])
            
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
    # The full machine state is the memory, the run-pointer and the phaseSet flag
    return([-1,mem,ptr,phaseSet])



# Read input file
f=open('input.txt');
inCode =[int(val) for val in f.read().split(',')];
f.close()

#inCode=[3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
#inCode=[3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]

#PART-A
phaseList=[0,1,2,3,4]
allPhase=itertools.permutations(phaseList)
bestGain=-1;
memory=[val for val in inCode]

for phase in list(allPhase):
    osig=0
    ptr=0;
    phaseSet=False
    for amp in range(0,5):
        out=runProgram(memory, ptr, phaseSet, [phase[amp],osig] )
        osig=out[0];
    #print("Final Out {0:d} {1:s}".format(osig,"".join(map(str,phase))))
    if osig>bestGain:
        bestGain=osig
        bestPhase=phase
print("Best Gain {0:d} with Phasing {1:s}".format(bestGain,"".join(map(str,bestPhase))))
print("Solution to Part A is {0:d}".format(bestGain))
print("")


# PART-B
#inCode=[3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
#inCode=[3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

# Initialize 
bestGain=-1
phaseList=[5,6,7,8,9]
allPhase=itertools.permutations(phaseList)

for phase in list(allPhase):
    # Initialize for each phase
    for amp in range(0,5):
        memory[amp]=[val for val in inCode]
    osig    =[0,0,0,0,0]
    haltMap =[0,0,0,0,0]
    ptr     =[0,0,0,0,0]
    phaseSet=[0,0,0,0,0]
    inMap   =[4,0,1,2,3]
    done=False
    while (not done):
        for amp in range(0,5):
            out=runProgram(memory[amp],ptr[amp],phaseSet[amp], [phase[amp],osig[inMap[amp]]])
            # Only update outputs from non-halted amps
            if (out[0]>=0):
                osig[amp] = out[0]
                memory[amp]=[val for val in out[1]]
                ptr[amp]   = out[2]
                phaseSet[amp]=out[3]
            else:
                haltMap[amp]=1
                
            if osig[4]>bestGain:
                bestGain=osig[4]
                bestPhase=phase

        # Check if all processes have halted
        if "".join(map(str,haltMap))=="11111":
            done=True
    #print("{0:s}  {1:d}/{2:d}".format("".join(map(str,phase)),osig,bestGain))

print("Best Gain {0:d} with Phasing {1:s}".format(bestGain,"".join(map(str,bestPhase))))
print("Solution to Part B is {0:d}".format(bestGain))
