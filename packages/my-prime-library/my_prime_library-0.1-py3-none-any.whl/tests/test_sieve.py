import unittest
from my_prime_library.sieve import sieve_of_eratosthenes

class TestSieveOfEratosthenes(unittest.TestCase):
    def test_sieve(self):
        self.assertEqual(sieve_of_eratosthenes(30), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])

if __name__ == "__main__":
    unittest.main()
