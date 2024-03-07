import unittest
from plasma_fhir_client_py import FHIRClient

class TestFHIRClient(unittest.TestCase):
    def test_initialize(self):
        client = FHIRClient.for_no_auth("http://google.com")
        self.assertEqual(client.base_url, "http://google.com")

if __name__ == '__main__':
    unittest.main()
