import os
import sys
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import system_prompt, user_prompt, model_name
from functions.call_function import available_functions
from functions.allowed_functions import *

def generate_response(client: genai.Client, messages: list):
    """
    Generates response from client with current set of messages.

    Parameters
    ----------
    client : genai.Client
        Client used.
    message : list
        list of messages used

    Returns
    -------
    response
        response from the model.
    """
    response = client.models.generate_content(
        model=model_name, 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt,
        ),
    )
    return response

def get_level_list() -> list[str]:
    """
    Generates list of all .lvl files in the directory.

    Returns
    -------
    list[str]
        list of all .lvl file names in directory
    """
    level_list = []
    directory_content = os.listdir(os.path.abspath('./'))
    for content in directory_content:
        content_source = os.path.join('./', content)
        if os.path.isfile(content_source):
            base, extension = os.path.splitext(content)
            if extension == '.lvl':
                level_list.append(content)
    return level_list

def show_level(map: list[list], drone: list, target: list) -> str:
    """
    Generates a printable output from the level and the positions of drone and target.

    Parameters
    ----------
    map: list[list]
        map to be shown.
    drone : list
        Coordinates of the drone.
    drone : list
        Coordinates of the target.

    Returns
    -------
    str
        Output text with formatting
    """
    x_max, y_max = len(map), len(map[0])

    printout = ''
    for i in range(x_max):
        for j in range(y_max):
            if [i,j] == drone and [i,j] == target:
                printout += '\033[92m'+'D'+'\033[0m'
            elif [i,j] == drone:
                printout += '\033[91m'+'D'+'\033[0m'
            elif [i,j] == target:
                printout += '\033[96m'+'T'+'\033[0m'
            else:
                printout += map[i][j]
        if i < x_max - 1:
            printout += '\n'
    return printout

def create_drone_map(level: list[list], drone: list) -> list[list]:
    """
    Generates a map for the drone_view.

    Parameters
    ----------
    level: list[list]
        level.
    drone : list
        Coordinates of the drone.

    Returns
    -------
    list[list]
        The known map for the drone, all '?', except the location of the drone itself
    """
    x_max, y_max = len(level), len(level[0])
    x_drone, y_drone = drone

    drone_map = [['?' for _ in range(y_max)] for _ in range(x_max)]
    drone_map[x_drone][y_drone] = level[x_drone][y_drone]
    
    return drone_map

def main():
    load_dotenv()
    
    # Obtain API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Api key not found!")

    # Initiate gemini client
    client = genai.Client(api_key=api_key)
    
    # Create list of available levels
    level_list = get_level_list()

    # Ask for which level to use
    if level_list == []:
        print("No levels found!")
        sys.exit(1)
    else:
        while True:
            print("Available level:")
            for i,level in enumerate(level_list):
                print(f'{i}: {level}')
            number = input('Which level (input the number)? ')
            if number.isdigit():
                if 0 <= int(number) < len(level_list):
                    level_file = level_list[int(number)]
                    break

    # Open the level
    with open(level_file, "r") as f:
        level = []
        row_length = []
        for line in f:
            if line == None:
                print("Level file corrupt")
                sys.exit(1)
            row = []
            text = line.strip()
            for char in text:
                row.append(char)
            level.append(row)
            row_length.append(len(row))
        # Check if the level is of rectangular shape
        if len(set(row_length)) > 1:
            print("Level file corrupt")
            sys.exit(1)

    # Set level size
    level_size = (len(level),len(level[0]))

    # Ask for starting drone position and target position
    while True:
        drone_position = [-1,-1]
        target_position = [-1,-1]

        print(show_level(level, drone_position, target_position))
        print(f'The level has {level_size[0]} rows and {level_size[1]} columns.' )

        try:
            drone_position_str = input('Where should the drone start (input as X,Y)? ')
            drone_position = [int(drone_position_str.split(',')[0])-1,int(drone_position_str.split(',')[1])-1]
        except:
            print("Drone position not valid. \n Try again:")
            continue

        try:
            target_position_str = input('Where should the target be (input as X,Y)? ')
            target_position = [int(target_position_str.split(',')[0])-1,int(target_position_str.split(',')[1])-1]
        except:
            print("Target position not valid. \n Try again:")
            continue

        if level[drone_position[0]][drone_position[1]] != ' ':
            print("Drone not in open space. \n Try again:")
            continue
        if level[target_position[0]][target_position[1]] != ' ':
            print("Target not in open space. \n Try again:")
            continue
        break
    
    # Create drone view
    drone_map = create_drone_map(level, drone_position)
    drone_map = update_map(level, drone_map, drone_position)

    print('Map visible to the drone:')
    print(show_level(drone_map, drone_position, target_position))

    # Compile user prompt as message, as well as the starting locations and the starting map known to the drone
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    messages.append(types.Content(role="user", parts=[types.Part(text=check_positions(drone_position, target_position))]))
    messages.append(types.Content(role="user", parts=[types.Part(text=check_map(drone_map))]))

    # To make sure that the system terminates, we limit to a total of 1000 function executions, but ask if user wants to terminate every 100
    for counter in range(1000):
        if counter % 100 == 0 and counter > 0:
            exitquestion = input('End pathfinding? (y/n) ')
            if exitquestion == 'y':
                print("User stopped search!")
                sys.exit(1)

        # get response with current messages from gemini
        try:
            response = generate_response(client, messages)
        except genai.errors.ServerError:
            print("Model is overloaded. Try again later.")
            
        
        # take the candidates from the response and append them to the current list of messages
        candidates = response.candidates
        if candidates:
            for candidate in candidates:
                messages.append(candidate)

        # check whether there was any meta data found with the response
        meta_data = response.usage_metadata
        if meta_data == None:
            raise RuntimeError("No Meta-data found!")
                
        # get the list of function calls from the response
        function_call_list = response.function_calls
        function_responses = []
        
        if function_call_list != None:
            for function_call in function_call_list:
                # Check if the functions are any of the known functions
                if function_call.name == 'check_positions':
                    function_call_result = types.Content(
                        role="tool",
                        parts=[
                            types.Part.from_function_response(
                                name='get_position',
                                response={"result": check_positions(drone_position, target_position)},
                            )
                        ]
                    )
                    function_responses.append(function_call_result.parts[0])

                    print(f'Step {counter}: Verify coordinates.')
                elif function_call.name == 'check_map':
                    function_responses.append(types.Part.from_function_response(
                                name='move_north',
                                response={"result": check_map(drone_map)},
                            )
                    )

                    print(f'Step {counter}: Review the map.')
                elif function_call.name == 'check_walkable':
                    function_responses.append(types.Part.from_function_response(
                                name='move_north',
                                response={"result": check_walkable(drone_map, drone_position)},
                            )
                    )

                    print(f'Step {counter}: Check free directions.')
                elif function_call.name == 'move_north':
                    movement = move_north(drone_map, drone_position)
                    if movement['success']:
                        drone_position[0] -= 1
                        drone_map = update_map(level, drone_map, drone_position)
                        function_responses.append(types.Part.from_function_response(
                                name='view_surroundings',
                                response={"result": f'This is the updated map after you moved {drone_map}'},
                            )
                        )
                    function_responses.append(types.Part.from_function_response(
                                name='move_north',
                                response={"result": movement['text']},
                            )
                    )
                    function_responses.append(types.Part.from_function_response(
                                name='move_north',
                                response={"result": check_walkable(drone_map, drone_position)},
                            )
                    )

                    print(f'Step {counter}: Move north:')
                    print(f'{show_level(drone_map, drone_position, target_position)}')
                    print(f'Open spaces: {check_walkable(drone_map, drone_position)}')
                elif function_call.name == 'move_south':
                    movement = move_south(drone_map, drone_position)
                    if movement['success']:
                        drone_position[0] += 1
                        drone_map = update_map(level, drone_map, drone_position)
                        function_responses.append(types.Part.from_function_response(
                                name='view_surroundings',
                                response={"result": f'This is the updated map after you moved {drone_map}'},
                            )
                        )
                    function_responses.append(types.Part.from_function_response(
                                name='move_south',
                                response={"result": movement['text']},
                            )
                    )
                    function_responses.append(types.Part.from_function_response(
                                name='move_north',
                                response={"result": check_walkable(drone_map, drone_position)},
                            )
                    )
                    
                    print(f'Step {counter}: Move south:')
                    print(f'{show_level(drone_map, drone_position, target_position)}')
                    print(f'Open spaces: {check_walkable(drone_map, drone_position)}')
                elif function_call.name == 'move_west':
                    movement = move_west(drone_map, drone_position)
                    if movement['success']:
                        drone_position[1] -= 1
                        drone_map = update_map(level, drone_map, drone_position)
                        function_responses.append(types.Part.from_function_response(
                                name='view_surroundings',
                                response={"result": f'This is the updated map after you moved {drone_map}'},
                            )
                        )
                    function_responses.append(types.Part.from_function_response(
                                name='move_west',
                                response={"result": movement['text']},
                            )
                    )
                    function_responses.append(types.Part.from_function_response(
                                name='move_north',
                                response={"result": check_walkable(drone_map, drone_position)},
                            )
                    )

                    print(f'Step {counter}: Move west:')
                    print(f'{show_level(drone_map, drone_position, target_position)}')
                    print(f'Open spaces: {check_walkable(drone_map, drone_position)}')
                elif function_call.name == 'move_east':
                    movement = move_east(drone_map, drone_position)
                    if movement['success']:
                        drone_position[1] += 1
                        drone_map = update_map(level, drone_map, drone_position)
                        function_responses.append(types.Part.from_function_response(
                                name='view_surroundings',
                                response={"result": f'This is the updated map after you moved {drone_map}'},
                            )
                        )
                    function_responses.append(types.Part.from_function_response(
                                name='move_east',
                                response={"result": movement['text']},
                            )
                    )
                    function_responses.append(types.Part.from_function_response(
                                name='move_north',
                                response={"result": check_walkable(drone_map, drone_position)},
                            )
                    )

                    print(f'Step {counter}: Move east:')
                    print(f'{show_level(drone_map, drone_position, target_position)}')
                    print(f'Open spaces: {check_walkable(drone_map, drone_position)}')
                else:
                    print(f'Step {counter}: Tried to use function {function_call.name}. It does not exist:')                    
                    
            # add the function responses to the messages list
            messages.append(types.Content(role="user", parts=function_responses))
        else:
            # if there were no new function calls, print the response of the client
            print("Response:")
            if response.text == None:
                print('No response, terminated with "None"')
                break
            print(response.text)
            break
    else:
        # if loop terminated let user know that the client did not get to a final response
        print("Gemini did not reach a final response!")
        sys.exit(1)


if __name__ == "__main__":
    main()
