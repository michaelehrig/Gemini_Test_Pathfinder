# Gemini Test Pathfinder

This is an experimental project to see how Gemini performs the simple task of moving a drone through a 2-dimensional grid.

Example maps are provided as '.lvl' files.
Start and target positions can be chosen within the free parts of the grid upon loading of the map.

Different prompts are included in the 'config.py' file to test. From a simple 'Find the way' to a more complex prompt telling Gemini what to do when he is getting stuck. This is meant to be extended to test other prompts as well as easily extendable to add more functions.

The following functions are available to Gemini:

## check_positions
To verify the position of the drone and the target.

## check_map
To see the currently visible and known map of the drone. The drone only knows the parts of the map it has been to and when it moves all surrounding cells.

## check_walkable
Checks in which directions the drone is allowed to walk here.

## move_north/move_south/move_west/move_east
Let's the drone move in the corresponding direction if possible.

