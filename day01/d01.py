#!/usr/bin/python3
import numpy as np

# Read input file
f=open('input.txt');
inval =[int(val) for val in f.read().split()];
f.close()

# Calculate fuel required
totalFuel = int(0);
partAFuel = int(0);
for moduleMass in inval:
    fuelIncrement = int(moduleMass/3) - 2;
    partAFuel += fuelIncrement;
    totalFuel += fuelIncrement;
    while(fuelIncrement>0):
        fuelIncrement = int(fuelIncrement/3) -2;
        totalFuel += np.maximum(fuelIncrement,0);

# Print solution
print("Part A: Solution is {0:d}".format(partAFuel));
print("Part B: Solution is {0:d}".format(totalFuel));
