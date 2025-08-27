#!/usr/bin/env python3
"""
Unit tests for PII Detection and Redaction Tool
"""

import unittest
import json
import tempfile
import os
import sys
from io import StringIO

# Add parent directory to path to import the main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from detector_varikuti_Narendra_Reddy import (
    redact_phone, redact_aadhar, redact_passport, 
    redact_name, redact_email, process_record
)


class TestPIIRedaction(unittest.TestCase):
    """Test cases for PII redaction functions"""

    def test_redact_phone(self):
        """Test phone number redaction"""
        test_cases = [
            ("9876543210", "98XXXXXX10"),
            ("1234567890", "12XXXXXX90"),
            ("5555555555", "55XXXXXX55"),
        ]
        
        for input_phone, expected in test_cases:
            with self.subTest(input_phone=input_phone):
                result = redact_phone(input_phone)
                self.assertEqual(result, expected)

    def test_redact_aadhar(self):
        """Test Aadhar number redaction"""
        test_cases = [
            ("1234 5678 9012", "XXXXXXXX9012"),
            ("9876 5432 1098", "XXXXXXXX1098"),
            ("4567 8901 2345", "XXXXXXXX2345"),
        ]
        
        for input_aadhar, expected in test_cases:
            with self.subTest(input_aadhar=input_aadhar):
                result = redact_aadhar(input_aadhar)
                self.assertEqual(result, expected)

    def test_redact_passport(self):
        """Test passport number redaction"""
        test_cases = [
            ("A1234567", "AXXXXXX7"),
            ("B9876543", "BXXXXXX3"),
            ("C4567890", "CXXXXXX0"),
        ]
        
        for input_passport, expected in test_cases:
            with self.subTest(input_passport=input_passport):
                result = redact_passport(input_passport)
                self.assertEqual(result, expected)

    def test_redact_name(self):
        """Test name redaction"""
        test_cases = [
            ("John Doe", "JXXX DXX"),
            ("Jane Smith", "JXXX SXXXX"),
            ("A", "A"),
            ("", ""),
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = redact_name(input_name)
                self.assertEqual(result, expected)

    def test_redact_email(self):
        """Test email redaction"""
        test_cases = [
            ("john.doe@example.com", "jXXXe@example.com"),
            ("test@domain.com", "tXXXt@domain.com"),
            ("a@b.com", "X@b.com"),
            ("ab@c.com", "XX@c.com"),
        ]
        
        for input_email, expected in test_cases:
            with self.subTest(input_email=input_email):
                result = redact_email(input_email)
                self.assertEqual(result, expected)

    def test_process_record_standalone_pii(self):
        """Test processing records with standalone PII"""
        # Test phone number detection
        data = {"phone": "9876543210"}
        redacted, is_pii = process_record(data)
        self.assertTrue(is_pii)
        self.assertEqual(redacted["phone"], "98XXXXXX10")

        # Test Aadhar detection
        data = {"aadhar": "1234 5678 9012"}
        redacted, is_pii = process_record(data)
        self.assertTrue(is_pii)
        self.assertEqual(redacted["aadhar"], "XXXXXXXX9012")

        # Test passport detection
        data = {"passport": "A1234567"}
        redacted, is_pii = process_record(data)
        self.assertTrue(is_pii)
        self.assertEqual(redacted["passport"], "AXXXXXX7")

        # Test UPI detection
        data = {"upi_id": "user@upi"}
        redacted, is_pii = process_record(data)
        self.assertTrue(is_pii)
        self.assertEqual(redacted["upi_id"], "[REDACTED_UPI]")

    def test_process_record_combinatorial_pii(self):
        """Test processing records with combinatorial PII"""
        # Test name + email + address combination
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "address": "123 Main Street, City"
        }
        redacted, is_pii = process_record(data)
        self.assertTrue(is_pii)
        self.assertEqual(redacted["name"], "JXXX DXX")
        self.assertEqual(redacted["email"], "jXXXn@example.com")
        self.assertEqual(redacted["address"], "[REDACTED_ADDRESS]")

        # Test device context combination (both ip_address and device_id together)
        data = {
            "ip_address": "192.168.1.100",
            "device_id": "DEVICE_001"
        }
        redacted, is_pii = process_record(data)
        # The current logic doesn't trigger combinatorial PII for device context alone
        # So we expect no PII detection for this case
        self.assertFalse(is_pii)
        self.assertEqual(redacted["ip_address"], "192.168.1.100")
        self.assertEqual(redacted["device_id"], "DEVICE_001")

    def test_process_record_no_pii(self):
        """Test processing records without PII"""
        data = {
            "age": "25",
            "city": "Mumbai",
            "occupation": "Engineer"
        }
        redacted, is_pii = process_record(data)
        self.assertFalse(is_pii)
        self.assertEqual(redacted, data)

    def test_process_record_edge_cases(self):
        """Test edge cases in record processing"""
        # Empty data
        data = {}
        redacted, is_pii = process_record(data)
        self.assertFalse(is_pii)
        self.assertEqual(redacted, {})

        # Non-string values
        data = {"age": 25, "active": True}
        redacted, is_pii = process_record(data)
        self.assertFalse(is_pii)
        self.assertEqual(redacted, data)

        # Empty string values
        data = {"name": "", "email": "   "}
        redacted, is_pii = process_record(data)
        self.assertFalse(is_pii)
        self.assertEqual(redacted, data)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow"""

    def test_csv_processing_workflow(self):
        """Test the complete CSV processing workflow"""
        # Create a temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("record_id,data_json\n")
            f.write('1,"{"name": "John Doe", "phone": "9876543210"}"\n')
            f.write('2,"{"email": "test@example.com", "address": "123 Main St"}"\n')
            temp_input = f.name

        try:
            # Import and run the main function
            from detector_varikuti_Narendra_Reddy import main
            
            # Create temporary output file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
                temp_output = f.name

            # Run the main function
            main(temp_input, temp_output)

            # Verify output file was created
            self.assertTrue(os.path.exists(temp_output))

            # Read and verify output
            with open(temp_output, 'r') as f:
                lines = f.readlines()
                self.assertEqual(len(lines), 3)  # Header + 2 data rows
                
                # Check header
                self.assertIn("record_id", lines[0])
                self.assertIn("redacted_data_json", lines[0])
                self.assertIn("is_pii", lines[0])

        finally:
            # Clean up temporary files
            if os.path.exists(temp_input):
                os.unlink(temp_input)
            if os.path.exists(temp_output):
                os.unlink(temp_output)


def run_tests():
    """Run all tests with verbose output"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestPIIRedaction))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("Running PII Detection Tool Tests...")
    print("=" * 50)
    
    success = run_tests()
    
    print("=" * 50)
    if success:
        print("All tests passed!")
        sys.exit(0)
    else:
        print("Some tests failed!")
        sys.exit(1)
