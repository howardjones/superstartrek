#!/use/bin/env python3

import math
import random
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def fnr(i):
    """a random position on the galactic map"""
    return int(random.random() * 7.98 + 1.01)


def fnd(i):
    raise ValueError("wtf is this?")
    return 0


def coords_to_strpos(z1, z2):
    return int(z2 - 0.5) * 3 + int(z1 - 0.5) * 24


def print_map(q_str):
    print("---------------------------------")
    for i in range(1, 9):
        p = coords_to_strpos(i, 1)
        print(q_str[p:p + 23])
    print("---------------------------------")


def update_local_map(mapstring, z1, z2, a_str):
    s8 = coords_to_strpos(z1, z2)
    logger.debug(f"Putting {a_str} at {z1},{z2} ({s8})")
    if len(a_str) != 3:
        raise ValueError("ERROR")
    if s8 == 0:
        logger.debug("Special case for first pos")
        mapstring = a_str + mapstring[3:]
    elif s8 == 189:
        logger.debug("Special case for last pos")
        mapstring = mapstring[:188] + a_str
    else:
        mapstring = mapstring[:s8] + a_str + mapstring[s8 + 3:]

    return mapstring


def check_map_contents(q_str, z1, z2, expected):
    s8 = coords_to_strpos(z1, z2)
    g = q_str[s8:s8 + 3]
    logger.debug(f"Pos {z1},{z2} ({s8}) is '{g}' (Looking for '{expected}')")
    if g != expected:
        return False
    return True


def find_empty_map_spot(q_str):
    while True:
        r1 = fnr(1)
        r2 = fnr(1)
        if check_map_contents(q_str, r1, r2, "   "):
            return r1, r2


def device_name(r1):
    names = ["WARP ENGINES", "SHORT RANGE SENSORS", "LONG RANGE SENSORS", "PHASER CONTROL", "PHOTON TUBES",
             "DAMAGE CONTROL", "SHIELD CONTROL", "LIBRARY COMPUTER"]
    return names[r1 - 1]


def quadrant_name(z4, z5, g5):
    quadrants = ["ANTARES", "RIGEL", "PROCYON", "VEGA", "CANOPUS", "ALTAIR", "SAGGITARIUS", "POLLUX", "SIRIUS", "DENEB",
                 "CAPELLA", "BETELGEUSE", "ALDEBARAN", "REGULUS", "ARCTURUS", "SPICA"]
    subquadrants = ["I", "II", "III", "IV"]
    name = "BROKEN-NAME"
    print(f"Naming {z4},{z5}")
    if z5 <= 4:
        name = quadrants[z4 - 1]
    else:
        name = quadrants[z4 + 8 - 1]
    if g5 != 1:
        name += " " + subquadrants[z5 % 4]

    return name


print("")
print("                                    ,------*------,")
print("                    ,-------------   '---  ------'")
print("                     '-------- --'      / /")
print("                         ,---' '-------/ /--,")
print("                          '----------------'")
print("")
print("                    THE USS ENTERPRISE --- NCC-1701")
print("")

# making these 9x9 for now, to avoid 0vs1 array indices
g = [[0 for x in range(9)] for y in range(9)]
z = [[0 for x in range(9)] for y in range(9)]
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

for i in range(1, 9):
    for j in range(1, 9):
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

i = random.random()

# on entering a new quadrant (line 1310)
z4 = q1
z5 = q2
k3 = 0
b3 = 0
s3 = 0
g5 = 0
d4 = 0.5 * random.random()
z[q1][q2] = g[q1][q2]

if q1 < 1 or q1 > 8 or q2 < 1 or q2 > 8:
    pass

g2 = quadrant_name(z4, z5, g5)
if t == t0:
    print("YOUR MISSION BEGINS WITH YOUR STARSHIP LOCATED")
    print(f"IN THE GALACTIC QUADRANT, '{g2}'.")
else:
    print(f"NOW ENTERING {g2} QUADRANT . . .")

k3 = int(g[q1][q2] * 0.01)
b3 = int(g[q1][q2] * 0.1) - 10 * k3
s3 = g[q1][q2] - 100 * k3 - 10 * b3
print(f"{k3} klingons, {b3} bases, {s3} stars")
if k3 > 0:
    print("COMBAT AREA      CONDITION RED")
    if s <= 200:
        print("   SHIELDS DANGEROUSLY LOW")
for i in range(3):
    k[i][0] = 0
    k[i][1] = 0
    k[i][2] = 0

# q_str is a 192-char long string for the quadrant map
q_str = 192 * " "
q_str = update_local_map(q_str, s1, s2, "<*>")
if k3 > 0:
    for i in range(0, k3):
        r1, r2 = find_empty_map_spot(q_str)
        z1 = r1
        z2 = r2
        q_str = update_local_map(q_str, r1, r2, "+K+")
        k[i][0] = r1
        k[i][1] = r2
if b3 > 0:
    r1, r2 = find_empty_map_spot(q_str)
    q_str = update_local_map(q_str, r1, r2, ">!<")
    b4 = r1
    b5 = r2
if s3 > 0:
    for i in range(0, s3):
        r1, r2 = find_empty_map_spot(q_str)
        q_str = update_local_map(q_str, r1, r2, " * ")

did_dock = False
for i in range(s1 - 1, s1 + 2):  # (upper range is not inclusive)
    for j in range(s2 - 1, s2 + 2):
        if i >= 1 and i <= 8 and j >= 1 and j <= 8:
            if check_map_contents(q_str, i, j, ">!<"):
                did_dock = True
if did_dock:
    d0 = 1
    c_str = "DOCKED"
    p = p0
    e = e0
    print("SHIELDS DROPPED FOR DOCKING PURPOSES")
    s = 0
else:
    if k3 > 0:
        c_str = "*RED*"
    else:
        c_str = "GREEN"
        if e < e0 * 0.1:
            c_str = "AMBER"

if d(2) == 0:
    print("*** SHORT RANGE SENSORS ARE OUT ***")
else:
    print("---------------------------------")
    for i in range(1, 9):
        for j in range(coords_to_strpos(i, 1), coords_to_strpos(i, 8), 3):
            print(" ")
    print("---------------------------------")

# line 1990
