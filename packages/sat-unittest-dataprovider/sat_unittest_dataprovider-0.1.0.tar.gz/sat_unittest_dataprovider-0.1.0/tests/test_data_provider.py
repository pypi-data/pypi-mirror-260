from unittest import TestCase
from sat_unittest_dataprovider import data_provider


class Test(TestCase):

    def test_raises_AttributeError_if_data_set_is_not_supported(self):
        string_provider: str = "This is a string"

        with self.assertRaises(AttributeError) as error:
            @data_provider(string_provider)
            def test_func():
                pass
            test_func()

        expected_msg = "data_set must be of type [Function, List, Dict, Tuple], got 'Str'"
        current_msg = str(error.exception)
        self.assertEqual(expected_msg, current_msg)

    @data_provider([('given_value', 'expected_value', 'the_message')])
    def test_data_provider_passes_all_values(self, given, expected, msg):
        self.assertEqual(given, 'given_value')
        self.assertEqual(expected, 'expected_value')
        self.assertEqual(msg, 'the_message')

    @data_provider([
        (1, 1),
        (2, 4),
        (3, 9),
        (4, 16),
        (8, 64)
    ])
    def test_data_provider_is_executed(self, given, expected):
        c = given * given
        self.assertEqual(expected, c)
        return c

    def test_data_provider_can_handle_functions_as_data_set(self):
        def data_p_as_func() -> list[tuple[str, str]]:
            return [
                ('test1', 'TEST1'), ('test2', 'TEST2'), ('TEST3', 'TEST3'),
            ]

        @data_provider(data_p_as_func)
        def test_fun(*args):
            expected: str = args[1]
            given: str = args[0]
            self.assertEqual(expected, given.upper())

        test_fun()
