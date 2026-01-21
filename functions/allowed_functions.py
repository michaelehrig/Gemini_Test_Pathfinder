from google.genai import types

def check_positions(drone: list, target: list) -> str:
    """
    Checks position of drone and target.

    Parameters
    ----------
    drone : list
        Coordinates of the drone.
    target : list
        Coordinates of the drone.

    Returns
    -------
    str
        Text giving drone and target positions.
    """

    return f"Your drone is at position {drone}. The target is at position {target}."

# Instruct the API what check_position does 
schema_check_positions = types.FunctionDeclaration(
    name="check_positions",
    description="Returns the coordinates of the drone and the target",
    parameters=types.Schema(
        type=types.Type.OBJECT,
    ),
)

def check_map(drone_map: list[list]) -> str:
    """
    Checks known map for the drone.

    Parameters
    ----------
    drone_map : list[list]
        Currently known map for the drone.

    Returns
    -------
    str
        Text giving the drone map.
    """
    return f'The map known to you is {drone_map}'

# Instruct the API what check_map does 
schema_check_map = types.FunctionDeclaration(
    name="check_map",
    description="You review the map known to you.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
    ),
)

def check_walkable(drone_map: list[list], drone_position: list) -> str:
    """
    Checks in which directions the drone can walk.

    Parameters
    ----------
    drone_map : list[list]
        Currently known map for the drone.
    drone : list
        Coordinates of the drone.

    Returns
    -------
    str
        Text giving a list of the walkable directions.
    """

    x_max = len(drone_map)
    y_max = len(drone_map[0])

    walkable_directions = []

    if 0 <= drone_position[0]-1:
        if drone_map[drone_position[0]-1][drone_position[1]] == ' ':
            walkable_directions.append('north')
    if drone_position[0]+1 < x_max:
        if drone_map[drone_position[0]+1][drone_position[1]] == ' ':
            walkable_directions.append('south')
    if 0 <= drone_position[1]-1:
        if drone_map[drone_position[0]][drone_position[1]-1] == ' ':
            walkable_directions.append('west')
    if drone_position[1]+1 < y_max:
        if drone_map[drone_position[0]][drone_position[1]+1] == ' ':
            walkable_directions.append('east')
    return f'You can move to the following directions {walkable_directions}'

# Instruct the API what check_walkable does 
schema_check_walkable = types.FunctionDeclaration(
    name="check_walkable",
    description="You determine in which directions you can walk from this location.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
    ),
)

def move_north(drone_map: list[list], drone_position: list) -> {str, bool}:
    """
    Attempts to move the drone north.

    Parameters
    ----------
    drone_map : list[list]
        Currently known map for the drone.
    drone : list
        Coordinates of the drone.

    Returns
    -------
    {'text', 'success}
        'text': Explanation what happened
        'success': Returns whether the movement was successful
    """
    if 0 <= drone_position[0]-1:
        if drone_map[drone_position[0]-1][drone_position[1]] == ' ':
            return {'text' : f'The drone moved north by one step. The new drone position is {[drone_position[0]-1,drone_position[1]]}', 'success' : True}
        elif drone_map[drone_position[0]-1][drone_position[1]] == 'X':
            return {'text' : f'The drone cannot move there, this is a wall', 'success' : False}
        elif drone_map[drone_position[0]-1][drone_position[1]] == '?':
            return {'text' : f'You need to know what it there to move into that space', 'success' : False}
        else:
            return {'text' : f'Unidentified obstacle, go around', 'success' : False}
    return {'text' : f'That is outside the allowed area', 'success' : False}

# Instruct the API what move_north does
schema_move_north = types.FunctionDeclaration(
    name="move_north",
    description="Try to move north and update your map",
    parameters=types.Schema(
        type=types.Type.OBJECT,
    ),
)

def move_south(drone_map: list[list], drone_position: list) -> {str, bool}:
    """
    Attempts to move the drone south.

    Parameters
    ----------
    drone_map : list[list]
        Currently known map for the drone.
    drone : list
        Coordinates of the drone.

    Returns
    -------
    {'text', 'success}
        'text': Explanation what happened
        'success': Returns whether the movement was successful
    """
    x_max = len(drone_map)

    if drone_position[0]+1 < x_max:
        if drone_map[drone_position[0]+1][drone_position[1]] == ' ':
            return {'text' : f'The drone moved south by one step. The new drone position is {[drone_position[0]+1,drone_position[1]]}', 'success' : True}
        elif drone_map[drone_position[0]+1][drone_position[1]] == 'X':
            return {'text' : f'The drone cannot move there, this is a wall', 'success' : False}
        elif drone_map[drone_position[0]+1][drone_position[1]] == '?':
            return {'text' : f'You need to know what it there to move into that space', 'success' : False}
        else:
            return {'text' : f'Unidentified obstacle, go around', 'success' : False}
    return {'text' : f'That is outside the allowed area', 'success' : False}

# Instruct the API what move_south does 
schema_move_south = types.FunctionDeclaration(
    name="move_south",
    description="Try to move south and update your map.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
    ),
)

def move_west(drone_map: list[list], drone_position: list) -> {str, bool}:
    """
    Attempts to west the drone north.

    Parameters
    ----------
    drone_map : list[list]
        Currently known map for the drone.
    drone : list
        Coordinates of the drone.

    Returns
    -------
    {'text', 'success}
        'text': Explanation what happened
        'success': Returns whether the movement was successful
    """
    if 0 <= drone_position[1]-1:
        if drone_map[drone_position[0]][drone_position[1]-1] == ' ':
            return {'text' : f'The drone moved west by one step. The new drone position is {[drone_position[0],drone_position[1]-1]}', 'success' : True}
        elif drone_map[drone_position[0]][drone_position[1]-1] == 'X':
            return {'text' : f'The drone cannot move there, this is a wall', 'success' : False}
        elif drone_map[drone_position[0]][drone_position[1]-1] == '?':
            return {'text' : f'You need to know what it there to move into that space', 'success' : False}
        else:
            return {'text' : f'Unidentified obstacle, go around', 'success' : False}
    return {'text' : f'That is outside the allowed area', 'success' : False}

# Instruct the API what move_west does 
schema_move_west = types.FunctionDeclaration(
    name="move_west",
    description="Try to move west and update your map",
    parameters=types.Schema(
        type=types.Type.OBJECT,
    ),
)

def move_east(drone_map: list[list], drone_position: list) -> {str, bool}:
    """
    Attempts to move the drone east.

    Parameters
    ----------
    drone_map : list[list]
        Currently known map for the drone.
    drone : list
        Coordinates of the drone.

    Returns
    -------
    {'text', 'success}
        'text': Explanation what happened
        'success': Returns whether the movement was successful
    """
    y_max = len(drone_map[0])

    if drone_position[1]+1 < y_max:
        if drone_map[drone_position[0]][drone_position[1]+1] == ' ':
            return {'text' : f'The drone moved east by one step. The new drone position is {[drone_position[0],drone_position[1]+1]}', 'success' : True}
        elif drone_map[drone_position[0]][drone_position[1]+1] == 'X':
            return {'text' : f'The drone cannot move there, this is a wall', 'success' : False}
        elif drone_map[drone_position[0]][drone_position[1]+1] == '?':
            return {'text' : f'You need to know what it there to move into that space', 'success' : False}
        else:
            return {'text' : f'Unidentified obstacle, go around', 'success' : False}
    return {'text' : f'That is outside the allowed area', 'success' : False}

# Instruct the API what move_east does 
schema_move_east = types.FunctionDeclaration(
    name="move_east",
    description="Try to move east and update your map",
    parameters=types.Schema(
        type=types.Type.OBJECT,
    ),
)

def update_map(level: list[list], drone_map: list[list], drone_position: list) -> list[list]:
    """
    Updates the drone map from the level with the current drone position.

    Parameters
    ----------
    level : list[list]
        Currently known map for the drone.
    drone_map : list[list]
        Currently known map for the drone.
    drone : list
        Coordinates of the drone.

    Returns
    -------
    list[list]
        returns the updated map
    """
    x_max = len(drone_map)
    y_max = len(drone_map[0])

    # all cells surrounding the drone position are now visible (including diagonals)
    for i in range(x_max):
        for j in range(y_max):
            if (abs(i - drone_position[0]) <= 1) and (abs(j - drone_position[1]) <= 1):
                drone_map[i][j] = level[i][j]
    return drone_map

# sets available functions as tools for the API
available_functions = types.Tool(
    function_declarations=[
        schema_check_positions, 
        schema_check_map,
        schema_check_walkable,
        schema_move_north,
        schema_move_south,
        schema_move_west,
        schema_move_east,
    ],
)

