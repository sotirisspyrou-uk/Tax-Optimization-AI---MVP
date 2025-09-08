# //functions/uk_tax_calculations.py
# [Version 08-09-2025 14:30:00]
# UK Tax Calculation Functions for TaxOptim AI
# Authored by: Sotiris Spyrou, CEO, VerityAI

import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class TaxThresholds:
    """2024/25 UK Tax Year Thresholds"""
    personal_allowance: float = 12570
    basic_rate_threshold: float = 50270
    higher_rate_threshold: float = 125140
    basic_rate: float = 0.20
    higher_rate: float = 0.40
    additional_rate: float = 0.45
    ni_threshold: float = 12570
    ni_upper_threshold: float = 50270
    ni_basic_rate: float = 0.12
    ni_higher_rate: float = 0.02
    cgt_allowance: float = 6000
    cgt_basic_rate: float = 0.10
    cgt_higher_rate: float = 0.20
    cgt_property_basic: float = 0.18
    cgt_property_higher: float = 0.24
    dividend_allowance: float = 1000
    isa_allowance: float = 20000
    pension_annual_allowance: float = 60000

class UKTaxCalculator:
    """Comprehensive UK Tax Calculation Engine"""
    
    def __init__(self):
        self.thresholds = TaxThresholds()
        
    def calculate_income_tax(self, 
                           gross_income: float, 
                           pension_contributions: float = 0,
                           gift_aid_donations: float = 0,
                           personal_allowance_adjustment: float = 0) -> Dict:
        """Calculate income tax liability with reliefs and allowances"""
        
        # Calculate adjusted gross income after pension relief
        adjusted_gross_income = gross_income - pension_contributions
        
        # Apply Gift Aid gross-up for band extension
        gift_aid_gross = gift_aid_donations * 1.25  # Gross up net donations
        extended_income = adjusted_gross_income + gift_aid_gross
        
        # Calculate personal allowance (tapered for high earners)
        personal_allowance = self._calculate_personal_allowance(
            adjusted_gross_income, personal_allowance_adjustment
        )
        
        # Calculate taxable income
        taxable_income = max(0, adjusted_gross_income - personal_allowance)
        
        # Calculate tax bands with Gift Aid extension
        basic_rate_limit = self.thresholds.basic_rate_threshold + gift_aid_gross
        higher_rate_limit = self.thresholds.higher_rate_threshold + gift_aid_gross
        
        # Calculate tax by bands
        tax_breakdown = self._calculate_tax_bands(
            taxable_income, basic_rate_limit, higher_rate_limit
        )
        
        return {
            "gross_income": gross_income,
            "pension_contributions": pension_contributions,
            "gift_aid_donations": gift_aid_donations,
            "gift_aid_gross": gift_aid_gross,
            "personal_allowance": personal_allowance,
            "taxable_income": taxable_income,
            "tax_bands": tax_breakdown,
            "total_tax": sum(tax_breakdown.values()),
            "effective_rate": sum(tax_breakdown.values()) / gross_income if gross_income > 0 else 0,
            "marginal_rate": self._calculate_marginal_rate(extended_income)
        }
    
    def calculate_national_insurance(self, 
                                   employment_income: float,
                                   self_employment_income: float = 0) -> Dict:
        """Calculate National Insurance contributions"""
        
        # Class 1 Employee NI
        class1_employee = 0
        if employment_income > self.thresholds.ni_threshold:
            # Basic rate band
            basic_band = min(employment_income, self.thresholds.ni_upper_threshold) - self.thresholds.ni_threshold
            class1_employee += basic_band * self.thresholds.ni_basic_rate
            
            # Higher rate band
            if employment_income > self.thresholds.ni_upper_threshold:
                higher_band = employment_income - self.thresholds.ni_upper_threshold
                class1_employee += higher_band * self.thresholds.ni_higher_rate
        
        # Class 2 Self-Employed NI (£3.45 per week if profits between £6,515-£50,270)
        class2_self_employed = 0
        if 6515 <= self_employment_income <= 50270:
            class2_self_employed = 3.45 * 52  # £179.40 annually
        
        # Class 4 Self-Employed NI
        class4_self_employed = 0
        if self_employment_income > self.thresholds.ni_threshold:
            # Basic rate band
            basic_band = min(self_employment_income, self.thresholds.ni_upper_threshold) - self.thresholds.ni_threshold
            class4_self_employed += basic_band * 0.09  # 9% rate for Class 4
            
            # Higher rate band
            if self_employment_income > self.thresholds.ni_upper_threshold:
                higher_band = self_employment_income - self.thresholds.ni_upper_threshold
                class4_self_employed += higher_band * self.thresholds.ni_higher_rate
        
        return {
            "employment_income": employment_income,
            "self_employment_income": self_employment_income,
            "class1_employee": class1_employee,
            "class2_self_employed": class2_self_employed,
            "class4_self_employed": class4_self_employed,
            "total_ni": class1_employee + class2_self_employed + class4_self_employed
        }
    
    def calculate_capital_gains_tax(self, 
                                  gains_and_losses: List[Dict],
                                  annual_exempt_amount: float = None) -> Dict:
        """Calculate Capital Gains Tax liability"""
        
        if annual_exempt_amount is None:
            annual_exempt_amount = self.thresholds.cgt_allowance
        
        # Separate property and other gains
        property_gains = []
        other_gains = []
        total_losses = 0
        
        for item in gains_and_losses:
            if item['type'] == 'property':
                if item['amount'] > 0:
                    property_gains.append(item['amount'])
                else:
                    total_losses += abs(item['amount'])
            else:
                if item['amount'] > 0:
                    other_gains.append(item['amount'])
                else:
                    total_losses += abs(item['amount'])
        
        # Calculate net gains
        total_property_gains = sum(property_gains)
        total_other_gains = sum(other_gains)
        total_gross_gains = total_property_gains + total_other_gains
        
        # Apply losses
        net_gains_after_losses = max(0, total_gross_gains - total_losses)
        
        # Apply annual exempt amount
        taxable_gains = max(0, net_gains_after_losses - annual_exempt_amount)
        
        # Calculate tax (simplified - assumes basic rate taxpayer)
        property_tax = min(taxable_gains, total_property_gains) * self.thresholds.cgt_property_basic
        other_tax = max(0, taxable_gains - total_property_gains) * self.thresholds.cgt_basic_rate
        
        return {
            "total_gross_gains": total_gross_gains,
            "total_losses": total_losses,
            "net_gains_after_losses": net_gains_after_losses,
            "annual_exempt_amount_used": min(annual_exempt_amount, net_gains_after_losses),
            "taxable_gains": taxable_gains,
            "property_tax": property_tax,
            "other_gains_tax": other_tax,
            "total_cgt": property_tax + other_tax
        }
    
    def calculate_rental_income_tax(self, 
                                  gross_rental_income: float,
                                  allowable_expenses: float,
                                  mortgage_interest: float,
                                  property_allowance_election: bool = False) -> Dict:
        """Calculate rental income tax with mortgage interest relief"""
        
        if property_allowance_election:
            # Use property allowance instead of actual expenses
            net_rental_income = max(0, gross_rental_income - 1000)
            mortgage_interest_relief = 0  # No mortgage relief with property allowance
            actual_expenses_used = 0
        else:
            # Use actual expenses
            net_rental_income = gross_rental_income - allowable_expenses
            mortgage_interest_relief = mortgage_interest * 0.20  # 20% tax credit
            actual_expenses_used = allowable_expenses
        
        # Taxable rental profit (before mortgage interest relief)
        taxable_rental_profit = max(0, net_rental_income)
        
        return {
            "gross_rental_income": gross_rental_income,
            "allowable_expenses": actual_expenses_used,
            "property_allowance_used": 1000 if property_allowance_election else 0,
            "net_rental_income": net_rental_income,
            "taxable_rental_profit": taxable_rental_profit,
            "mortgage_interest": mortgage_interest,
            "mortgage_interest_relief": mortgage_interest_relief,
            "property_allowance_election": property_allowance_election
        }
    
    def calculate_dividend_tax(self, 
                             dividend_income: float,
                             total_income: float) -> Dict:
        """Calculate dividend tax with allowance and appropriate rates"""
        
        # Apply dividend allowance
        taxable_dividends = max(0, dividend_income - self.thresholds.dividend_allowance)
        
        # Determine tax rates based on total income position
        basic_rate_remaining = max(0, self.thresholds.basic_rate_threshold - 
                                 (total_income - dividend_income))
        
        dividend_basic_rate = 0.0875  # 8.75%
        dividend_higher_rate = 0.3375  # 33.75%
        dividend_additional_rate = 0.3925  # 39.25%
        
        # Calculate tax by bands
        tax = 0
        remaining_dividends = taxable_dividends
        
        # Basic rate band
        basic_rate_dividends = min(remaining_dividends, basic_rate_remaining)
        tax += basic_rate_dividends * dividend_basic_rate
        remaining_dividends -= basic_rate_dividends
        
        # Higher rate band
        higher_rate_limit = self.thresholds.higher_rate_threshold - self.thresholds.basic_rate_threshold
        higher_rate_dividends = min(remaining_dividends, higher_rate_limit)
        tax += higher_rate_dividends * dividend_higher_rate
        remaining_dividends -= higher_rate_dividends
        
        # Additional rate band
        tax += remaining_dividends * dividend_additional_rate
        
        return {
            "dividend_income": dividend_income,
            "dividend_allowance_used": min(dividend_income, self.thresholds.dividend_allowance),
            "taxable_dividends": taxable_dividends,
            "dividend_tax": tax,
            "effective_dividend_rate": tax / dividend_income if dividend_income > 0 else 0
        }
    
    def _calculate_personal_allowance(self, income: float, adjustment: float = 0) -> float:
        """Calculate personal allowance with high income taper"""
        base_allowance = self.thresholds.personal_allowance + adjustment
        
        # Taper starts at £100,000
        if income > 100000:
            reduction = (income - 100000) * 0.5
            return max(0, base_allowance - reduction)
        
        return base_allowance
    
    def _calculate_tax_bands(self, taxable_income: float, 
                           basic_rate_limit: float, 
                           higher_rate_limit: float) -> Dict:
        """Calculate tax across different rate bands"""
        bands = {
            "basic_rate_tax": 0,
            "higher_rate_tax": 0,
            "additional_rate_tax": 0
        }
        
        remaining_income = taxable_income
        
        # Basic rate band
        basic_rate_income = min(remaining_income, basic_rate_limit)
        bands["basic_rate_tax"] = basic_rate_income * self.thresholds.basic_rate
        remaining_income -= basic_rate_income
        
        # Higher rate band
        if remaining_income > 0:
            higher_rate_income = min(remaining_income, higher_rate_limit - basic_rate_limit)
            bands["higher_rate_tax"] = higher_rate_income * self.thresholds.higher_rate
            remaining_income -= higher_rate_income
        
        # Additional rate band
        if remaining_income > 0:
            bands["additional_rate_tax"] = remaining_income * self.thresholds.additional_rate
        
        return bands
    
    def _calculate_marginal_rate(self, income: float) -> float:
        """Calculate marginal tax rate at given income level"""
        if income <= self.thresholds.personal_allowance:
            return 0.0
        elif income <= self.thresholds.basic_rate_threshold:
            return self.thresholds.basic_rate
        elif income <= self.thresholds.higher_rate_threshold:
            return self.thresholds.higher_rate
        else:
            return self.thresholds.additional_rate

def calculate_comprehensive_tax_liability(income_data: Dict) -> Dict:
    """Master function to calculate complete UK tax liability"""
    
    calculator = UKTaxCalculator()
    
    # Extract income components
    employment_income = income_data.get('employment_income', 0)
    rental_income_data = income_data.get('rental_income', {})
    investment_income = income_data.get('investment_income', {})
    capital_gains = income_data.get('capital_gains', [])
    
    # Calculate rental income tax
    rental_tax_calc = calculator.calculate_rental_income_tax(
        gross_rental_income=rental_income_data.get('gross_income', 0),
        allowable_expenses=rental_income_data.get('expenses', 0),
        mortgage_interest=rental_income_data.get('mortgage_interest', 0),
        property_allowance_election=rental_income_data.get('property_allowance_election', False)
    )
    
    # Calculate dividend tax
    dividend_income = investment_income.get('dividends', 0)
    total_income = employment_income + rental_tax_calc['taxable_rental_profit'] + dividend_income
    
    dividend_tax_calc = calculator.calculate_dividend_tax(dividend_income, total_income)
    
    # Calculate main income tax
    income_tax_calc = calculator.calculate_income_tax(
        gross_income=employment_income + rental_tax_calc['taxable_rental_profit'],
        pension_contributions=income_data.get('pension_contributions', 0),
        gift_aid_donations=income_data.get('gift_aid_donations', 0)
    )
    
    # Calculate National Insurance
    ni_calc = calculator.calculate_national_insurance(
        employment_income=employment_income,
        self_employment_income=income_data.get('self_employment_income', 0)
    )
    
    # Calculate Capital Gains Tax
    cgt_calc = calculator.calculate_capital_gains_tax(capital_gains)
    
    # Compile total liability
    total_liability = {
        "income_tax": income_tax_calc['total_tax'],
        "dividend_tax": dividend_tax_calc['dividend_tax'],
        "national_insurance": ni_calc['total_ni'],
        "capital_gains_tax": cgt_calc['total_cgt'],
        "mortgage_interest_relief": rental_tax_calc['mortgage_interest_relief']
    }
    
    net_total_tax = (total_liability["income_tax"] + 
                    total_liability["dividend_tax"] + 
                    total_liability["national_insurance"] + 
                    total_liability["capital_gains_tax"] - 
                    total_liability["mortgage_interest_relief"])
    
    return {
        "calculation_date": datetime.now().isoformat(),
        "tax_year": "2024/25",
        "income_breakdown": {
            "employment": employment_income,
            "rental": rental_tax_calc,
            "dividends": dividend_tax_calc,
            "capital_gains": cgt_calc
        },
        "tax_calculations": {
            "income_tax": income_tax_calc,
            "national_insurance": ni_calc,
            "dividend_tax": dividend_tax_calc,
            "capital_gains_tax": cgt_calc
        },
        "total_liability": total_liability,
        "net_total_tax": net_total_tax,
        "effective_tax_rate": net_total_tax / total_income if total_income > 0 else 0
    }
