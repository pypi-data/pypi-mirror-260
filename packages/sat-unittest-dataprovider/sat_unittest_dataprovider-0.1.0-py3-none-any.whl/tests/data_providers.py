def tuples_in_list() -> list[tuple[int, int, int, str]]:
    return [
        (1, 2, 3, '1 + 2 is 3'),
        (2, 2, 4, '2 + 2 is 3')
    ]


def tuples_in_tuple() -> tuple[tuple[int, int, int, str], ...]:
    return (
        (1, 2, 3, '1 + 2 is 3'),
        (2, 2, 4, '2 + 2 is 3'),
    )


def dict_with_tuples() -> dict[str, tuple[int, int, int, str]]:
    return {
        "record_1": (1, 2, 3, '1 + 2 is 3'),
        "record_2": (2, 2, 4, '2 + 2 is 3'),
    }


a_dict: dict[str, tuple[int, int, int, str]] = {
    "record_1": (1, 2, 3, '1 + 2 is 3'),
    "record_2": (2, 2, 4, '2 + 2 is 3'),
}
