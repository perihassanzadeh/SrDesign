#Test Kociemba Python Module for Solving Rubik's Cube
#Used for testing integration purposes with computer vision
#Peri Hassanzadeh
#Last Modified: November 27th, 2022

##--NOTES--##
#Standard Cube Orientation
#UP Right Front Down Left back

#up = Yellow
#left = blue
#front = red
#right = green
#back = orange
#down - white

#Imported Libraries
import kociemba

#Set Cube Faces with Lowercase first letter of color
up= "yyywywyyy"
front = "ooooroooo"
down = "wwwywywww"
left = "ggggbgggg"
right = "bbbbgbbbb"
back = "rrrrorrrr"

#Final State String Formatted for Colors
init = up + right + front + down + left+back
print(init)

#Format State String for Kociemba Module
init = init.replace('y', 'U')
init = init.replace('r', 'F')
init= init.replace('g', 'R')
init=init.replace('o', 'B')
init=init.replace('w', 'D')
init=init.replace('b', 'L')
print(init)

#Manual Check
tosolve = 'RFFUULULBRULURDUBRFDUDFBLFFDURRDLUFFBRLBLBBFBDDDRBRDLL'
if init==tosolve:
	print("CORRECT") 

#Display Solve Sequence
print(kociemba.solve(init))
#"U' D R' L2 F' U L U2 L2 U' L' D2 F2 D F2 D' L2 U B2 U2 F2"