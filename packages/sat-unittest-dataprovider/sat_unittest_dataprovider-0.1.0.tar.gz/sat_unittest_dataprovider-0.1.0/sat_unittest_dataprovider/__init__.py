import inspect
import functools
from inspect import Arguments
from types import FunctionType
from typing import Union, Dict, Tuple, List, Callable, TypeAlias

DataSetType: TypeAlias = Union[Callable, Dict, Tuple, List]
DataSetReturnType: TypeAlias = Union[Dict, Tuple, List]


def __validate_data_set(data_set: DataSetType):
    supported_types = [FunctionType, list, dict, tuple]
    if not type(data_set) in supported_types:
        types_csv = ", ".join([
            x.__name__.capitalize() for x in supported_types
        ])
        msg = f"data_set must be of type [{types_csv}],"
        msg += f" got '{type(data_set).__name__.capitalize()}'"
        raise AttributeError(msg)


def __convert_to_list(data_set: DataSetType) -> list[DataSetReturnType]:
    if type(data_set) is FunctionType:
        data_set_list = __convert_to_list(data_set())   # we convert the result of the function to a list
    elif type(data_set) is dict:
        data_set_list = list(data_set.values())
    else:
        data_set_list = data_set

    return [row for row in data_set_list]


def data_provider(data_set: Union[Callable, Dict, Tuple, List]) -> Callable:
    # check is data_set a function
    __validate_data_set(data_set)

    data_set_list = __convert_to_list(data_set)

    def function_wrapper(func: FunctionType):
        functools.wraps(func)

        def method_args(self, *args):
            func_value = []
            for row in data_set_list:
                func_value.append(func(self, *row, *args))

            return func_value

        def function_args(*args):
            func_value = []
            for row in data_set_list:
                func_value.append(func(*row, *args))

            return func_value

        func_args: Arguments = inspect.getargs(func.__code__)

        return method_args if 'self' in func_args.args else function_args

    return function_wrapper
