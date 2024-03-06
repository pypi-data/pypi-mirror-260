from unittest import TestCase
from sat_unittest_dataprovider import data_provider
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
