#!/usr/bin/env python3
# main.py
# [Version 08-09-2025 15:00:00]
# Tax Optimization AI - Main Entry Point
# Authored by: Sotiris Spyrou, CEO, VerityAI

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Optional
import argparse

# Add functions directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'functions'))

# Import core modules
try:
    from uk_tax_calculations import calculate_comprehensive_tax_liability
    from document_processing_tools import DocumentProcessor, batch_process_documents
    from validation_reporting_functions import run_complete_validation_and_reporting
    from optimization_engine_functions import generate_comprehensive_optimization_plan
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("💡 Ensure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)

def load_environment():
    """Load environment variables from .env file"""
    env_file = '.env'
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    
    # Check for required API key
    if not os.getenv('CLAUDE_API_KEY'):
        print("❌ CLAUDE_API_KEY not found in environment")
        print("💡 Please create a .env file with your Claude API key")
        print("📝 Copy .env.example to .env and add your API key")
        sys.exit(1)

def interactive_mode():
    """Run interactive tax optimization workflow"""
    print("\n🎯 Tax Optimization AI - Interactive Mode")
    print("=" * 50)
    
    # Step 1: Document Collection
    print("\n📄 Step 1: Document Processing")
    document_files = []
    
    while True:
        file_path = input("Enter document file path (or 'done' to continue): ").strip()
        if file_path.lower() == 'done':
            break
        if file_path and os.path.exists(file_path):
            document_files.append(file_path)
            print(f"✅ Added: {file_path}")
        else:
            print("❌ File not found. Please check the path.")
    
    if not document_files:
        print("⚠️  No documents provided. Using manual input mode.")
        return manual_input_mode()
    
    # Process documents
    print(f"\n🔄 Processing {len(document_files)} documents...")
    try:
        api_key = os.getenv('CLAUDE_API_KEY')
        results = batch_process_documents(document_files, api_key)
        
        # Extract and consolidate data
        income_data = consolidate_extracted_data(results)
        print("✅ Document processing complete")
        
    except Exception as e:
        print(f"❌ Document processing failed: {e}")
        return manual_input_mode()
    
    # Step 2: Tax Calculation
    return process_tax_calculation(income_data)

def manual_input_mode():
    """Manual data input mode"""
    print("\n✏️  Manual Input Mode")
    print("Please enter your tax information:")
    
    income_data = {}
    
    # Employment income
    employment = input("Employment income (£): ").strip()
    if employment:
        income_data['employment_income'] = float(employment)
    
    # Rental income
    rental_income = input("Gross rental income (£, optional): ").strip()
    if rental_income:
        rental_expenses = input("Rental expenses (£): ").strip() or "0"
        mortgage_interest = input("Mortgage interest (£): ").strip() or "0"
        
        income_data['rental_income'] = {
            'gross_income': float(rental_income),
            'expenses': float(rental_expenses),
            'mortgage_interest': float(mortgage_interest)
        }
    
    # Investment income
    dividends = input("Dividend income (£, optional): ").strip()
    if dividends:
        income_data['investment_income'] = {
            'dividends': float(dividends)
        }
    
    # Deductions
    pension = input("Pension contributions (£, optional): ").strip()
    if pension:
        income_data['pension_contributions'] = float(pension)
    
    gift_aid = input("Gift Aid donations (£, optional): ").strip()
    if gift_aid:
        income_data['gift_aid_donations'] = float(gift_aid)
    
    return process_tax_calculation(income_data)

def consolidate_extracted_data(extraction_results: Dict) -> Dict:
    """Consolidate data from multiple document extractions"""
    income_data = {
        'employment_income': 0,
        'rental_income': {'gross_income': 0, 'expenses': 0, 'mortgage_interest': 0},
        'investment_income': {'dividends': 0},
        'pension_contributions': 0,
        'gift_aid_donations': 0,
        'capital_gains': []
    }
    
    for file_path, result in extraction_results.items():
        if 'error' in result:
            print(f"⚠️  Skipping {file_path}: {result['error']}")
            continue
        
        extracted_data = result.get('extracted_data', {})
        
        # Consolidate income streams
        for income in extracted_data.get('income_streams', []):
            if income['type'] == 'Employment':
                income_data['employment_income'] += income.get('amount', 0)
            elif income['type'] == 'Rental':
                income_data['rental_income']['gross_income'] += income.get('amount', 0)
            elif income['type'] == 'Investment':
                income_data['investment_income']['dividends'] += income.get('amount', 0)
        
        # Consolidate expenses
        for expense in extracted_data.get('expenses', []):
            if expense.get('category') == 'Property':
                income_data['rental_income']['expenses'] += expense.get('amount', 0)
        
        # Consolidate tax deductions
        tax_deductions = extracted_data.get('tax_deductions', {})
        income_data['pension_contributions'] += tax_deductions.get('pension_contributions', 0)
    
    return income_data

def process_tax_calculation(income_data: Dict):
    """Process tax calculations and generate reports"""
    print("\n🧮 Step 2: Tax Calculations")
    
    try:
        # Calculate comprehensive tax liability
        tax_result = calculate_comprehensive_tax_liability(income_data)
        print("✅ Tax calculations complete")
        
        # Display summary
        total_tax = tax_result.get('net_total_tax', 0)
        effective_rate = tax_result.get('effective_tax_rate', 0)
        
        print(f"\n📊 Tax Summary:")
        print(f"💰 Total Tax Liability: £{total_tax:,.2f}")
        print(f"📈 Effective Tax Rate: {effective_rate:.1%}")
        
    except Exception as e:
        print(f"❌ Tax calculation failed: {e}")
        return
    
    # Step 3: Validation and Reporting
    print("\n✅ Step 3: Validation and Reporting")
    
    try:
        api_key = os.getenv('CLAUDE_API_KEY')
        validation_report = run_complete_validation_and_reporting(tax_result, api_key)
        
        if validation_report['processing_summary']['validation_passed']:
            print("✅ All validations passed")
        else:
            print(f"⚠️  Found {validation_report['processing_summary']['errors_count']} errors")
            print(f"⚠️  Found {validation_report['processing_summary']['warnings_count']} warnings")
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        validation_report = None
    
    # Step 4: Optimization Analysis
    print("\n🎯 Step 4: Optimization Analysis")
    
    try:
        optimization_plan = generate_comprehensive_optimization_plan(tax_result)
        
        summary = optimization_plan.get('summary', {})
        potential_savings = summary.get('potential_savings', 0)
        immediate_actions = summary.get('immediate_actions', 0)
        
        print(f"💡 Found {summary.get('total_recommendations', 0)} optimization opportunities")
        print(f"💰 Potential Annual Savings: £{potential_savings:,.2f}")
        print(f"🚨 Immediate Actions Required: {immediate_actions}")
        
    except Exception as e:
        print(f"❌ Optimization analysis failed: {e}")
        optimization_plan = None
    
    # Step 5: Generate Reports
    print("\n📋 Step 5: Generate Reports")
    
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save JSON results
    json_file = f"{output_dir}/tax_analysis_{timestamp}.json"
    with open(json_file, 'w') as f:
        json.dump({
            'tax_calculation': tax_result,
            'validation_report': validation_report,
            'optimization_plan': optimization_plan
        }, f, indent=2, default=str)
    
    print(f"💾 Detailed results saved to: {json_file}")
    
    # Display next steps
    if optimization_plan:
        immediate_actions = optimization_plan.get('optimization_results', {}).get('immediate_actions', [])
        if immediate_actions:
            print(f"\n🎯 Priority Actions:")
            for i, action in enumerate(immediate_actions[:3], 1):
                print(f"{i}. {action.get('title', 'Action')}")
                if action.get('deadline'):
                    print(f"   ⏰ Deadline: {action['deadline']}")
                if action.get('potential_saving'):
                    print(f"   💰 Potential Saving: £{action['potential_saving']:,.2f}")
    
    print(f"\n✅ Tax optimization analysis complete!")
    print(f"📁 Check the '{output_dir}' directory for detailed reports")

def cli_mode(args):
    """Command line interface mode"""
    if args.files:
        print(f"🔄 Processing {len(args.files)} files...")
        try:
            api_key = os.getenv('CLAUDE_API_KEY')
            results = batch_process_documents(args.files, api_key)
            income_data = consolidate_extracted_data(results)
            process_tax_calculation(income_data)
        except Exception as e:
            print(f"❌ CLI processing failed: {e}")
    else:
        print("❌ No files specified for CLI mode")

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description='Tax Optimization AI')
    parser.add_argument('--files', nargs='+', help='Document files to process')
    parser.add_argument('--cli', action='store_true', help='Run in CLI mode')
    
    args = parser.parse_args()
    
    # Load environment
    load_environment()
    
    print("🎯 Tax Optimization AI v1.0")
    print("Created by: Sotiris Spyrou, CEO, VerityAI")
    print("=" * 50)
    
    if args.cli:
        cli_mode(args)
    else:
        interactive_mode()

if __name__ == "__main__":
    main()
