import sys
import unittest

class Animal(object):

    def __init__(self, name, num_legs):
        self.name = name
        self.num_legs = num_legs

    def get_num_legs():
        return self.num_legs

    def get_name():
        return self.name


class Dog(Animal):

    def __init__(self, name, num_legs):
        super(Dog, self).__init__(name, num_legs)


class TestInheritance(unittest.TestCase):

    def test_inheritance(self):
        d = Dog("Spot", 4)
        self.assertEqual('Spot', d.name)
        self.assertEqual(4, d.num_legs)


unittest.main()




