# //functions/validation_reporting_functions.py
# [Version 08-09-2025 14:40:00]
# Data Validation & Report Generation Functions for TaxOptim AI (MVP Version)
# Authored by: Sotiris Spyrou, CEO, VerityAI

import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ValidationResult:
    """Result of data validation process"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    confidence_score: float
    validation_notes: List[str]

class DataValidator:
    """Comprehensive data validation for tax calculations"""
    
    def __init__(self):
        self.validation_rules = self._load_validation_rules()
        self.hmrc_thresholds = self._load_hmrc_thresholds()
    
    def validate_complete_submission(self, tax_data: Dict) -> ValidationResult:
        """Validate complete tax submission data"""
        
        errors = []
        warnings = []
        notes = []
        
        # Validate income data
        income_validation = self._validate_income_data(tax_data.get('income_breakdown', {}))
        errors.extend(income_validation['errors'])
        warnings.extend(income_validation['warnings'])
        
        # Validate tax calculations
        calculation_validation = self._validate_tax_calculations(tax_data.get('tax_calculations', {}))
        errors.extend(calculation_validation['errors'])
        warnings.extend(calculation_validation['warnings'])
        
        # Validate HMRC compliance
        compliance_validation = self._validate_hmrc_compliance(tax_data)
        errors.extend(compliance_validation['errors'])
        warnings.extend(compliance_validation['warnings'])
        
        # Calculate overall confidence score
        confidence_score = self._calculate_confidence_score(errors, warnings, tax_data)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            confidence_score=confidence_score,
            validation_notes=notes
        )
    
    def _validate_income_data(self, income_data: Dict) -> Dict:
        """Validate income data for completeness and accuracy"""
        
        errors = []
        warnings = []
        
        # Check employment income
        employment = income_data.get('employment', 0)
        if employment < 0:
            errors.append("Employment income cannot be negative")
        elif employment > 1000000:
            warnings.append("Employment income appears unusually high - please verify")
        
        # Check rental income
        rental_data = income_data.get('rental', {})
        if isinstance(rental_data, dict):
            gross_rental = rental_data.get('gross_rental_income', 0)
            expenses = rental_data.get('allowable_expenses', 0)
            
            if gross_rental < 0:
                errors.append("Gross rental income cannot be negative")
            
            if expenses > gross_rental * 1.2:
                warnings.append("Rental expenses appear high relative to income")
        
        return {"errors": errors, "warnings": warnings}
    
    def _validate_tax_calculations(self, tax_calculations: Dict) -> Dict:
        """Validate tax calculation accuracy"""
        
        errors = []
        warnings = []
        
        # Validate income tax calculation
        income_tax_calc = tax_calculations.get('income_tax', {})
        if income_tax_calc:
            gross_income = income_tax_calc.get('gross_income', 0)
            total_tax = income_tax_calc.get('total_tax', 0)
            
            if gross_income > 0:
                effective_rate = total_tax / gross_income
                if effective_rate > 0.5:
                    warnings.append("Effective tax rate appears very high")
                elif effective_rate < 0:
                    errors.append("Effective tax rate cannot be negative")
        
        return {"errors": errors, "warnings": warnings}
    
    def _validate_hmrc_compliance(self, tax_data: Dict) -> Dict:
        """Validate HMRC compliance requirements"""
        
        errors = []
        warnings = []
        
        # Check if Self Assessment required
        total_income = tax_data.get('total_liability', {}).get('income_tax', 0)
        if total_income > 100000:
            warnings.append("Income above £100k - Self Assessment filing required")
        
        return {"errors": errors, "warnings": warnings}
    
    def _calculate_confidence_score(self, errors: List, warnings: List, tax_data: Dict) -> float:
        """Calculate overall confidence score for validation"""
        
        base_score = 1.0
        base_score -= len(errors) * 0.2
        base_score -= len(warnings) * 0.05
        
        return max(0.0, min(1.0, base_score))
    
    def _load_validation_rules(self) -> Dict:
        """Load validation rules for tax data"""
        return {
            "income_limits": {"employment_max": 10000000},
            "rate_limits": {"effective_tax_rate_max": 0.50}
        }
    
    def _load_hmrc_thresholds(self) -> Dict:
        """Load current HMRC thresholds for validation"""
        return {"self_assessment_threshold": 100000}

class ReportGenerator:
    """Generate comprehensive tax reports"""
    
    def __init__(self):
        self.templates = {}
    
    def generate_complete_tax_report(self, tax_data: Dict, validation_result: ValidationResult) -> Dict:
        """Generate complete tax liability report"""
        
        # Generate executive summary
        executive_summary = self._generate_executive_summary(tax_data)
        
        # Generate detailed breakdowns
        income_breakdown = self._generate_income_breakdown(tax_data.get('income_breakdown', {}))
        tax_breakdown = self._generate_tax_breakdown(tax_data.get('tax_calculations', {}))
        
        # Generate next steps
        next_steps = self._generate_next_steps(tax_data, validation_result)
        
        report_data = {
            "report_metadata": {
                "generated_date": datetime.now().isoformat(),
                "tax_year": "2024/25",
                "report_type": "Tax Liability Analysis",
                "validation_status": "Validated" if validation_result.is_valid else "Requires Review"
            },
            "executive_summary": executive_summary,
            "income_breakdown": income_breakdown,
            "tax_breakdown": tax_breakdown,
            "next_steps": next_steps,
            "validation_notes": validation_result.validation_notes,
            "warnings": validation_result.warnings,
            "errors": validation_result.errors
        }
        
        # Generate formatted outputs
        formatted_outputs = {
            "json_export": json.dumps(report_data, indent=2, default=str),
            "text_summary": self._generate_text_summary(report_data)
        }
        
        return {
            "report_data": report_data,
            "formatted_outputs": formatted_outputs
        }
    
    def _generate_executive_summary(self, tax_data: Dict) -> Dict:
        """Generate executive summary of tax position"""
        
        total_liability = tax_data.get('total_liability', {})
        net_tax = tax_data.get('net_total_tax', 0)
        effective_rate = tax_data.get('effective_tax_rate', 0)
        
        return {
            "total_tax_liability": net_tax,
            "effective_tax_rate": f"{effective_rate:.1%}",
            "key_components": {
                "income_tax": total_liability.get('income_tax', 0),
                "national_insurance": total_liability.get('national_insurance', 0),
                "capital_gains_tax": total_liability.get('capital_gains_tax', 0)
            }
        }
    
    def _generate_income_breakdown(self, income_data: Dict) -> Dict:
        """Generate detailed income breakdown"""
        
        breakdown = {}
        
        if income_data.get('employment'):
            breakdown['employment'] = {
                "gross_income": income_data['employment'],
                "description": "Employment income"
            }
        
        return breakdown
    
    def _generate_tax_breakdown(self, tax_calculations: Dict) -> Dict:
        """Generate detailed tax calculation breakdown"""
        
        breakdown = {}
        
        income_tax = tax_calculations.get('income_tax', {})
        if income_tax:
            breakdown['income_tax'] = {
                "taxable_income": income_tax.get('taxable_income', 0),
                "total_income_tax": income_tax.get('total_tax', 0)
            }
        
        return breakdown
    
    def _generate_next_steps(self, tax_data: Dict, validation_result: ValidationResult) -> List[str]:
        """Generate next steps based on analysis"""
        
        steps = []
        
        if not validation_result.is_valid:
            steps.append("Review and address validation errors before proceeding")
        
        steps.extend([
            "Review calculations and verify input data",
            "Consider professional tax advice for complex areas",
            "Plan for tax payment and filing deadlines"
        ])
        
        return steps
    
    def _generate_text_summary(self, report_data: Dict) -> str:
        """Generate human-readable text summary"""
        
        summary = f"""
TAX OPTIMIZATION AI - SUMMARY REPORT
Generated: {report_data['report_metadata']['generated_date']}

EXECUTIVE SUMMARY:
Total Tax Liability: £{report_data['executive_summary']['total_tax_liability']:,.2f}
Effective Tax Rate: {report_data['executive_summary']['effective_tax_rate']}

NEXT STEPS:
"""
        
        for step in report_data['next_steps']:
            summary += f"- {step}\n"
        
        return summary

# Main workflow function
def run_complete_validation_and_reporting(tax_calculation_result: Dict, anthropic_api_key: str = None) -> Dict:
    """Complete validation and reporting workflow"""
    
    # Run validation
    validator = DataValidator()
    validation_result = validator.validate_complete_submission(tax_calculation_result)
    
    # Generate reports
    report_generator = ReportGenerator()
    report_package = report_generator.generate_complete_tax_report(
        tax_calculation_result, validation_result
    )
    
    return {
        "validation_result": validation_result.__dict__,
        "report_package": report_package,
        "processing_summary": {
            "validation_passed": validation_result.is_valid,
            "confidence_score": validation_result.confidence_score,
            "errors_count": len(validation_result.errors),
            "warnings_count": len(validation_result.warnings),
            "report_generated": True
        }
    }
