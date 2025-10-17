import unittest
from scanner_core import Scanner

class TestScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = Scanner()
    
    def test_scanner_init(self):
        self.assertIsNotNone(self.scanner)
        self.assertEqual(self.scanner.name, "Code Location Scanner")
        self.assertEqual(self.scanner.version, "1.0.0")
    
    def test_get_info(self):
        info = self.scanner.get_info()
        self.assertIn("Code Location Scanner", info)
        self.assertIn("1.0.0", info)
    
    def test_scan_directory(self):
        # Test scanning current directory
        results = self.scanner.scan_directory(".")
        self.assertIsInstance(results, list)

if __name__ == '__main__':
    unittest.main()