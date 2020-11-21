#!/use/bin/env python3

import math
import random


def fnr(i):
    """a random position on the galactic map"""
    return int(random.random() * 7.98 + 1.01)


def fnd(i):
    raise ValueError("wtf is this?")
    return 0


print("")
print("                                    ,------*------,")
print("                    ,-------------   '---  ------'")
print("                     '-------- --'      / /")
print("                         ,---' '-------/ /--,")
print("                          '----------------'")
print("")
print("                    THE USS ENTERPRISE --- NCC-1701")
print("")

g = [[0 for x in range(8)] for y in range(8)]
z = [[0 for x in range(8)] for y in range(8)]
k = [[0 for x in range(3)] for y in range(3)]
n = [0, 0, 0]
d = [0, 0, 0, 0, 0, 0, 0, 0]  # initialized on 680
c = [  # initialised at 540 in basic
    [0, -1, -1, -1, 0, 1, 1, 1, 0],
    [1, 1, 0, 0, -1, -1, -1, 1, 1]
]
z_str = "                         "

e = 3000
s = 0

e0 = e
d0 = 0
t = random.randint(20, 40) * 100
t0 = t
t9 = 25 + random.randint(0, 10)
p = 10
p0 = p
s9 = 200
b9 = 2
k9 = 0
x_str = ""
x0_str = " IS "

q1 = fnr(1)
q2 = fnr(1)
s1 = fnr(1)
s2 = fnr(1)

a1_str = "NAVSRSLRSPHATORSHEDAMCOMXXX"

for i in range(0, 8):
    for j in range(0, 8):
        k3 = 0
        z[i][j] = 0
        r1 = random.random()
        if r1 > 0.80:
            k3 = 1
            k9 = k9 + 1
        elif r1 > 0.95:
            k3 = 2
            k9 = k9 + 2
        elif r1 > 0.98:
            k3 = 3
            k9 = k9 + 3
        b3 = 0
        if random.random() > 0.96:
            b3 = 1
            b9 = b9 + 1
        g[i][j] = k3 * 100 + b3 * 10 + fnr(1)

if k9 > t9:  # make sure you have at least one turn per klingon!
    t9 = k9 + 1

if b9 == 0:
    if g[q1][q2] < 200:  # make sure you start with some bad guys??
        g[q1][q2] += 120
        k9 += 1
    b9 = 1
    g[q1][q2] += 10
    q1 = fnr(1)
    q2 = fnr(1)

k7 = k9
if b9 != 1:
    x0_str = " ARE "
    x_str = "S"

print(f"YOUR ORDERS ARE AS FOLLOWS:\n   DESTROY THE {k9} KLINGON WARSHIPS WHICH HAVE INVADED\n   THE GALAXY BEFORE "
      f"THEY CAN ATTACK FEDERATION HEADQUARTERS\n   ON STARDATE {t0 + t9}. THIS GIVES YOU {t9} DAYS. THERE{x0_str}{b9} \n"
      f"   STARBASE{x_str} IN THE GALAXY FOR RESUPPLYING YOUR SHIP\n\n")
