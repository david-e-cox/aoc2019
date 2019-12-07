#!/usr/bin/python3

def runProgram(inCode,inputValue):
    # Reset Memory
    mem = [val for val in inCode]
    
    # Parameter Length for each opCode
    pLength=[-1,3,3, 1,1, 2,2, 3,3 ]

    #Initialize
    done=False
    ptr=0;
    opCode="{0:05d}".format(mem[ptr])
    mode=[ int(m) for m in [opCode[2],opCode[1],opCode[0]] ]
    inst=int(opCode[3:])

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
            mem[Paddr[0]] = inputValue
            print("Input is {0:d}".format(inputValue))
            
        elif (inst==4): # Write Output
            #output = mem[Param[0]]
            print("Output is {0:d}".format(Param[0]))
            
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
                
        else:
            # invalid program, move on
            return(-1);
        # update run pointer and handle halt condition
        if ( not jumpIteration):
            ptr+=pLength[inst]+1
            
        # update instructions and parameter modes
        opCode="{0:05d}".format(mem[ptr])
        mode=[ int(m) for m in [opCode[2],opCode[1],opCode[0]] ]
        inst=int(opCode[3:])
        
        #Handle halt condition
        if inst==99:
            done=True
#    print(mem)
    return(0)

# Read input file
f=open('input.txt');
inCode =[int(val) for val in f.read().split(',')];
f.close()

# Test
#inputValue=[3,8,9]
#inCode = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
#1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
#999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
#
#for i in inputValue:
#    runProgram(inCode,i)


# Read input file
f=open('input.txt');
inCode =[int(val) for val in f.read().split(',')];
f.close()

# Part-A
runProgram(inCode,1)
print("")
#Part-B
runProgram(inCode,5)



    
        
        
        
    
