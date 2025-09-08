# //tests/test_basic.py
# [Version 08-09-2025 15:00:00]
# Basic Test Suite for Tax Optimization AI
# Authored by: Sotiris Spyrou, CEO, VerityAI

import sys
import os
import unittest

# Add functions directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'functions'))

from uk_tax_calculations import UKTaxCalculator, calculate_comprehensive_tax_liability

class TestTaxCalculations(unittest.TestCase):
    """Test UK tax calculation functions"""
    
    def setUp(self):
        self.calculator = UKTaxCalculator()
    
    def test_basic_income_tax(self):
        """Test basic income tax calculation"""
        result = self.calculator.calculate_income_tax(50000)
        
        # Should have personal allowance
        self.assertEqual(result['personal_allowance'], 12570)
        
        # Should have taxable income
        self.assertEqual(result['taxable_income'], 37430)
        
        # Should have basic rate tax
        self.assertGreater(result['total_tax'], 0)
    
    def test_national_insurance(self):
        """Test National Insurance calculation"""
        result = self.calculator.calculate_national_insurance(50000)
        
        self.assertEqual(result['employment_income'], 50000)
        self.assertGreater(result['class1_employee'], 0)
        self.assertEqual(result['total_ni'], result['class1_employee'])
    
    def test_comprehensive_calculation(self):
        """Test comprehensive tax liability calculation"""
        income_data = {
            'employment_income': 50000,
            'pension_contributions': 5000
        }
        
        result = calculate_comprehensive_tax_liability(income_data)
        
        self.assertIn('tax_year', result)
        self.assertEqual(result['tax_year'], '2024/25')
        self.assertIn('net_total_tax', result)
        self.assertGreater(result['net_total_tax'], 0)

if __name__ == '__main__':
    unittest.main()
