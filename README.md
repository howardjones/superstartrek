# SUPER STAR TREK

Attempting to make a Python version of Super Star Trek from David Ahl's classic Basic Computer Games.

Original Source Code from here: http://www.vintage-basic.net/bcg/superstartrek.bas

Scanned from here: https://www.atariarchives.org/basicgames/showpage.php?page=157

My cleaned up source (adding about 2.5KB of whitespace only - no code changes!) is in [tidied-source.bas](tidied-source.bas)

## NOTES

No string arrays make this jump around a lot more than it needs to!

Arrays count from 1 in basic, and 0 in Python - be careful!

Everything is global

### ARRAYS
    
    G is the galactic map. One integer for each  (100s are klingons, 10s are bases, 1s are stars)
    Z is a copy of the galactic map
    C is direction vectors for moving ship
    D is the damage to various systems
    
### VARIABLES

    Q1,Q2 is your initial position
    Z4,Z5 is your current position
    S shield level (starts at 0)
    E energy (starts at 3000)
    K9 current number of klingons
    B9 number of starbases
    T9 number of turns total
    T0 starting stardate
    
    
### SUBROUTINES
    
    