import unittest
from plasma_fhir_client_py import add_one

class TestExample(unittest.TestCase):
    def test_add_one(self):
        self.assertEqual(add_one(1), 2)

if __name__ == '__main__':
    unittest.main()
