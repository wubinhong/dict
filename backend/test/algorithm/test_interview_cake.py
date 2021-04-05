from datetime import datetime
from typing import List
from unittest import TestCase

from bson import json_util
from web.util import get_logger

log = get_logger(__name__)

# All the following test cases come from https://www.interviewcake.com/table-of-contents


class TestAlgorithmicThinking(TestCase):
    """
    Intro for some basic algorithmic knowledge
    """

    # This section is about O(x) complexity in time and space.
    @staticmethod
    def print_first_item(items: list):
        """
        O(1)
        """
        log.info(items[0])

    def print_all_items(self, items: list):
        """
        O(n)
        """
        for item in items:
            log.info(item)

    def print_all_possible_ordered_pairs(self, items: list):
        """
        O(n2)
        """
        for first_item in items:
            for second_item in items:
                log.info('%s, %s', first_item, second_item)

    def say_hi_n_times(self, n: int):
        """
        O(1) - N could be the actual input, or the size of the input
        """
        for time in range(n):
            log.info('say hi: %s', time)

    def print_all_items_twice(self, items: list):
        """
        O(2n) --> we just cll O(n)
        """
        for item in items:
            log.info(item)
        # Once more, with feeling
        for item in items:
            log.info(item)

    def print_first_item_then_first_half_then_say_hi_100_times(self, items: list):
        """
        O(1 + n/2 + 100) --> O(n)
        """
        log.info(items[0])
        middle_index = len(items) / 2
        index = 0
        while index < middle_index:
            log.info(items[index])
            index += 1
        for time in range(100):
            log.info('Say hi: %s', time)

    def print_all_member_then_all_pair_sums(self, numbers: list):
        """
        Drop the less significant terms.
        e.g. O(n + n2) --> O(n2); Even for O(n2/2 + 100n) --> O(n2)
        """
        log.info('Drop the less significant terms')
        print('These are the numbers:')
        for number in numbers:
            print(number)

        print('And these are their sums')
        for first_number in numbers:
            for second_number in numbers:
                print('%s + %s = %s' % (first_number, second_number, first_number + second_number))

    def contains(self, haystack: List[int], needle: int):
        """
        We're usually talking about the "worst case"
        """
        log.info('Method contains...')
        index = 0
        for item in haystack:
            print('Search times: %s' % index)
            index += 1
            if item == needle:
                return True
        return False
    
    def list_of_hi_n_times(self, n: int):
        """
        Space complexity: the final frontier.
        The size of hi_list scales with the size of the input
        """
        log.info('Demonstrate space complexity for input')
        hi_list = []
        for time in range(n):
            hi_list.append('hi[%s] ' % time)
        return hi_list
    
    def get_largest_item(self, items: List[float]):
        """
        Usually when we talk about space complexity, we're talking about additioanl space,
        so we don't include space taken up by the input.
        This method's space complexity is O(1), while time complexity is O(n) in the worset case.
        """
        largest = float('-inf')
        for item in items:
            if item > largest:
                largest = item
        return largest

    def test_big_o_notation(self):
        """
        Get the idea behind big O notation by demonstrating some kinds of coding.
        """
        items = ['a', 'b', 1]
        TestAlgorithmicThinking.print_first_item(items)
        self.print_all_items(items)
        self.print_all_possible_ordered_pairs(items)
        self.say_hi_n_times(len(items))
        # Drop the constants
        self.print_all_items_twice(items)
        self.print_first_item_then_first_half_then_say_hi_100_times(items)
        numbers = [1, 2, 3, 8, 4]
        self.print_all_member_then_all_pair_sums(numbers)
        log.info('Contains method result: %s', self.contains(numbers, 3))
        log.info('Space complexity: %s', self.list_of_hi_n_times(4))
        log.info('Result of get_largest_item: %s', self.get_largest_item(numbers))

    # The next section is all about Data Structure.


class TestArrayStrManipulation(TestCase):
    """
    Test case for Array and string manipulation
    """

    def test_datetime(self):
        # ff
        pass
