from unittest import TestCase
from sat_unittest_dataprovider import data_provider
from .real_world_example import snake_case_to_camel_case
from .data_providers import (
    tuples_in_list,
    tuples_in_tuple,
    dict_with_tuples,
    a_dict
)


def my_data_set():
    return [
        [1, 1, '1 * 1 is 1'],
        [2, 4, '2 * 2 is 4'],
        [3, 9, '3 * 3 is 9']
    ]


class Test(TestCase):

    def test_without_dataprovider(self):
        test_data = [
            (1, 1, '1 * 1 is 1'),
            (2, 4, '2 * 2 is 4')
        ]
        for row in test_data:
            given_value, expected_result, msg = row
            calculated_result = given_value * given_value
            self.assertEqual(expected_result, calculated_result, msg)

    @data_provider([
        (1, 1, '1 * 1 is 1'),
        (2, 4, '2 * 2 is 4')
    ])
    def test_with_dataprovider(self, given_value, expected_result, msg):
        calculated_result = given_value * given_value
        self.assertEqual(expected_result, calculated_result, msg)

    @data_provider([
        (1, 2, 3, '1 + 2 = 3')
    ])
    def test_simple_example(self, value, value2, expected, msg):
        self.assertEqual(expected, value + value2, msg)

    @data_provider([
        (1, 1, '1 * 1 is 1'),
        (2, 4, '2 * 2 is 4'),
        (3, 9, '3 * 3 is 9')
    ])
    def test_multiply(self, given, expected, message):
        calculated_result = given * given
        self.assertEqual(expected, calculated_result, message)

    @data_provider([
        [1, 1, '1 * 1 is 1'],
        [2, 4, '2 * 2 is 4'],
        [3, 9, '3 * 3 is 9']
    ])
    def test_multiply_with_list(self, given, expected, message):
        calculated_result = given * given
        self.assertEqual(expected, calculated_result, message)

    @data_provider(my_data_set)
    def test_multiply_with_function(self, given, expected, message):
        calculated_result = given * given
        self.assertEqual(expected, calculated_result, message)

    @data_provider(my_data_set)
    def test_divider_with_function(self, divider, given, message):
        expected_result = divider
        calculated_result = given // divider
        self.assertEqual(expected_result, calculated_result)

    @data_provider(tuples_in_list)
    def test_addition_with_tuples_in_list(self, value1, value2, expected, msg):
        self.assertEqual(expected, value1 + value2, msg)

    @data_provider(tuples_in_tuple)
    def test_addition_with_tuples_in_tuple(self, value1, value2, expected, msg):
        self.assertEqual(expected, value1 + value2, msg)

    @data_provider(dict_with_tuples)
    def test_addition_with_dict_with_tuples(self, value1, value2, expected, msg):
        self.assertEqual(expected, value1 + value2, msg)

    @data_provider(a_dict)
    def test_addition_with_a_dict(self, value1, value2, expected, msg):
        self.assertEqual(expected, value1 + value2, msg)

    @data_provider([
        # The snake case value  | First item upper | The Expected Result     | The failure message
        ("some_camel_case_string",      True,       "SomeCamelCaseString",      "Test Case 1, first item upper"),
        ("this_is_Another_string",      True,       "ThisIsAnotherString",      "Test Case 2, first item upper"),
        ("ThisIsAlreadyCamelCase",      True,       "ThisIsAlreadyCamelCase",   "Test Case 3, first item upper"),
        ("This_is_an_other_Test",       True,       "ThisIsAnOtherTest",        "Test Case 4, first item upper"),
        ("This_is_an_OtHer_Test",       True,       "ThisIsAnOtHerTest",        "Test Case 5, first item upper"),
        ("a_b_c_d_e_f_g_h_i_j_k",       True,       "ABCDEFGHIJK",              "Test Case 6, first item upper"),
        ("test_with_2_numbers_1_and_2", True,       "TestWith2Numbers1And2",    "Test Case 7, first item upper"),

        # No we run the same test, but this time, the first item should be lower case
        ("some_camel_case_string",      False,      "someCamelCaseString",      "Test Case 8, first item lower"),
        ("this_is_Another_string",      False,      "thisIsAnotherString",      "Test Case 9, first item lower"),
        ("ThisIsAlreadyCamelCase",      False,      "thisIsAlreadyCamelCase",   "Test Case 10, first item lower"),
        ("This_is_an_other_Test",       False,      "thisIsAnOtherTest",        "Test Case 11, first item lower"),
        ("This_is_an_OtHer_Test",       False,      "thisIsAnOtHerTest",        "Test Case 12, first item lower"),
        ("a_b_c_d_e_f_g_h_i_j_k",       False,      "aBCDEFGHIJK",              "Test Case 13, first item lower"),
        ("test_with_2_numbers_1_and_2", False,      "testWith2Numbers1And2",    "Test Case 14, first item lower")
    ])
    def test_snake_case_to_camel_case(self, given_value, first_item_upper, expected_value, msg):
        camel_case: str = snake_case_to_camel_case(given_value, first_item_upper)
        self.assertEqual(expected_value, camel_case, msg)
