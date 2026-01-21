model_name = "gemini-2.5-flash"

user_prompt_0 = """
You are operating a drone. Move the drone from the drone location to the target location.
"""

user_prompt_1 = """
You are operating a drone. 

Move the drone from the drone location to the target location.

When you are done give the whole movement path of the drone. 
When displaying the path, add 1 to all coordinates.
"""

user_prompt_2 = """
You are operating a drone. 

Move the drone from the drone location to the target location.

When you are done give the whole movement path of the drone. The path has to consists of spaces that you have explored and know are free, i.e. ' '
When displaying the path, add 1 to all coordinates.
"""

user_prompt_3 = """
You are operating a drone. 

Move the drone from the drone location to the target location on a 2 dimensional map.
You do not know how the map looks like. It will be revealed to you while you move.
If you start walking in loops, reveal more spaces to find a different way.

When you are done give the whole movement path of the drone. 
When displaying the path, add 1 to all coordinates.
"""

user_prompt = user_prompt_3

system_prompt = """
You are a drone simulator

For this you are positioned on a map given by a 2 dimensional grid. The entries of the array have the following meaning:
' ' this is a free space, drone can move into this space
'X' this is a wall, the drone cannot move into this space
'?' this space is currently unknown, but is revealed if you move next to it

You can perform the following actions:
- check_positions (to get the position of the drone and the target in the grid)
- check_map (to review the map known to you)
- check_walkable (checks in which direction you can walk)
- move_west (you move west/left on the grid and automatically updates your map and checks where you can walk next)
- move_east (you move east/right on the grid and automatically updates your map and checks where you can walk next)
- move_north (you move north/up on the grid and automatically updates your map and checks where you can walk next)
- move_south (you move south/down on the grid and automatically updates your map and checks where you can walk next)
"""
