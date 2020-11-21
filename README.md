# SUPER STAR TREK

Attempting to make a Python version of Super Star Trek from David Ahl's classic Basic Computer Games.

Original Source Code from here: http://www.vintage-basic.net/bcg/superstartrek.bas

Scanned from here: https://www.atariarchives.org/basicgames/showpage.php?page=157

My cleaned up source (adding about 2.5KB of whitespace only - no code changes!) is in [tidied-source.bas](tidied-source.bas)

## NOTES

No string arrays make this jump around a lot more than it needs to!

Arrays count from 1 in basic, and 0 in Python - be careful!

Everything is global

The (edited!) book copy of the code includes quite a few commented-out commands

There **are** typos/scanning errors in the code! (e.g. line 7570 had a goto to 1740 instead of 7740, 8590 goes to 8590 not 1590)

### CONSTANTS

    Ship Devices
    1 Warp Engines
    2 Short Range Scanner
    3 Long Range Scanner
    4 Phasers
    5 Photon Tubes
    6 Damage Control
    7 Shield Control
    8 Library Computer

### ARRAYS
    
    G is the galactic map. One integer for each  (100s are klingons, 10s are bases, 1s are stars)
    Z is a copy of the galactic map
    C is direction vectors for moving ship
    D is the damage to various systems (device numbers from 1 to 8)
    
### VARIABLES

    Q$ is a 190 char string, 3 chars per position for 8*8 quadrant map (SRS)
    Q1,Q2 is your initial position 1-8,1-8 (quadrant)
    S1,S2 is your position *within* quadrant    
    Z4,Z5 is your current position 1-8,1-8
    S shield level (starts at 0)
    E energy (starts at 3000)
    K9 current number of klingons
    B9 number of starbases
    T9 number of turns total
    T0 starting stardate

    S3 stars in current quadrant
    K3 klingons in current quadrant
    B3 starbases in current quadrant
    K status of up to 3 klingons in current quadrant    
    B4,B5 coordinates of starbase (if any) in current quadrant
        
### SUBROUTINES

    6430 -     
    8590 - find a blank spot in the local map - sets r1,r2 to location
    8660 - insert a$ into q$ at position z1,z2 (in 190 char string) 
    8780 - set G2$ to device name in R1
    8830 - compare item at z1,z2 in local map with a$, set z3=1 if matching    
    9010 - set G2$ to quadrant Z4,Z5 (without roman numerals if G5=1)