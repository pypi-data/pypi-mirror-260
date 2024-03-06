# Python Unittest dataprovider

## Description
Python package to add a `data_provider` decorator to a test function,   
to execute the test with different test values / cases.    
The test function will be executed for each record, which is defined at the `data_provider`.
```python
@data_provider([                    # The DataSet as a List
    (value1, value2, value3),       # Record 1
    (value1, value2, value3)        # Record 2    
    (value1, value2, value3)        # Record 3    
])
```
The data_provider accepts the following Types as argument
- Function
- Dict
- List
- Tuple

> This package is a Python version of the PHP UnitTest dataprovider.   
> https://phpunit.de/manual/3.7/en/writing-tests-for-phpunit.html#writing-tests-for-phpunit.data-providers


## Installation
```commandline
pip install sat_unittest_dataprovider
```
or
```commandline
python -m pip install sat_unittest_dataprovider
```

## Usage

> The test method will be called with the values of the record as arguments   
> **Therefor you need to make sure, to define the same amount of arguments at the test function,**  
> **as you defined values at the record.**
> ```python
> @data_provider([
>     (arg1, arg2, arg3, arg4) 
> ])
> def test_multiply(arg1, arg2, arg3, arg4):
>     ...
>     do someting the arguments
>     ...
> ```

> Without the unittest data provider you would probably create a test like this:
> ```python
> class Test(TestCase):
>     def test_without_dataprovider(self):
>         test_data = [
>             (1, 1, '1 * 1 is 1'),
>             (2, 4, '2 * 2 is 4')
>         ]
>         for row in test_data:
>             given_value, expected_result, msg = row                     # We unpack the tuple here
>             calculated_result = given_value * given_value               # Calculation
>             self.assertEqual(expected_result, calculated_result, msg)   # The Test   
>
>```
 
> The same test with the data_provider decorator would look like this:
> ```python
> class Test(TestCase):
>     @data_provider([
>         (1, 1, '1 * 1 is 1'),
>         (2, 4, '2 * 2 is 4')
>     ])
>     def test_with_dataprovider(self, given_value, expected_result, msg):    # We get all values as function arguments
>         calculated_result = given_value * given_value                       # Calculation
>         self.assertEqual(expected_result, calculated_result, msg)           # The Test
> ```
> This makes the test more readable to others.
***
Simple example:
```python
@data_provider([
    (1, 2, 3, '1 + 2 = 3') 
])
def test_simple_example(self, value, value2, expected, msg):
    self.assertEqual(expected, value + value2, msg)
```
> At the example above, we define 4 values at the record, we want to test a simple number addition.   
> The first argument `value` will be added to the second argument `value2` and we expect,   
> that the calculated result is the same as defined in `expected`.   
> The last argument `msg` is used as a message which will be shown, when the test fails.
***
Example 1:
`DataSet is a List of Tupels`
```python
from unittest import TestCase
from sat_unittest_dataprovider import data_provider

class Test(TestCase):
    
    @data_provider([
        (1, 1, '1 * 1 is 1'), 
        (2, 4, '2 * 2 is 4'),
        (3, 9, '3 * 3 is 9')
    ])
    def test_multiply(self, given, expected, message):
        calculated_result = given * given
        self.assertEqual(expected, calculated_result, message)
```
***
Example 2:
`DataSet is a List with List items`
```python
from unittest import TestCase
from sat_unittest_dataprovider import data_provider

class Test(TestCase):
    
    @data_provider([
        [1, 1, '1 * 1 is 1'], 
        [2, 4, '2 * 2 is 4'],
        [3, 9, '3 * 3 is 9']
    ])
    def test_multiply(self, given, expected, message):
        calculated_result = given * given
        self.assertEqual(expected, calculated_result, message)
```
***
Example 3:
`DataSet is a Function, which should return the test records either as List, Dict or Tuple`    
```python
from unittest import TestCase
from sat_unittest_dataprovider import data_provider

def my_data_set():
    return [
        [1, 1, '1 * 1 is 1'], 
        [2, 4, '2 * 2 is 4'],
        [3, 9, '3 * 3 is 9']
    ] 

class Test(TestCase):
    
    @data_provider(my_data_set)
    def test_multiply(self, given, expected, message):
        calculated_result = given * given
        self.assertEqual(expected, calculated_result, message)

    @data_provider(my_data_set)
    def test_divider(self, divider, given, message):
        expected_result = divider                               # the expected result is the same as the divider
        calculated_result = given / divider
        self.assertEqual(expected_result, calculated_result)    # We don't use the message here, because for this test it doesn't make sense ;-)
```
> In the example above, you can use the data_set function for multiple test cases   
> to reduce code duplication
***
Example 4:
`DataSet is a seperate file`
> For bigger tests you can place the provider functions or values in a separate file   
> 
`test/data_providers.py`
```python
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
```

`test/test_readme_examples.py`
```python
from unittest import TestCase
from sat_unittest_dataprovider import data_provider

from .data_providers import (
    tuples_in_list,
    tuples_in_tuple,
    dict_with_tuples,
    a_dict
)


class Test(TestCase):

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

```
*** 
