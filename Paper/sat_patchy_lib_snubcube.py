#!/usr/bin/env python

"""
Crystal SAT specification adapted from Lukas, as a class


THIS ONE IS ADAPTED to FULLERENS!!!!

"Atoms" are "movable and rotatable", have 6 slots
"Positions" are fixed in the crystal, have 6 slots and bind according to spec
The problem has 2 parts:
A. find color bindings and colorings of position slots where each slot neightbors according to crystal model have
    colors that bind
B. find colorings of atoms s.t. all crystal positions are identical to (some) atom rotation. The atom definitions
    must not allow for bad 2-binds

indexes:
- colors:   1...c...#c (variable number)
- atoms:    1...a...#a (variable number)
- slots:    0...s...5=#s-1 (bindings places on atoms - 0,1,2 on one side, 3,4,5 on the other)
- position: 1...p...16=#p (number of positions in the crystal)
- rotation: 1...r...6=#r possible rotations of an atom
- condition: 1...d...#d conditions to avoid bad crystal
- qualification: 0..#q (0 for good crystal, one more for each bad one)

(boolean) variables:
- B(c1, c2): color c1 binds with c2 (n=#c*#c)
- F(p, s, c): slot s at position p has color c (n=#p*#s*#c)
- C(a, s, c): slot s on atom a has color c (n=#a*#s*#c)
- P(p, a, r): position p is occupied by atom a with rotation r (n=#p*#a*#r)

encoding functions:
- rotation(s, r) = slot that s rotates to under rotation r
"""


# VARS
#Na = 2     # number of atoms
#Nc = 8     # number of colors (4*Na)

# CONSTANTS
#Ns = 4      # number of slots
#Np = 8    # number of crytal positions
#Nr = 12      # number of possible rotations
#note that particle 0 has two interactions, through PBC, with particle 3, we can try to pecifhy that no two particles can interact through more than one patch?

#bindings_split = [[p for p in line.split() if p.isdigit()] for line in bindings_text]
#bindings = {(int(p1), int(s1)): (int(p2), int(s2)) for (p1, s1, p2, s2) in bindings_split}
#variables = {}


import json
import sys
import subprocess
import tempfile
import os

diogo_snubdodecahedron='''
Particle 0 patch 0 with Particle 8 patch 1
Particle 0 patch 1 with Particle 24 patch 0
Particle 0 patch 2 with Particle 18 patch 2
Particle 0 patch 3 with Particle 26 patch 4
Particle 0 patch 4 with Particle 4 patch 3
Particle 1 patch 0 with Particle 9 patch 1
Particle 1 patch 1 with Particle 25 patch 0
Particle 1 patch 2 with Particle 19 patch 2
Particle 1 patch 3 with Particle 27 patch 4
Particle 1 patch 4 with Particle 5 patch 3
Particle 2 patch 0 with Particle 4 patch 1
Particle 2 patch 1 with Particle 28 patch 0
Particle 2 patch 2 with Particle 12 patch 2
Particle 2 patch 3 with Particle 42 patch 4
Particle 2 patch 4 with Particle 8 patch 3
Particle 3 patch 0 with Particle 5 patch 1
Particle 3 patch 1 with Particle 29 patch 0
Particle 3 patch 2 with Particle 13 patch 2
Particle 3 patch 3 with Particle 43 patch 4
Particle 3 patch 4 with Particle 9 patch 3
Particle 4 patch 0 with Particle 28 patch 1
Particle 4 patch 2 with Particle 8 patch 2
Particle 4 patch 4 with Particle 14 patch 3
Particle 5 patch 0 with Particle 29 patch 1
Particle 5 patch 2 with Particle 9 patch 2
Particle 5 patch 4 with Particle 15 patch 3
Particle 6 patch 0 with Particle 14 patch 1
Particle 6 patch 1 with Particle 44 patch 0
Particle 6 patch 2 with Particle 10 patch 2
Particle 6 patch 3 with Particle 48 patch 4
Particle 6 patch 4 with Particle 28 patch 3
Particle 7 patch 0 with Particle 15 patch 1
Particle 7 patch 1 with Particle 45 patch 0
Particle 7 patch 2 with Particle 11 patch 2
Particle 7 patch 3 with Particle 49 patch 3
Particle 7 patch 4 with Particle 29 patch 3
Particle 8 patch 0 with Particle 24 patch 1
Particle 8 patch 4 with Particle 16 patch 3
Particle 9 patch 0 with Particle 25 patch 1
Particle 9 patch 4 with Particle 17 patch 3
Particle 10 patch 0 with Particle 51 patch 1
Particle 10 patch 1 with Particle 48 patch 0
Particle 10 patch 3 with Particle 44 patch 4
Particle 10 patch 4 with Particle 53 patch 3
Particle 11 patch 0 with Particle 50 patch 1
Particle 11 patch 1 with Particle 49 patch 2
Particle 11 patch 3 with Particle 45 patch 4
Particle 11 patch 4 with Particle 52 patch 3
Particle 12 patch 0 with Particle 52 patch 1
Particle 12 patch 1 with Particle 42 patch 0
Particle 12 patch 3 with Particle 28 patch 4
Particle 12 patch 4 with Particle 50 patch 3
Particle 13 patch 0 with Particle 53 patch 1
Particle 13 patch 1 with Particle 43 patch 0
Particle 13 patch 3 with Particle 29 patch 4
Particle 13 patch 4 with Particle 51 patch 3
Particle 14 patch 0 with Particle 44 patch 1
Particle 14 patch 2 with Particle 28 patch 2
Particle 14 patch 4 with Particle 38 patch 3
Particle 15 patch 0 with Particle 45 patch 1
Particle 15 patch 2 with Particle 29 patch 2
Particle 15 patch 4 with Particle 39 patch 3
Particle 16 patch 0 with Particle 58 patch 1
Particle 16 patch 1 with Particle 30 patch 0
Particle 16 patch 2 with Particle 24 patch 2
Particle 16 patch 4 with Particle 54 patch 3
Particle 17 patch 0 with Particle 59 patch 1
Particle 17 patch 1 with Particle 31 patch 0
Particle 17 patch 2 with Particle 25 patch 2
Particle 17 patch 4 with Particle 55 patch 3
Particle 18 patch 0 with Particle 36 patch 1
Particle 18 patch 1 with Particle 26 patch 0
Particle 18 patch 3 with Particle 24 patch 4
Particle 18 patch 4 with Particle 34 patch 3
Particle 19 patch 0 with Particle 37 patch 1
Particle 19 patch 1 with Particle 27 patch 0
Particle 19 patch 3 with Particle 25 patch 4
Particle 19 patch 4 with Particle 35 patch 3
Particle 20 patch 0 with Particle 38 patch 1
Particle 20 patch 1 with Particle 40 patch 0
Particle 20 patch 2 with Particle 22 patch 2
Particle 20 patch 3 with Particle 46 patch 4
Particle 20 patch 4 with Particle 44 patch 3
Particle 21 patch 0 with Particle 39 patch 1
Particle 21 patch 1 with Particle 41 patch 0
Particle 21 patch 2 with Particle 23 patch 2
Particle 21 patch 3 with Particle 47 patch 4
Particle 21 patch 4 with Particle 45 patch 3
Particle 22 patch 0 with Particle 55 patch 1
Particle 22 patch 1 with Particle 46 patch 0
Particle 22 patch 3 with Particle 40 patch 4
Particle 22 patch 4 with Particle 59 patch 3
Particle 23 patch 0 with Particle 54 patch 1
Particle 23 patch 1 with Particle 47 patch 0
Particle 23 patch 3 with Particle 41 patch 4
Particle 23 patch 4 with Particle 58 patch 3
Particle 24 patch 3 with Particle 30 patch 4
Particle 25 patch 3 with Particle 31 patch 4
Particle 26 patch 1 with Particle 36 patch 0
Particle 26 patch 2 with Particle 40 patch 2
Particle 26 patch 3 with Particle 38 patch 4
Particle 27 patch 1 with Particle 37 patch 0
Particle 27 patch 2 with Particle 41 patch 2
Particle 27 patch 3 with Particle 39 patch 4
Particle 30 patch 1 with Particle 58 patch 0
Particle 30 patch 2 with Particle 33 patch 2
Particle 30 patch 3 with Particle 56 patch 4
Particle 31 patch 1 with Particle 59 patch 0
Particle 31 patch 2 with Particle 32 patch 2
Particle 31 patch 3 with Particle 57 patch 4
Particle 32 patch 0 with Particle 34 patch 1
Particle 32 patch 1 with Particle 57 patch 0
Particle 32 patch 3 with Particle 59 patch 4
Particle 32 patch 4 with Particle 36 patch 3
Particle 33 patch 0 with Particle 35 patch 1
Particle 33 patch 1 with Particle 56 patch 0
Particle 33 patch 3 with Particle 58 patch 4
Particle 33 patch 4 with Particle 37 patch 3
Particle 34 patch 0 with Particle 57 patch 1
Particle 34 patch 2 with Particle 36 patch 2
Particle 34 patch 4 with Particle 56 patch 3
Particle 35 patch 0 with Particle 56 patch 1
Particle 35 patch 2 with Particle 37 patch 2
Particle 35 patch 4 with Particle 57 patch 3
Particle 36 patch 4 with Particle 40 patch 3
Particle 37 patch 4 with Particle 41 patch 3
Particle 38 patch 0 with Particle 40 patch 1
Particle 38 patch 2 with Particle 44 patch 2
Particle 39 patch 0 with Particle 41 patch 1
Particle 39 patch 2 with Particle 45 patch 2
Particle 42 patch 1 with Particle 52 patch 0
Particle 42 patch 2 with Particle 47 patch 2
Particle 42 patch 3 with Particle 54 patch 4
Particle 43 patch 1 with Particle 53 patch 0
Particle 43 patch 2 with Particle 46 patch 2
Particle 43 patch 3 with Particle 55 patch 4
Particle 46 patch 1 with Particle 55 patch 0
Particle 46 patch 3 with Particle 53 patch 4
Particle 47 patch 1 with Particle 54 patch 0
Particle 47 patch 3 with Particle 52 patch 4
Particle 48 patch 1 with Particle 51 patch 0
Particle 48 patch 2 with Particle 49 patch 0
Particle 48 patch 3 with Particle 50 patch 4
Particle 49 patch 1 with Particle 50 patch 0
Particle 49 patch 4 with Particle 51 patch 4
Particle 50 patch 2 with Particle 52 patch 2
Particle 51 patch 2 with Particle 53 patch 2
Particle 54 patch 2 with Particle 58 patch 2
Particle 55 patch 2 with Particle 59 patch 2
Particle 56 patch 2 with Particle 57 patch 2
'''

diogo_snubcube='''
Particle 0 patch 0 with Particle 13 patch 0
Particle 0 patch 1 with Particle 23 patch 2
Particle 0 patch 2 with Particle 19 patch 1
Particle 0 patch 3 with Particle 4 patch 4
Particle 0 patch 4 with Particle 5 patch 3
Particle 1 patch 0 with Particle 12 patch 0
Particle 1 patch 1 with Particle 20 patch 2
Particle 1 patch 2 with Particle 16 patch 1
Particle 1 patch 3 with Particle 5 patch 4
Particle 1 patch 4 with Particle 4 patch 3
Particle 2 patch 0 with Particle 15 patch 0
Particle 2 patch 1 with Particle 22 patch 2
Particle 2 patch 2 with Particle 18 patch 1
Particle 2 patch 3 with Particle 6 patch 4
Particle 2 patch 4 with Particle 7 patch 3
Particle 3 patch 0 with Particle 14 patch 0
Particle 3 patch 1 with Particle 21 patch 2
Particle 3 patch 2 with Particle 17 patch 1
Particle 3 patch 3 with Particle 7 patch 4
Particle 3 patch 4 with Particle 6 patch 3
Particle 4 patch 0 with Particle 19 patch 0
Particle 4 patch 1 with Particle 8 patch 2
Particle 4 patch 2 with Particle 12 patch 1
Particle 5 patch 0 with Particle 16 patch 0
Particle 5 patch 1 with Particle 9 patch 2
Particle 5 patch 2 with Particle 13 patch 1
Particle 6 patch 0 with Particle 18 patch 0
Particle 6 patch 1 with Particle 10 patch 2
Particle 6 patch 2 with Particle 14 patch 1
Particle 7 patch 0 with Particle 17 patch 0
Particle 7 patch 1 with Particle 11 patch 2
Particle 7 patch 2 with Particle 15 patch 1
Particle 8 patch 0 with Particle 22 patch 0
Particle 8 patch 1 with Particle 12 patch 2
Particle 8 patch 3 with Particle 19 patch 4
Particle 8 patch 4 with Particle 18 patch 3
Particle 9 patch 0 with Particle 21 patch 0
Particle 9 patch 1 with Particle 13 patch 2
Particle 9 patch 3 with Particle 16 patch 4
Particle 9 patch 4 with Particle 17 patch 3
Particle 10 patch 0 with Particle 23 patch 0
Particle 10 patch 1 with Particle 14 patch 2
Particle 10 patch 3 with Particle 18 patch 4
Particle 10 patch 4 with Particle 19 patch 3
Particle 11 patch 0 with Particle 20 patch 0
Particle 11 patch 1 with Particle 15 patch 2
Particle 11 patch 3 with Particle 17 patch 4
Particle 11 patch 4 with Particle 16 patch 3
Particle 12 patch 3 with Particle 22 patch 4
Particle 12 patch 4 with Particle 20 patch 3
Particle 13 patch 3 with Particle 21 patch 4
Particle 13 patch 4 with Particle 23 patch 3
Particle 14 patch 3 with Particle 23 patch 4
Particle 14 patch 4 with Particle 21 patch 3
Particle 15 patch 3 with Particle 20 patch 4
Particle 15 patch 4 with Particle 22 patch 3
Particle 16 patch 2 with Particle 20 patch 1
Particle 17 patch 2 with Particle 21 patch 1
Particle 18 patch 2 with Particle 22 patch 1
Particle 19 patch 2 with Particle 23 patch 1
'''

diogo_snubcube1='''
Particle 0 patch 1 with Particle 13 patch 1
Particle 0 patch 0 with Particle 23 patch 2
Particle 0 patch 2 with Particle 19 patch 0
Particle 0 patch 3 with Particle 4 patch 4
Particle 0 patch 4 with Particle 5 patch 3
Particle 1 patch 1 with Particle 12 patch 1
Particle 1 patch 0 with Particle 20 patch 2
Particle 1 patch 2 with Particle 16 patch 0
Particle 1 patch 3 with Particle 5 patch 4
Particle 1 patch 4 with Particle 4 patch 3
Particle 2 patch 1 with Particle 15 patch 1
Particle 2 patch 0 with Particle 22 patch 2
Particle 2 patch 2 with Particle 18 patch 0
Particle 2 patch 3 with Particle 6 patch 4
Particle 2 patch 4 with Particle 7 patch 3
Particle 3 patch 1 with Particle 14 patch 1
Particle 3 patch 0 with Particle 21 patch 2
Particle 3 patch 2 with Particle 17 patch 0
Particle 3 patch 3 with Particle 7 patch 4
Particle 3 patch 4 with Particle 6 patch 3
Particle 4 patch 1 with Particle 19 patch 1
Particle 4 patch 0 with Particle 8 patch 2
Particle 4 patch 2 with Particle 12 patch 0
Particle 5 patch 1 with Particle 16 patch 1
Particle 5 patch 0 with Particle 9 patch 2
Particle 5 patch 2 with Particle 13 patch 0
Particle 6 patch 1 with Particle 18 patch 1
Particle 6 patch 0 with Particle 10 patch 2
Particle 6 patch 2 with Particle 14 patch 0
Particle 7 patch 1 with Particle 17 patch 1
Particle 7 patch 0 with Particle 11 patch 2
Particle 7 patch 2 with Particle 15 patch 0
Particle 8 patch 1 with Particle 22 patch 1
Particle 8 patch 0 with Particle 12 patch 2
Particle 8 patch 3 with Particle 19 patch 4
Particle 8 patch 4 with Particle 18 patch 3
Particle 9 patch 1 with Particle 21 patch 1
Particle 9 patch 0 with Particle 13 patch 2
Particle 9 patch 3 with Particle 16 patch 4
Particle 9 patch 4 with Particle 17 patch 3
Particle 10 patch 1 with Particle 23 patch 1
Particle 10 patch 0 with Particle 14 patch 2
Particle 10 patch 3 with Particle 18 patch 4
Particle 10 patch 4 with Particle 19 patch 3
Particle 11 patch 1 with Particle 20 patch 1
Particle 11 patch 0 with Particle 15 patch 2
Particle 11 patch 3 with Particle 17 patch 4
Particle 11 patch 4 with Particle 16 patch 3
Particle 12 patch 3 with Particle 22 patch 4
Particle 12 patch 4 with Particle 20 patch 3
Particle 13 patch 3 with Particle 21 patch 4
Particle 13 patch 4 with Particle 23 patch 3
Particle 14 patch 3 with Particle 23 patch 4
Particle 14 patch 4 with Particle 21 patch 3
Particle 15 patch 3 with Particle 20 patch 4
Particle 15 patch 4 with Particle 22 patch 3
Particle 16 patch 2 with Particle 20 patch 0
Particle 17 patch 2 with Particle 21 patch 0
Particle 18 patch 2 with Particle 22 patch 0
Particle 19 patch 2 with Particle 23 patch 0
'''

diogo_snubcube2='''
Particle 0 patch 2 with Particle 13 patch 2
Particle 0 patch 1 with Particle 23 patch 0
Particle 0 patch 0 with Particle 19 patch 1
Particle 0 patch 3 with Particle 4 patch 4
Particle 0 patch 4 with Particle 5 patch 3
Particle 1 patch 2 with Particle 12 patch 2
Particle 1 patch 1 with Particle 20 patch 0
Particle 1 patch 0 with Particle 16 patch 1
Particle 1 patch 3 with Particle 5 patch 4
Particle 1 patch 4 with Particle 4 patch 3
Particle 2 patch 2 with Particle 15 patch 2
Particle 2 patch 1 with Particle 22 patch 0
Particle 2 patch 0 with Particle 18 patch 1
Particle 2 patch 3 with Particle 6 patch 4
Particle 2 patch 4 with Particle 7 patch 3
Particle 3 patch 2 with Particle 14 patch 2
Particle 3 patch 1 with Particle 21 patch 0
Particle 3 patch 0 with Particle 17 patch 1
Particle 3 patch 3 with Particle 7 patch 4
Particle 3 patch 4 with Particle 6 patch 3
Particle 4 patch 2 with Particle 19 patch 2
Particle 4 patch 1 with Particle 8 patch 0
Particle 4 patch 0 with Particle 12 patch 1
Particle 5 patch 2 with Particle 16 patch 2
Particle 5 patch 1 with Particle 9 patch 0
Particle 5 patch 0 with Particle 13 patch 1
Particle 6 patch 2 with Particle 18 patch 2
Particle 6 patch 1 with Particle 10 patch 0
Particle 6 patch 0 with Particle 14 patch 1
Particle 7 patch 2 with Particle 17 patch 2
Particle 7 patch 1 with Particle 11 patch 0
Particle 7 patch 0 with Particle 15 patch 1
Particle 8 patch 2 with Particle 22 patch 2
Particle 8 patch 1 with Particle 12 patch 0
Particle 8 patch 3 with Particle 19 patch 4
Particle 8 patch 4 with Particle 18 patch 3
Particle 9 patch 2 with Particle 21 patch 2
Particle 9 patch 1 with Particle 13 patch 0
Particle 9 patch 3 with Particle 16 patch 4
Particle 9 patch 4 with Particle 17 patch 3
Particle 10 patch 2 with Particle 23 patch 2
Particle 10 patch 1 with Particle 14 patch 0
Particle 10 patch 3 with Particle 18 patch 4
Particle 10 patch 4 with Particle 19 patch 3
Particle 11 patch 2 with Particle 20 patch 2
Particle 11 patch 1 with Particle 15 patch 0
Particle 11 patch 3 with Particle 17 patch 4
Particle 11 patch 4 with Particle 16 patch 3
Particle 12 patch 3 with Particle 22 patch 4
Particle 12 patch 4 with Particle 20 patch 3
Particle 13 patch 3 with Particle 21 patch 4
Particle 13 patch 4 with Particle 23 patch 3
Particle 14 patch 3 with Particle 23 patch 4
Particle 14 patch 4 with Particle 21 patch 3
Particle 15 patch 3 with Particle 20 patch 4
Particle 15 patch 4 with Particle 22 patch 3
Particle 16 patch 0 with Particle 20 patch 1
Particle 17 patch 0 with Particle 21 patch 1
Particle 18 patch 0 with Particle 22 patch 1
Particle 19 patch 0 with Particle 23 patch 1
'''

#some lattice definitions from John:
john_diamond = '''
Particle 0 patch 0 with Particle 4 patch 0
Particle 0 patch 1 with Particle 5 patch 0
Particle 0 patch 2 with Particle 6 patch 0
Particle 0 patch 3 with Particle 7 patch 0
Particle 1 patch 0 with Particle 4 patch 1
Particle 1 patch 1 with Particle 5 patch 1
Particle 1 patch 2 with Particle 6 patch 1
Particle 1 patch 3 with Particle 7 patch 1
Particle 2 patch 0 with Particle 4 patch 3
Particle 2 patch 1 with Particle 5 patch 3
Particle 2 patch 2 with Particle 6 patch 3
Particle 2 patch 3 with Particle 7 patch 3
Particle 3 patch 0 with Particle 4 patch 2
Particle 3 patch 1 with Particle 5 patch 2
Particle 3 patch 2 with Particle 6 patch 2
Particle 3 patch 3 with Particle 7 patch 2
'''

john_hexa = '''
Particle 0 patch 0 with Particle 2 patch 0
Particle 0 patch 1 with Particle 3 patch 0
Particle 0 patch 2 with Particle 3 patch 1
Particle 0 patch 3 with Particle 6 patch 0
Particle 1 patch 0 with Particle 2 patch 1
Particle 1 patch 1 with Particle 2 patch 3
Particle 1 patch 2 with Particle 3 patch 3
Particle 1 patch 3 with Particle 7 patch 0
Particle 2 patch 2 with Particle 4 patch 0
Particle 3 patch 2 with Particle 5 patch 0
Particle 4 patch 1 with Particle 6 patch 1
Particle 4 patch 2 with Particle 7 patch 1
Particle 4 patch 3 with Particle 7 patch 3
Particle 5 patch 1 with Particle 6 patch 3
Particle 5 patch 2 with Particle 6 patch 2
Particle 5 patch 3 with Particle 7 patch 2
'''

john_hexa_megalattice = '''
Particle 0 patch 0 with Particle 4 patch 0
Particle 0 patch 1 with Particle 7 patch 0
Particle 0 patch 2 with Particle 12 patch 0
Particle 0 patch 3 with Particle 23 patch 0
Particle 1 patch 0 with Particle 5 patch 0
Particle 1 patch 1 with Particle 6 patch 0
Particle 1 patch 2 with Particle 13 patch 0
Particle 1 patch 3 with Particle 22 patch 0
Particle 2 patch 0 with Particle 4 patch 1
Particle 2 patch 1 with Particle 6 patch 1
Particle 2 patch 2 with Particle 14 patch 0
Particle 2 patch 3 with Particle 20 patch 0
Particle 3 patch 0 with Particle 5 patch 1
Particle 3 patch 1 with Particle 7 patch 1
Particle 3 patch 2 with Particle 15 patch 0
Particle 3 patch 3 with Particle 21 patch 0
Particle 4 patch 2 with Particle 8 patch 0
Particle 4 patch 3 with Particle 18 patch 0
Particle 5 patch 2 with Particle 9 patch 0
Particle 5 patch 3 with Particle 19 patch 0
Particle 6 patch 2 with Particle 10 patch 0
Particle 6 patch 3 with Particle 17 patch 0
Particle 7 patch 2 with Particle 11 patch 0
Particle 7 patch 3 with Particle 16 patch 0
Particle 8 patch 1 with Particle 12 patch 1
Particle 8 patch 3 with Particle 14 patch 1
Particle 8 patch 2 with Particle 30 patch 0
Particle 9 patch 1 with Particle 13 patch 1
Particle 9 patch 3 with Particle 15 patch 1
Particle 9 patch 2 with Particle 31 patch 0
Particle 10 patch 1 with Particle 13 patch 3
Particle 10 patch 3 with Particle 14 patch 3
Particle 10 patch 2 with Particle 29 patch 0
Particle 11 patch 1 with Particle 12 patch 3
Particle 11 patch 3 with Particle 15 patch 3
Particle 11 patch 2 with Particle 28 patch 0
Particle 12 patch 2 with Particle 27 patch 0
Particle 13 patch 2 with Particle 26 patch 0
Particle 14 patch 2 with Particle 24 patch 0
Particle 15 patch 2 with Particle 25 patch 0
Particle 16 patch 1 with Particle 20 patch 1
Particle 16 patch 3 with Particle 23 patch 1
Particle 16 patch 2 with Particle 28 patch 1
Particle 17 patch 1 with Particle 21 patch 1
Particle 17 patch 3 with Particle 22 patch 1
Particle 17 patch 2 with Particle 29 patch 1
Particle 18 patch 1 with Particle 20 patch 3
Particle 18 patch 3 with Particle 22 patch 3
Particle 18 patch 2 with Particle 30 patch 1
Particle 19 patch 1 with Particle 21 patch 3
Particle 19 patch 3 with Particle 23 patch 3
Particle 19 patch 2 with Particle 31 patch 1
Particle 20 patch 2 with Particle 24 patch 1
Particle 21 patch 2 with Particle 25 patch 1
Particle 22 patch 2 with Particle 26 patch 1
Particle 23 patch 2 with Particle 27 patch 1
Particle 24 patch 2 with Particle 28 patch 2
Particle 24 patch 3 with Particle 30 patch 2
Particle 25 patch 2 with Particle 29 patch 2
Particle 25 patch 3 with Particle 31 patch 2
Particle 26 patch 2 with Particle 29 patch 3
Particle 26 patch 3 with Particle 30 patch 3
Particle 27 patch 2 with Particle 28 patch 3
Particle 27 patch 3 with Particle 31 patch 3
'''

john_ice0 = '''
Particle 0 patch 0 with Particle 6 patch 0
Particle 0 patch 1 with Particle 7 patch 0
Particle 0 patch 3 with Particle 10 patch 0
Particle 0 patch 2 with Particle 11 patch 0
Particle 1 patch 0 with Particle 4 patch 0
Particle 1 patch 1 with Particle 5 patch 0
Particle 1 patch 2 with Particle 8 patch 0
Particle 1 patch 3 with Particle 9 patch 0
Particle 2 patch 0 with Particle 6 patch 1
Particle 2 patch 1 with Particle 7 patch 1
Particle 2 patch 3 with Particle 10 patch 1
Particle 2 patch 2 with Particle 11 patch 1
Particle 3 patch 0 with Particle 4 patch 1
Particle 3 patch 1 with Particle 5 patch 1
Particle 3 patch 2 with Particle 8 patch 1
Particle 3 patch 3 with Particle 9 patch 1
Particle 4 patch 2 with Particle 5 patch 2
Particle 4 patch 3 with Particle 11 patch 2
Particle 5 patch 3 with Particle 10 patch 2
Particle 6 patch 2 with Particle 7 patch 2
Particle 6 patch 3 with Particle 9 patch 2
Particle 7 patch 3 with Particle 8 patch 2
Particle 8 patch 3 with Particle 9 patch 3
Particle 10 patch 3 with Particle 11 patch 3
'''

john_clathrate = '''
Particle 0 patch 0 with Particle 2 patch 0
Particle 0 patch 1 with Particle 3 patch 0
Particle 0 patch 2 with Particle 4 patch 0
Particle 0 patch 3 with Particle 5 patch 0
Particle 1 patch 0 with Particle 6 patch 0
Particle 1 patch 1 with Particle 7 patch 0
Particle 1 patch 3 with Particle 8 patch 0
Particle 1 patch 2 with Particle 9 patch 0
Particle 2 patch 1 with Particle 10 patch 0
Particle 2 patch 3 with Particle 18 patch 0
Particle 2 patch 2 with Particle 26 patch 0
Particle 3 patch 1 with Particle 11 patch 0
Particle 3 patch 3 with Particle 19 patch 0
Particle 3 patch 2 with Particle 27 patch 0
Particle 4 patch 1 with Particle 12 patch 0
Particle 4 patch 3 with Particle 20 patch 0
Particle 4 patch 2 with Particle 28 patch 0
Particle 5 patch 1 with Particle 13 patch 0
Particle 5 patch 3 with Particle 21 patch 0
Particle 5 patch 2 with Particle 29 patch 0
Particle 6 patch 1 with Particle 14 patch 0
Particle 6 patch 2 with Particle 22 patch 0
Particle 6 patch 3 with Particle 30 patch 0
Particle 7 patch 1 with Particle 15 patch 0
Particle 7 patch 2 with Particle 23 patch 0
Particle 7 patch 3 with Particle 31 patch 0
Particle 8 patch 1 with Particle 16 patch 0
Particle 8 patch 2 with Particle 24 patch 0
Particle 8 patch 3 with Particle 32 patch 0
Particle 9 patch 1 with Particle 17 patch 0
Particle 9 patch 2 with Particle 25 patch 0
Particle 9 patch 3 with Particle 33 patch 0
Particle 10 patch 1 with Particle 13 patch 1
Particle 10 patch 2 with Particle 24 patch 1
Particle 10 patch 3 with Particle 31 patch 1
Particle 11 patch 1 with Particle 12 patch 1
Particle 11 patch 2 with Particle 25 patch 1
Particle 11 patch 3 with Particle 30 patch 1
Particle 12 patch 2 with Particle 22 patch 1
Particle 12 patch 3 with Particle 33 patch 1
Particle 13 patch 2 with Particle 23 patch 1
Particle 13 patch 3 with Particle 32 patch 1
Particle 14 patch 1 with Particle 17 patch 1
Particle 14 patch 3 with Particle 20 patch 1
Particle 14 patch 2 with Particle 27 patch 1
Particle 15 patch 1 with Particle 16 patch 1
Particle 15 patch 3 with Particle 21 patch 1
Particle 15 patch 2 with Particle 26 patch 1
Particle 16 patch 3 with Particle 18 patch 1
Particle 16 patch 2 with Particle 29 patch 1
Particle 17 patch 3 with Particle 19 patch 1
Particle 17 patch 2 with Particle 28 patch 1
Particle 18 patch 2 with Particle 19 patch 2
Particle 18 patch 3 with Particle 33 patch 3
Particle 19 patch 3 with Particle 32 patch 3
Particle 20 patch 2 with Particle 21 patch 2
Particle 20 patch 3 with Particle 31 patch 3
Particle 21 patch 3 with Particle 30 patch 3
Particle 22 patch 3 with Particle 23 patch 3
Particle 22 patch 2 with Particle 29 patch 2
Particle 23 patch 2 with Particle 28 patch 2
Particle 24 patch 3 with Particle 25 patch 3
Particle 24 patch 2 with Particle 27 patch 2
Particle 25 patch 2 with Particle 26 patch 2
Particle 26 patch 3 with Particle 28 patch 3
Particle 27 patch 3 with Particle 29 patch 3
Particle 30 patch 2 with Particle 32 patch 2
Particle 31 patch 2 with Particle 33 patch 2
'''



john_doublediamond = '''
Particle 0 patch 3 with Particle 4 patch 3
Particle 0 patch 2 with Particle 5 patch 0
Particle 0 patch 1 with Particle 14 patch 0
Particle 0 patch 0 with Particle 15 patch 0
Particle 1 patch 2 with Particle 4 patch 2
Particle 1 patch 1 with Particle 5 patch 3
Particle 1 patch 3 with Particle 14 patch 3
Particle 1 patch 0 with Particle 15 patch 1
Particle 2 patch 0 with Particle 4 patch 0
Particle 2 patch 1 with Particle 5 patch 2
Particle 2 patch 2 with Particle 6 patch 2
Particle 2 patch 3 with Particle 7 patch 3
Particle 3 patch 2 with Particle 4 patch 1
Particle 3 patch 1 with Particle 5 patch 1
Particle 3 patch 3 with Particle 6 patch 1
Particle 3 patch 0 with Particle 7 patch 2
Particle 6 patch 0 with Particle 8 patch 1
Particle 6 patch 3 with Particle 9 patch 3
Particle 7 patch 0 with Particle 8 patch 0
Particle 7 patch 1 with Particle 9 patch 0
Particle 8 patch 3 with Particle 12 patch 3
Particle 8 patch 2 with Particle 13 patch 0
Particle 9 patch 2 with Particle 12 patch 2
Particle 9 patch 1 with Particle 13 patch 3
Particle 10 patch 0 with Particle 12 patch 0
Particle 10 patch 1 with Particle 13 patch 2
Particle 10 patch 2 with Particle 14 patch 2
Particle 10 patch 3 with Particle 15 patch 3
Particle 11 patch 2 with Particle 12 patch 1
Particle 11 patch 1 with Particle 13 patch 1
Particle 11 patch 3 with Particle 14 patch 1
Particle 11 patch 0 with Particle 15 patch 2
'''


john_fullerene = ''' 
Particle 0 patch 0 with Particle 3 patch 0
Particle 0 patch 2 with Particle 36 patch 1
Particle 0 patch 1 with Particle 48 patch 2
Particle 1 patch 0 with Particle 4 patch 0
Particle 1 patch 2 with Particle 37 patch 1
Particle 1 patch 1 with Particle 49 patch 2
Particle 2 patch 0 with Particle 5 patch 0
Particle 2 patch 2 with Particle 38 patch 1
Particle 2 patch 1 with Particle 50 patch 2
Particle 3 patch 1 with Particle 39 patch 2
Particle 3 patch 2 with Particle 51 patch 1
Particle 4 patch 1 with Particle 40 patch 2
Particle 4 patch 2 with Particle 52 patch 1
Particle 5 patch 1 with Particle 41 patch 2
Particle 5 patch 2 with Particle 53 patch 1
Particle 6 patch 0 with Particle 9 patch 0
Particle 6 patch 1 with Particle 42 patch 2
Particle 6 patch 2 with Particle 54 patch 1
Particle 7 patch 0 with Particle 10 patch 0
Particle 7 patch 1 with Particle 43 patch 2
Particle 7 patch 2 with Particle 55 patch 1
Particle 8 patch 0 with Particle 11 patch 0
Particle 8 patch 1 with Particle 44 patch 2
Particle 8 patch 2 with Particle 56 patch 1
Particle 9 patch 2 with Particle 45 patch 1
Particle 9 patch 1 with Particle 57 patch 2
Particle 10 patch 2 with Particle 46 patch 1
Particle 10 patch 1 with Particle 58 patch 2
Particle 11 patch 2 with Particle 47 patch 1
Particle 11 patch 1 with Particle 59 patch 2
Particle 12 patch 2 with Particle 24 patch 1
Particle 12 patch 1 with Particle 36 patch 2
Particle 12 patch 0 with Particle 37 patch 0
Particle 13 patch 2 with Particle 25 patch 1
Particle 13 patch 1 with Particle 37 patch 2
Particle 13 patch 0 with Particle 38 patch 0
Particle 14 patch 2 with Particle 26 patch 1
Particle 14 patch 0 with Particle 36 patch 0
Particle 14 patch 1 with Particle 38 patch 2
Particle 15 patch 1 with Particle 27 patch 2
Particle 15 patch 2 with Particle 39 patch 1
Particle 15 patch 0 with Particle 43 patch 0
Particle 16 patch 1 with Particle 28 patch 2
Particle 16 patch 2 with Particle 40 patch 1
Particle 16 patch 0 with Particle 44 patch 0
Particle 17 patch 1 with Particle 29 patch 2
Particle 17 patch 2 with Particle 41 patch 1
Particle 17 patch 0 with Particle 42 patch 0
Particle 18 patch 1 with Particle 30 patch 2
Particle 18 patch 2 with Particle 42 patch 1
Particle 18 patch 0 with Particle 49 patch 0
Particle 19 patch 1 with Particle 31 patch 2
Particle 19 patch 2 with Particle 43 patch 1
Particle 19 patch 0 with Particle 50 patch 0
Particle 20 patch 1 with Particle 32 patch 2
Particle 20 patch 2 with Particle 44 patch 1
Particle 20 patch 0 with Particle 48 patch 0
Particle 21 patch 2 with Particle 33 patch 1
Particle 21 patch 1 with Particle 45 patch 2
Particle 21 patch 0 with Particle 55 patch 0
Particle 22 patch 2 with Particle 34 patch 1
Particle 22 patch 1 with Particle 46 patch 2
Particle 22 patch 0 with Particle 56 patch 0
Particle 23 patch 2 with Particle 35 patch 1
Particle 23 patch 1 with Particle 47 patch 2
Particle 23 patch 0 with Particle 54 patch 0
Particle 24 patch 0 with Particle 40 patch 0
Particle 24 patch 2 with Particle 48 patch 1
Particle 25 patch 0 with Particle 41 patch 0
Particle 25 patch 2 with Particle 49 patch 1
Particle 26 patch 0 with Particle 39 patch 0
Particle 26 patch 2 with Particle 50 patch 1
Particle 27 patch 0 with Particle 46 patch 0
Particle 27 patch 1 with Particle 51 patch 2
Particle 28 patch 0 with Particle 47 patch 0
Particle 28 patch 1 with Particle 52 patch 2
Particle 29 patch 0 with Particle 45 patch 0
Particle 29 patch 1 with Particle 53 patch 2
Particle 30 patch 0 with Particle 52 patch 0
Particle 30 patch 1 with Particle 54 patch 2
Particle 31 patch 0 with Particle 53 patch 0
Particle 31 patch 1 with Particle 55 patch 2
Particle 32 patch 0 with Particle 51 patch 0
Particle 32 patch 1 with Particle 56 patch 2
Particle 33 patch 2 with Particle 57 patch 1
Particle 33 patch 0 with Particle 58 patch 0
Particle 34 patch 2 with Particle 58 patch 1
Particle 34 patch 0 with Particle 59 patch 0
Particle 35 patch 0 with Particle 57 patch 0
Particle 35 patch 2 with Particle 59 patch 1
'''


#Lukas Crystal SAT Solver, applied to tetrahedral particles
class LCSS:
    relsat_executable  = '/home/petr/projects/venice/FCC_and_HCP/simulation/KERN_FRENKEl/check_all/lukas_results/relsat/relsat'
    #relsat_executable  = '/home/petr/projects/venice/NEW_SAT/clathrate/relsat'
    #minisat_executable = '/home/petr/projects/venice/NEW_SAT/clathrate/minisat_static'
    minisat_executable = 'minisat' #'/home/petr/projects/venice/FCC_and_HCP/minisat/core/minisat_static'
    def __init__(self,Na=None,Nc=None,Np=None,Ns=5,Nr=1,rotations=None):
        #problem specification:
        self.Na = Na  # Number of distinct particle types for the solver
        self.Nc = Nc  # Number of colors in the whole system
        self.Np = Np  # Numper of particle positions in the crystal lattice
        self.Ns = Ns  # Number of patches on a single partile, defaul is 4
        self.Nr = Nr  # Number of distinct rotations (12)

        self.set_rotations(rotations)

        self.variables = {}
        self.basic_sat_clauses = None       #  string of a basic sat clause
        self.additional_sat_clauses = None  #  some additional conditions
        self.BC_varlen = None               #  the number of clauses that determine B and C

    def check_bindings(self):
        bindings = self.bindings
        pids = [x[0] for x in bindings.keys()] + [x[0] for x in bindings.values()]
        Np = 1 + max(pids)
        sids = [x[1] for x in bindings.keys()] + [x[1] for x in bindings.values()]
        Ns = 1 + max(sids)

        if self.Np is None:
            self.Np = Np
        elif self.Np != Np:
            raise IOError("Bindings text has different number of positions %d than imposed %d " % (self.Np,Np))

        if self.Ns is None:
            self.Ns = Ns
        elif self.Ns != Ns:
            raise IOError("Bindings text has different number of slots than imposed")

        return True



    def set_crystal_topology_from_text(self,bindings_text):
        '''
        Accepts text binding description, of format, per each line (each interacting pair only listed once):
        Particle 0 patch 0 with Particle 4 patch 0
        Particle 0 patch 1 with Particle 5 patch 0
        '''
        bindings_text = bindings_text.strip().replace(',', '').splitlines()
        bindings_split = [[p for p in line.split() if p.isdigit()] for line in bindings_text]
        bindings = {(int(p1), int(s1)): (int(p2), int(s2)) for (p1, s1, p2, s2) in bindings_split}

        self.bindings = bindings
        self.check_bindings()

    def generate_unique_topology(self,output):
        self.Na = self.Np
        self.Nc = self.Np*self.Ns

        outputfile = open(output,'w')
        for pid,patch in self.bindings.keys():
                qid, qpatch = self.bindings[ (pid,patch)]
                c1 = pid*self.Ns + patch 
                c2 = qid*self.Ns + qpatch
                outputfile.write('B(%d,%d)\n' % (c1,c2) )
                

        color = 0
        for pid in range(self.Na):
            for patch in range(self.Ns):
                outputfile.write('C(%d,%d,%d)\n' % (pid,patch,color  ) )
                color += 1
         


    def set_crystal_topology(self,bindings):
        '''
        Accepts an array of integer tuples bindings, of format [particle_id1,patch1,particle_id_2,patch2], where particle_id1 uses patch1 to bind to particle_id2 on patch2
        Each interacting pair is only to be listed once
        '''
        self.bindings = {(int(p1), int(s1)): (int(p2), int(s2)) for (p1, s1, p2, s2) in bindings}
        self.check_bindings()

    def construct_SAT_problem(self):
        pass


    def B(self,c1, c2):
        """ color c1 binds with c2 """
        if c2 < c1:
            c1, c2 = c2, c1
        assert 0 <= c1 <= c2 < self.Nc
        #print >> sys.stderr, 'B({c1},{c2})'.format(c1=c1, c2=c2)
        return self.variables.setdefault('B({c1},{c2})'.format(c1=c1, c2=c2), len(self.variables) + 1)



    def F(self, p, s, c):
        """ slot s at position p has color c """
        assert 0 <= p < self.Np
        assert 0 <= s < self.Ns
        assert 0 <= c < self.Nc
        return self.variables.setdefault('F({p},{s},{c})'.format(p=p, s=s, c=c), len(self.variables) + 1)


    def C(self,a, s, c):
        """ slot s on atom a has color c """
        assert 0 <= a < self.Na
        assert 0 <= s < self.Ns
        assert 0 <= c < self.Nc
        return self.variables.setdefault('C({a},{s},{c})'.format(a=a, s=s, c=c), len(self.variables) + 1)


    def P(self, p, a, r):
        """ position p is occupied by atom a with rotation r """
        assert 0 <= p < self.Np
        assert 0 <= a < self.Na
        assert 0 <= r < self.Nr
        return self.variables.setdefault('P({p},{a},{r})'.format(p=p, a=a, r=r), len(self.variables) + 1)


    def set_rotations(self,rotations=None):
        if rotations is None:
            self.rotations = {
                    0 : {  0 : 0, 1 : 1, 2 : 2, 3 : 3, 4 : 4} 
                    }
        else:
            self.rotations = rotations

    def rotation(self,s, r):
        """ slot that s rotates to under rotation r """
        assert 0 <= s < self.Ns
        assert 0 <= r < self.Nr
        # assert all(len(set(rotations[r].keys())) == Ns for r in rotations)
        # assert all(len(set(rotations[r].values())) == Ns for r in rotations)
        assert len(self.rotations) == self.Nr
        assert r in self.rotations
        assert s in self.rotations[r]
        return self.rotations[r][s]


    def check_settings(self):
        assert len(self.bindings) == (self.Np * self.Ns) / 2.0
        assert len(set(self.bindings.values())) == len(self.bindings)
        assert len(set(self.bindings) | set(self.bindings.values())) == self.Np * self.Ns
        assert min([a for a, _ in self.bindings] + [a for _, a in self.bindings] +
                [a for a, _ in self.bindings.values()] + [a for _, a in self.bindings.values()]) == 0
        assert max([a for a, _ in self.bindings] + [a for a, _ in self.bindings.values()]) == self.Np - 1
        assert max([a for _, a in self.bindings] + [a for _, a in self.bindings.values()]) == self.Ns - 1
        for s in range(self.Ns):
            for r in range(self.Nr):
                self.rotation(s, r)


    def _exactly_one(self,vs):
        """ returns a list of constraints implementing "exacly one of vs is true" """
        assert all(v > 0 for v in vs)
        assert len(vs) > 1
        constraints = [tuple(sorted(vs))]
        for v1 in sorted(vs):
            for v2 in sorted(vs):
                if v2 >= v1:
                    break
                constraints.append((-v1, -v2))
        assert len(set(constraints)) == (len(vs) * (len(vs)-1)) / 2 + 1
        return constraints


    def generate_constraints(self):
        # make sure B and C vars are first:
        for c1 in range(self.Nc):
            for c2 in range(self.Nc):
                self.B(c1, c2)
        for a in range(self.Na):
            for s in range(self.Ns):
                for c in range(self.Nc):
                    self.C(a, s, c)
        #print('c settings: Na=%d Nc=%d Ns=%d ' % (Na, Nc, Ns) )
        #print('c Last B and C var number: %s' % len(variables))
        self.basic_sat_clauses = []
        #self.basic_sat_clauses.append('c settings: Na=%d Nc=%d Ns=%d ' % (self.Na, self.Nc, self.Ns) )
        #self.basic_sat_clauses.append('c Last B and C var number: %s' % len(self.variables))
        self.BC_varlen = len(self.variables)
        constraints = []

        # BASIC THINGS:
        # - Legal color bindings:
        # "Each color has exactly one color that it binds to"
        # 	forall c1 exactly one c2 s.t. B(c1, c2)
        for c1 in range(self.Nc):
            constraints.extend(self._exactly_one([self.B(c1, c2) for c2 in range(self.Nc)]))
            #print >> sys.stderr, [B(c1, c2) for c2 in range(Nc) if c2 != c1]

        # - Legal atom slot coloring (unnecesay, implied by "Legal atom coloring in positions" and "Legal position
        #   slot coloring"):
        # "Each slot on every atom has exactly one color"
        #   forall a, forall s, exaclty one c s.t. C(a, s, c)
        for a in range(self.Na):
            for s in range(self.Ns):
                constraints.extend(self._exactly_one([self.C(a, s, c) for c in range(self.Nc)]))

        # ADD CRYSTAL and COLORS:
        # - Legal position slot coloring:
        # "Every position slot has exactly one color"
        # 	for all p, s exactly one c st. F(p, s, c)
        for p in range(self.Np):
            for s in range(self.Ns):
                constraints.extend(self._exactly_one([self.F(p, s, c) for c in range(self.Nc)]))

        # - Forms desired crystal:
        # "Specified binds have compatible colors"
        # 	forall (p1, s1) binding with (p2, s2) from crystal spec:
        # 		forall c1, c2: F(p1, s1, c1) and F(p2, s2, c2) => B(c1, c2)
        for (p1, s1), (p2, s2) in self.bindings.items():
            for c1 in range(self.Nc):
                for c2 in range(self.Nc):
                    constraints.append((-self.F(p1, s1, c1), -self.F(p2, s2, c2), self.B(c1, c2)))

        # - Legal atom placement in positions:
        # "Every position has exactly one atom placed there with exactly one rotation"
        #   forall p: exactly one a and r s.t. P(p, a, r)
        for p in range(self.Np):
            constraints.extend(self._exactly_one([self.P(p, a, r) for a in range(self.Na) for r in range(self.Nr)]))

        # - Legal atom coloring in positions:
        # "Given a place, atom and its rotation, the slot colors on the postion and (rotated) atom must be the same"
        #   for all p, a, r:
        #       P(p, a, r) => (forall s, c: F(p, s, c) <=> C(a, rotation(s, r), c))
        for p in range(self.Np):
            for a in range(self.Na):
                for r in range(self.Nr):
                    # forall part
                    for s in range(self.Ns):
                        for c in range(self.Nc):
                            s_rot = self.rotation(s, r)
                            constraints.append((-self.P(p, a, r), -self.F(p, s, c), self.C(a, s_rot, c)))
                            constraints.append((-self.P(p, a, r), self.F(p, s, c), -self.C(a, s_rot, c)))

        # OPTIONAL:
        # assign colors to all slots, if there are enough of them - MUCH FASTER
        #assert self.Na * self.Ns == self.Nc
        #c = 0
        #for a in range(self.Na):
        #    for s in range(self.Ns):
        #        constraints.append([self.C(a, s, c)])
        #        c += 1
        #assert c == self.Nc

        # symmetry breaking a little bit....
        #constraints.append([self.F(0, 0, 0)])
        #constraints.append([self.P(0, 0, 0)])

        self.basic_sat_clauses.extend(constraints)
        return constraints


    def output_cnf(self,constraints,out):
        """ Outputs a CNF formula """
        num_vars = max(self.variables.values())
        num_constraints = len(constraints)
        outstr = "p cnf %s %s\n" % (num_vars, num_constraints)
        out.write(outstr)
        #print("p cnf %s %s" % (num_vars, num_constraints))
        # print("c %s" % json.dumps(variables))
        for c in constraints:
            outstr = ' '.join([str(v) for v in c]) + ' 0\n'
            out.write(outstr)
        #return outstr


    def load_solution_from_lines(self,lines,maxvariable=None):
        """ loads solution from sat solution output in s string"""
        if len(lines) > 1:
            assert lines[0].strip() == 'SAT'
            satline = lines[1].strip().split()
        else:
            satline = lines[0].strip().split()

        #line = myinput.readline().strip()
        #assert line == 'SAT'
        sols = [int(v) for v in satline]
        assert sols[-1] == 0
        sols = sols[:-1]
        assert len(sols) <= len(self.variables)

        variable_names  = []
        for vname, vnum in sorted(self.variables.items()):
            if vnum > len(sols):
                break
            if maxvariable is not None and vnum > maxvariable:
                break
            if sols[vnum-1] > 0:
                variable_names.append(vname)

        return variable_names

    def add_constraints_from_vnames(self,vnames):
        constraints = []
        for vname in vnames:
            if vname not in self.variables:
                raise IOError("Trying to add variables that have not been defined, probably incompatible problem formulation?")
            constraints.append( self.variables[vname] )
        self.basic_sat_clauses.append(constraints)


    def convert_solution(self,myinput,output):
        """ loads solution from minisat sol in myinput handle, writes variable names to output """
        line = myinput.readline().strip()
        assert line == 'SAT'
        sols = [int(v) for v in myinput.readline().strip().split()]
        assert sols[-1] == 0
        sols = sols[:-1]
        assert len(sols) <= len(self.variables)

        for vname, vnum in sorted(self.variables.items()):
            if vnum > len(sols):
                break
            if sols[vnum-1] > 0:
                output.write(vname+'\n')

    def save_named_solution(self,solution,output,B=True,C=True,P=False):
        '''saves text values of system constraints , such as B(2,3) etc'''
        handle = open(output,'w')
        for vname,vnum in sorted(self.variables.items()):
            if vnum > len(solution):
                break
            if solution[vnum-1] > 0:
                if 'B' in vname and B:
                    handle.write('%s\n' % (vname)  )
                elif 'C' in vname and C:
                    handle.write('%s\n' % (vname)  )
                elif 'P' in vname and P:
                    handle.write('%s\n' % (vname)  )
        handle.close()


    def load_constraints_from_sol(self,sol_file,append=False):
        """ loads solution from minisat output in myinput handle, adds it to self.additional_sat_clauses constraints """
        myinput = open(sol_file)
        line = myinput.readline().strip()
        assert line == 'SAT'
        sols = [int(v) for v in myinput.readline().strip().split()]
        assert sols[-1] == 0
        sols = sols[:-1]
        assert len(sols) <= len(self.variables)
        new_constraints = []
        for vname, vnum in sorted(self.variables.items()):
            if vnum > len(sols):
                break
            if sols[vnum-1] > 0:
                new_constraints.append(self.variables[vname])
                #print(vname)
        if append:
            self.additional_sat_clauses.extend(new_constraints)
        return new_constraints

    def load_constraints_from_text_sol(self,sol_file,append=True):
        """ loads solution from written output (such as B(1,3), one clause per line) in myinput handle """
        myinput = open(sol_file)
        lines = [line.strip() for line in myinput.readlines()]
        new_constraints = []
        for vname in lines:
                new_constraints.append([self.variables[vname]])
                #print(vname)
        if append:
            #print 'Addding',new_constraints, 'to', self.basic_sat_clauses
            self.basic_sat_clauses.extend(new_constraints)
            #print self.basic_sat_clauses
        return new_constraints

        return new_constraints

    def load_BC_constraints_from_text_sol(self,sol_file,append=True):
        """ loads solution from written output (such as B(1,3), one clause per line) in myinput handle """
        myinput = open(sol_file)
        lines = [line.strip() for line in myinput.readlines()]
        new_constraints = []
        for vname in lines:
            if 'B' in vname or 'C' in vname:
                new_constraints.append([self.variables[vname]])
                #print(vname)
        if append:
            #print 'Addding',new_constraints, 'to', self.basic_sat_clauses
            self.basic_sat_clauses.extend(new_constraints)
            #print self.basic_sat_clauses
        return new_constraints


    def fill_constraints(self):
        self.generate_constraints()

    def dump_cnf_to_file(self,fname):
        self.output_cnf(self.basic_sat_clauses,open(fname,'w'))
        #with open(fname,'w') as outf:
        #    outf.write(parameters)


    def run_minisat(self,return_constraints=True):
        #print("Writing data")
        tempfilename = '/tmp/temp_for_minisat.%s.cls' % (os.getpid())
        tempout = tempfilename+'.sol'
        temp = open(tempfilename,'w')
        self.output_cnf(self.basic_sat_clauses,temp)
        #temp.write(parameters)
        temp.close()
        #here we execute
        #print [self.minisat_executable,tempfilename]
        process = subprocess.Popen([self.minisat_executable,tempfilename,tempout], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out = process.communicate()[0]
        result = out.split()[-1]
        if result == 'UNSATISFIABLE':
            return None,tempout
        elif result == 'SATISFIABLE':
            if return_constraints:
                #constraints = self.load_constraints_from_sol(tempout)
                self.convert_solution(open(tempout),open(tempout+'.converted','w'))
                #tempfilename = '/tmp/temp_for_minisat.%s.cls' % (os.getpid())
                #tempout = tempfilename+'.sol'
            return True, tempout+'.converted'
        else:
            raise IOError("Unknown output"+result)


    def add_constraints_all_particles(self):
        for a in range(self.Na):
            self.basic_sat_clauses.append( [self.P(p,a,r) for p in range(self.Np) for r in range(self.Nr)]  )

    def add_constraints_all_patches(self):
        for c in range(self.Nc):
            self.basic_sat_clauses.append( [self.C(a,s,c) for a in range(self.Na) for s in range(self.Ns)]  )

    def add_constraints_all_patches_except(self, forbidden):
        for c in range(self.Nc):
            if c != forbidden:
                self.basic_sat_clauses.append([self.C(a, s, c) for a in range(self.Na) for s in range(self.Ns)])
            # Do not use forbidden color
            for s in range(self.Ns):
                for a in range(self.Na):
                    self.basic_sat_clauses.append(
                            [-self.C(a, s, forbidden)]
                    )


    def add_constraints_no_self_complementarity(self,above_color=0):
        for c in range(above_color,self.Nc):
            self.basic_sat_clauses.append( [-self.B(c,c)  ]   )

    def add_constraints_unique_patches(self):
        c = 0
        for a in range(self.Na):
            for s in range(self.Ns):
                self.basic_sat_clauses.append([self.C(a, s, c)])
                c += 1

    def fix_particle_colors(self,ptype,sid,cid):
        self.basic_sat_clauses.append([self.C(ptype,sid,cid)])

    def fix_slot_colors(self,ptype,sid,cid):
        self.basic_sat_clauses.append([self.F(ptype,sid,cid)])

    def fix_color_interaction(self,c1,c2):
        self.basic_sat_clauses.append([self.B(c1,c2)] )


    def run_relsat(self,maxsol):
        #print("Writing data")
        tempfilename = '/tmp/temp_for_relsat.%s.cls' % (os.getpid())
        tempout = tempfilename+'.sol'
        temp = open(tempfilename,'w')
        self.output_cnf(self.basic_sat_clauses,temp)
        #temp.write(parameters)
        temp.close()
        #here we execute
        #print [self.minisat_executable,tempfilename]
        #process = subprocess.Popen([self.relsat_executable,' -#a ' ,tempfilename,tempout], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        print ('Calling'),
        print ('%s -#%d  %s> %s' % (self.relsat_executable, maxsol, tempfilename, tempout ))
        os.system('%s -#%d  %s | grep -v c > %s' %  (self.relsat_executable, maxsol, tempfilename, tempout ) )

        #out = process.communicate()[0]
        out = open(tempout).readlines()
        result = out[-1].strip() #.split()[-1]
        #print result
        if result == 'UNSAT':
            return 0,0
        elif result == 'SAT':
            all_solutions = []
            for line in out:
                if 'Solution' in line:
                    myvars = line.strip().split(':')[1].strip()
                    #print myvars
                    varnames =  self.load_solution_from_lines([myvars+ ' 0'])
                    clean_sol  = []
                    for x in varnames:
                        if 'P(' in x:
                            clean_sol.append(x)
                    all_solutions.append(clean_sol)

            return len(out)-1, all_solutions
        else:
            print (result)
            raise IOError("Found something else")

def do_sat_from_solution_file(solution_file,crystal_string):
    #simple function that loads solution in a text format (with B and C assignments) and checks the solution against crystal type; crystal type is a readable text describing the lattice
    colors = []
    particles = []
    with open(solution_file) as cf:
        for line in cf:
            sline = line.strip()
            if 'B' in sline:
                c1,c2 = [int(x) for x in  sline.split('(')[1].replace(')','').split(',') ]
                colors.extend([c1,c2])
            elif 'C' in sline:
                a1,s1,p1 = [int(x) for x in  sline.split('(')[1].replace(')','').split(',') ]
                particles.append(a1)

    Nc = max(colors)+1
    Na = max(particles)+1


    cs = crystal_string.strip().replace(',', '').splitlines()
    bindings_split = [[int(p) for p in line.split() if p.isdigit()] for line in cs]
    pidsa = [ x[0] for x  in bindings_split]
    pidsb = [ x[2] for x  in bindings_split]
    particles.extend(pidsa)
    particles.extend(pidsb)

    #Np = max(particles)+1

    print("Found Nc=%d, Na=%d, Np=%d" %  (Nc,Na,0))
    #print("Preparing system")
    mysat = LCSS(Na,Nc)
    mysat.set_crystal_topology_from_text(crystal_string)
    mysat.generate_constraints()
    mysat.load_BC_constraints_from_text_sol(solution_file)
    #mysat.check_settings()
    #print ("..done")

    result = mysat.run_minisat()
    return result



def do_all_sats_from_solution_file(solution_file,crystal_string,max_sol = 100000):
    #simple function that loads solution in a text format (with B and C assignments) and checks the solution against crystal type; crystal type is a readable text describing the lattice
    colors = []
    particles = []
    with open(solution_file) as cf:
        for line in cf:
            sline = line.strip()
            if 'B' in sline:
                c1,c2 = [int(x) for x in  sline.split('(')[1].replace(')','').split(',') ]
                colors.extend([c1,c2])
            elif 'C' in sline:
                a1,s1,p1 = [int(x) for x in  sline.split('(')[1].replace(')','').split(',') ]
                particles.append(a1)

    Nc = max(colors)+1
    Na = max(particles)+1


    cs = crystal_string.strip().replace(',', '').splitlines()
    bindings_split = [[int(p) for p in line.split() if p.isdigit()] for line in cs]
    pidsa = [ x[0] for x  in bindings_split]
    pidsb = [ x[2] for x  in bindings_split]
    particles.extend(pidsa)
    particles.extend(pidsb)

    #Np = max(particles)+1

    print("Found Nc=%d, Na=%d, Np=%d" %  (Nc,Na,0))
    #print("Preparing system")
    mysat = LCSS(Na,Nc)
    mysat.set_crystal_topology_from_text(crystal_string)
    mysat.generate_constraints()
    mysat.load_BC_constraints_from_text_sol(solution_file)
    #mysat.check_settings()
    #print ("..done")

    result = mysat.run_relsat(maxsol)
    return result


if __name__ == '__main__':
    #ctypes = {'diamond': john_diamond, 'hexagonal' : john_hexa, 'superhexa' : john_hexa_megalattice, 'ice0': john_ice0, 'clathrate' : john_clathrate}

    #ctypes = {'fullerene': john_fullerene} #, 'hexagonal' : john_hexa, 'superhexa' : john_hexa_megalattice, 'ice0': john_ice0, 'clathrate' : john_clathrate}

    ctypes = {'snubcube': diogo_snubcube, 'snubdode': diogo_snubdodecahedron, 'snubcube1': diogo_snubcube1, 'snubcube2': diogo_snubcube2}
    #ctypes = {'snubdode': diogo_snubdodecahedron}


    if len(sys.argv) != 3:
        print('Usage: %s file_with_B_and_Cs crystal_type' % (sys.argv[0] )  )
        print("Crystal types:")
        print(ctypes.keys())

        sys.exit(-1)

    sol_file = sys.argv[1]
    crystal_type = sys.argv[2]
    #ctypes = {'diamond': john_diamond, 'hexagonal' : john_hexa, 'superhexa' : john_hexa_megalattice, 'ice0': john_ice0, 'clathrate' : john_clathrate}
    crystal_string = ctypes[crystal_type]

    r = do_sat_from_solution_file(sol_file,crystal_string)
    if r is None:
        print ("%s NO" % (sol_file))
    elif r == True:
        print("%s YES" % (sol_file))
    else:
        print("ERROR")


    #constraints = generate_constraints()
    #if len(sys.argv) == 1:
    #    output_cnf(constraints)
    #else:
    #    #print >> sys.stderr, "Loading ", sys.argv[1]
    #    load_solution(open(sys.argv[1],'r'))

