from google.genai import types

from .allowed_functions import *

def call_function(function_call: dict, verbose: bool = False) -> types.Content:
    """
    Looks through the content of the directory.

    Parameters
    ----------
    function_call : dict
        containing function name and arguments.
    verbose : boolean, optional
        whether the function should be verbose

    Returns
    -------
    types.Content
        the function response or an error response.
    """
    
    # Output if verbose
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
        
    # Verify name
    function_name = function_call.name or ""
    
    # Check if function_name appears in the list of available functions
    if not function_name in function_map.keys():
        # return an error as content that the function did not exist
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    else:
        args = dict(function_call.args) if function_call.args else {}

        
        # get results from running the function with its arguments
        function_result = function_map[function_name](**args)
        
        # return the result
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )