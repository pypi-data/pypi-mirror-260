
def snake_case_to_camel_case(snake_case_value: str, first_to_upper: bool = False) -> str:
    """
    This function converts a given snake_case value to an camelCase
    :param first_to_upper: If True, the first item of the snake_case items will be converted as well
    :param snake_case_value:
    :return: The camelCase string
    """
    snake_case_items = snake_case_value.split("_")  # we split the value at each `_` underscore
    camel_case_items: list = list()                 # a list to store the converted items

    for index, item in enumerate(snake_case_items):

        first_letter = item[:1]     # we get the first letter of the item
        the_rest = item[1:]         # we get the rest of the string, excluding the first letter

        # make sure the first item is lower case
        if first_to_upper is False and index == 0:
            camel_case_items.append(first_letter.lower() + the_rest)
        else:
            camel_case_items.append(first_letter.upper() + the_rest)

    return "".join(camel_case_items)
