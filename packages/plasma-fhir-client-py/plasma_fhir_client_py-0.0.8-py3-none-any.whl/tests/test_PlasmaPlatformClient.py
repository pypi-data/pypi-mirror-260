import unittest
from plasma_fhir_client_py import PlasmaPlatformClient

class TestPlasmaPlatformClient(unittest.TestCase):
    def test_initialize(self):
        client = PlasmaPlatformClient.initialize("http://google.com", "state", "code", "project_id", "environment_id")
        self.assertEqual(client.plasma_base_url, "http://google.com")

if __name__ == '__main__':
    unittest.main()
