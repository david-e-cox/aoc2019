#!/usr/bin/python3

# Input
inRange = [178416,676461]

# Determine if there are any repeated digits in pin
def checkRepeat(pin):
    s=str(pin)
    letterLast='0';
    for letter in s:
        if letter==letterLast:
            return True
        letterLast=letter;
    return False

# Determine if digits in pin are non-decreasing
def checkIncreasing(pin):
    s=str(pin)
    letterLast='0'
    for letter in s:
        if int(letter)<int(letterLast):
            return False
        letterLast=letter;
    return True

# Determine if there are one or more doubles amoung repeats
def checkDouble(pin):
    s=str(pin)
    #repeat[] is a histogram style repeat count, index by pin value
    repeat=[0,0,0,0,0,0,0,0,0,0]
    letterLast='0';
    for letter in s:
        if letter==letterLast:
            repeat[int(letter)]+=1;
        letterLast=letter;
    # if any doubles exist amoung repeats, return True
    for cnt in repeat:
        if cnt==1:
            return True
    return False

cntA=0
cntB=0
for pin in range(inRange[0],inRange[1]):
    # Check non-decreasing first, common to A/B parts
    if (checkIncreasing(pin)):
        # Check for part A conditions of repeats
        if (checkRepeat(pin)):
            cntA+=1
            # Check for part B conditions of existance of a double
            if (checkDouble(pin)):
                cntB+=1

print("Solution to Part A is {0:d}".format(cntA))
print("Solution to Part B is {0:d}".format(cntB))




    



