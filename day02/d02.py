#!/usr/bin/python3
from itertools import product

# Read input file
f=open('input.txt');
inCode =[int(val) for val in f.read().split(',')];
f.close()

# Initialize
solvedA=False
solvedB=False
Param=[0,0,0]

# Double loop, searching for noun and verb
for noun,verb in product(range(99),range(99)):
    done=False    # Initialize done flag
    ptr=0         # Reset Pointer
    mem = [val for val in inCode]   # Reset Memory

    # Substitue trial values into memory
    mem[1]=noun
    mem[2]=verb

    # Run instructions
    while (not done):
        inst=mem[ptr]
        Param[0]=mem[ptr+1]
        Param[1]=mem[ptr+2]
        Param[2]=mem[ptr+3]
    
        if (inst==1):
            mem[Param[2]] = mem[Param[0]]+mem[Param[1]]
            ptr+=4
        elif (inst==2):
            mem[Param[2]] = mem[Param[0]]*mem[Param[1]]
            ptr+=4
        else:
            # invalid program, move on
            break;

        # Handle halt condition
        if mem[ptr]==99:
            done=True

# Completed a trial, check for Part A and Part B solutions
    if ([noun,verb] == [12,2]):
        print("Solution to Part A is {0:d}".format(mem[0]))
        solvedA=True;
            
    if (mem[0] == 19690720):
        print("Solution to Part B is {0:d}".format(100*noun+verb))
        solvedB=True;

    if solvedA and solvedB:
        exit(0)
    

                        



    
        
        
        
    
