import inspect
import copy
import json
from typing import List
from .package_primitives import WORKABLE_TYPES, FixedParameter
import time


def generate_api_key():
    import secrets
    import string

    key_length = 32
    # Define a character set from which the key will be generated
    characters = string.ascii_uppercase + string.digits
    api_key = "".join(secrets.choice(characters) for _ in range(key_length - 3))
    api_key = "cp-" + api_key
    return api_key


def match_parameters(func, *args, **kwargs):
    """
    Returns a dictionary of parameters matched to their values. If a parameter is not provided in the arguments, the default value is used.

    Note the input args and kwargs can be passed in in any order or method, it doesn't need to correspond to how they're defined in the function signature.
    """
    signature = inspect.signature(func)
    parameters = signature.parameters

    # Create an empty dictionary to record parameter values
    matched_params = {}

    # First, match position parameters
    for i, param_name in enumerate(parameters.keys()):
        if i < len(args):
            # If we have a corresponding positional argument, use it.
            matched_params[param_name] = args[i]
        elif param_name in kwargs:
            # Otherwise, check if we have a keyword argument.
            # Note that this could override positional arguments if names aren't matched properly.
            matched_params[param_name] = kwargs[param_name]
        else:
            # If there's no argument provided for a parameter with a default value, use the default.
            if parameters[param_name].default is not inspect.Parameter.empty:
                matched_params[param_name] = parameters[param_name].default
            else:
                raise TypeError(f"Missing required argument '{param_name}'")

    return matched_params


def parse_parameters(func, *demo_args, **demo_kwargs) -> List:
    """ """
    all_demos = match_parameters(func, *demo_args, **demo_kwargs)

    signature = inspect.signature(func)

    all_vars = []
    for param in signature.parameters.values():
        is_kwarg = param.default != inspect.Parameter.empty
        if is_kwarg == True:
            default_kwarg_value = param.default
        else:
            default_kwarg_value = None

        # check if variable is a custom derivative type
        if (
            param.annotation in WORKABLE_TYPES.__args__
            or type(param.annotation) in WORKABLE_TYPES.__args__
        ):
            if type(param.annotation) == type:
                # This in an uninstantiated type
                # We should instantiate it
                processed_param = param.annotation()
            else:
                # This is an instantiated type
                processed_param = copy.deepcopy(param.annotation)

            processed_param.name = param.name
            processed_param.is_kwarg = is_kwarg
            processed_param.kwarg_value = default_kwarg_value
            processed_param.demo_value = all_demos[param.name]
            processed_param.working_value = None

            all_vars.append(processed_param)

        else:
            # These are variables that aren't annotated by the user
            all_vars.append(
                FixedParameter(
                    name=param.name,
                    is_kwarg=is_kwarg,
                    live_working_value=all_demos[param.name],
                )
            )

    return all_vars


def parse_return_type(func):
    signature = inspect.signature(func)
    return_type = signature.return_annotation

    if return_type == inspect.Signature.empty:
        return "none"

    return return_type.__name__


def stream_handler(stream, callback):
    """
    Calls the callback at a fixed time period
    """
    built_str = ""
    CALLBACK_PERIOD = 1
    last_callback_at_time = time.time()

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            delta_content = chunk.choices[0].delta.content

            if type(delta_content) is not str:
                raise ValueError("The stream is not returning strings.")
            else:
                built_str += delta_content

            # check whether to call the callback
            if time.time() - last_callback_at_time > CALLBACK_PERIOD:
                callback(built_str)
                last_callback_at_time = time.time()

    callback(built_str)

    # Finally return the built string
    return built_str
