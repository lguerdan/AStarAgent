——— INPUT ———
##Usage:
`python route_find.py <inputfile> <boolean nieve> <boolean launcher> <boolean speedbump>`


`inputfile` (required): the input room for the program. If the file can’t be opened an error message will be displayed.

`nieve` (optional): if True, will use BFS to calculate robot path instead of A *

`launcher` (optional): if True, will randomly generate a launch pad

`speedbump` (optional: if True, will randomly generate a speed bump


** All three optional args are False by default.
No opts are enabled, meaning if an optional positional argument is specified the preceding optional args must also be provided **

###Launcher:
If enabled, will choose a random location in the grid to accelerate objects when landed on.
A random launch value (1 or 2) will be added to previous object speed.

###Speedbump:
If enabled, will choose a random location in the grid to decellerate objects when landed on.
The previous object speed will be decremented by one if it is greater than 1.




——— OUTPUT ———


If the program determines that the input file is not formatted properly,
it will proceed to print a message describing which line of the input was formatted incorrectly (in the case that multiple lines are incorrect, it will only mention the first one of them) or it will print the message, `Input error: incorrect filesize`.
If the program determines that the input file is formatted properly, it will proceed to print a number of maps as well as the coordinates of each object.
Each map represents one iteration of the program (from one map to another, the robot will never move more than 1 space).


Should the robot become blocked or the exit is permanently covered,
the program will exit and state the robot finish.



#KEY (items listed in order of priority on map)

O  —  obstacle
R  —  robot
F  —  starting point
L  —  finishing point
+  —  space visited by robot
-  —  empty space
~  —  speed bump (will reduce an obstacle’s speed by 1, but to no lower than 1)
1 or 2  —  launchpad (will increase an obstacle’s speed by the number displayed)








