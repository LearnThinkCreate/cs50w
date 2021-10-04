import unittest
from func import is_prime

class Tests(unittest.TestCase):

    def test_one(self):
        """Check that 1 is not prime""" 
        self.assertFalse(is_prime(1))

    def test_min(self):
        """Check that 2 is prime"""
        self.assertTrue(is_prime(2))

    def test_even(self):
        """Check that 8 is not prime"""
        self.assertFalse(is_prime(8))

    def test_prime(self):
        """Check that 11 is prime"""
        self.assertTrue(is_prime(11))

    def test_square(self):
        """Check that 25 is not prime"""
        self.assertFalse(is_prime(25))


if __name__ == "__main__":
        """Run all the unit test"""
        unittest.main()