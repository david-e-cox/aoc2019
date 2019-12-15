#!/usr/bin/python3

import numpy as np
import itertools
import fractions

# Read input file


#moonPos = np.array([ [-1,0,2],[2,-10,-7],[4,-8,8],[3,5,-1] ])
moonPos  = np.array([ [-8,-10,0],[5,5,10],[2,-7,3],[9,-8,-3]],dtype=int)
#moonPos = np.array([ [3,-6,6],[10,7,-9],[-3,-7,9],[-8,0,4] ])
moonVel  = np.array([ [0,0,0],[0,0,0],[0,0,0],[0,0,0] ],dtype=int)

from math import gcd
from functools import reduce

with open('12.in') as f:
    data = f.readlines()


class Moon:
    def __init__(self, pos):
        x = int(pos.split('=')[1].split(',')[0])
        y = int(pos.split('=')[2].split(',')[0])
        z = int(pos.split('=')[3].split('>')[0])
        self.pos = [[x, 0], [y, 0], [z, 0]]
        self.period = [None, None, None]
        self.start = [[p, v] for p, v in self.pos]
        self.iter = 0

    def apply_gravity(self, other):
        for i in range(3):
            if self.pos[i][0] < other.pos[i][0]:
                self.pos[i][1] += 1
            elif self.pos[i][0] > other.pos[i][0]:
                self.pos[i][1] -= 1

    def update_posit(self):
        self.iter += 1
        for i in range(3):
            self.pos[i][0] += self.pos[i][1]

    def get_energy(self):
        potential = sum(abs(p[0]) for p in self.pos)
        kinetic = sum(abs(v[1]) for v in self.pos)
        return potential * kinetic


def _lcm(a, b):
    return (a * b) // gcd(a, b)


def lcm(lst):
    return reduce(_lcm, lst)


moons = []
for i, line in enumerate(data):
    moons.append(Moon(line.strip()))

lcms = dict()
while len(lcms) < 3:  # Part 2
# for _ in range(1000):  # Part 1
    # apply gravity
    for m in moons:
        for o in moons:
            if m == o:
                continue
            m.apply_gravity(o)

    # update position
    for m in moons:
        m.update_posit()

    for i in range(3):
        if moons[0].pos[i] == moons[0].start[i] and \
                moons[1].pos[i] == moons[1].start[i] and \
                moons[2].pos[i] == moons[2].start[i] and \
                moons[3].pos[i] == moons[3].start[i] and \
                i not in lcms:
            print('Period')
            l = lcm([m.iter for m in moons])
            print(l)
            lcms[i] = l

# print(sum(p.get_energy() for p in moons))  # Part 1
print(lcm(l for l in lcms.values()))  # Part 2
