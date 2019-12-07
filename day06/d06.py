#!/usr/bin/python2
# Using a library off the net, it's Python 2... 

from anytree import Node, RenderTree 

#orbitMap  = ["COM)B","B)C","C)D","D)E","E)F","B)G","G)H","D)I","E)J","J)K","K)L"]

f=open('input.txt')
orbitMap = f.read().split()
f.close()

earthMoon = [item.split(')') for item in orbitMap]

# Add central node, no parents
_COM=Node("_COM")

# Lvl set are the bodyies at current depth in the tree
# nextLvL is set of bodies at the next level
Lvl=set()
nextLvl=set();

# Build tree structure, level ordered to ensure parents exist first
Lvl.add("COM")
while (len(Lvl)):
    for pair in earthMoon:
        if pair[0] in Lvl:
            # Add this node with it's parent defined
            exec("_{1:s} = Node(\"_{1:s}\", parent=_{0:s})".format(pair[0],pair[1]),locals())
            nextLvl.add(pair[1])
    Lvl=nextLvl.copy()
    nextLvl.clear()


# count all ancestor lists to get full orbit count for each body
# then total for Part A
orbitCount=0
for pair in earthMoon:
    body=pair[1]
    list = [ node.name for node in eval("_{0:s}.ancestors".format(body))]
#    print("Body {0:s} has {1:d} orbits".format(body,len(list)))
    orbitCount += len(list);

print("Solution to Part A is {0:d}".format(orbitCount) );

# Create paths from YOU and SAN back to COM
upath = [node.name for node in _YOU.path ]
spath = [node.name for node in _SAN.path ]

# Reverse direction to start at end
upath.reverse()
spath.reverse()

# follow YOU path until a node is found in common with SAN path
cnt1=-1 # Bias to remove transfer at common node    
for node in upath:
    cnt1+=1;
    if node in spath:
        commonPoint=node
        break

# follow SAN path back to common node
cnt2=-1 # Bias to remove transfer at common node    
for node in spath:
    cnt2+=1
    if node==commonPoint:
        break
        
#print(upath)
#print(spath)
#print(commonPoint)

# Note, subtract 2 from path length to remove YOU->first parent and SAN->first parent
# moves, which don't count as orbital transfers
print("Solution to part B is {0:d}".format(cnt1+cnt2-2))










