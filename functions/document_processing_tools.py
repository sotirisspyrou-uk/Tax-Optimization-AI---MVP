# //functions/document_processing_tools.py
# [Version 08-09-2025 14:35:00]
# Document Processing Tools for TaxOptim AI (MVP Version)
# Authored by: Sotiris Spyrou, CEO, VerityAI

import re
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class DocumentMetadata:
    """Metadata for processed documents"""
    document_type: str
    confidence_score: float
    processing_date: str
    document_quality: str
    extraction_method: str

@dataclass
class ExtractedData:
    """Structured extracted data from documents"""
    income_streams: List[Dict]
    expenses: List[Dict]
    tax_deductions: Dict
    personal_details: Dict
    validation_flags: List[Dict]

class DocumentProcessor:
    """Main document processing engine for tax documents"""
    
    def __init__(self, anthropic_api_key: str = None):
        self.anthropic_api_key = anthropic_api_key
        self.document_patterns = self._load_document_patterns()
    
    def process_document(self, file_path: str, document_type: str = None) -> Dict:
        """
        Main entry point for document processing
        """
        
        # Extract text from document
        extracted_text = self._extract_text(file_path)
        
        # Determine document type if not provided
        if not document_type:
            document_type = self._identify_document_type(extracted_text)
        
        # Process based on document type
        if document_type == "P60":
            extracted_data = self._process_p60(extracted_text)
        elif document_type == "bank_statement":
            extracted_data = self._process_bank_statement(extracted_text)
        else:
            # Basic text processing fallback
            extracted_data = self._basic_text_processing(extracted_text)
        
        # Calculate confidence and quality metrics
        metadata = self._calculate_metadata(extracted_text, extracted_data, document_type)
        
        return {
            "metadata": metadata.__dict__,
            "extracted_data": extracted_data.__dict__,
            "raw_text": extracted_text[:1000],  # First 1000 chars for reference
            "processing_notes": self._generate_processing_notes(extracted_data)
        }
    
    def _extract_text(self, file_path: str) -> str:
        """Extract text from various file formats"""
        
        file_extension = file_path.lower().split('.')[-1]
        
        try:
            if file_extension == 'txt':
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()
            elif file_extension == 'csv':
                # Basic CSV reading
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()
            else:
                # For MVP, require pre-converted text files
                return f"File format {file_extension} requires manual conversion to text. Please convert to .txt or .csv format."
                
        except Exception as e:
            return f"Error extracting text: {str(e)}"
    
    def _identify_document_type(self, text: str) -> str:
        """Identify document type from extracted text"""
        
        text_lower = text.lower()
        
        # P60 indicators
        if any(indicator in text_lower for indicator in ['p60', 'end of year certificate', 'annual statement']):
            return "P60"
        
        # Bank statement indicators
        if any(indicator in text_lower for indicator in ['bank statement', 'account summary', 'current account']):
            return "bank_statement"
        
        # Default to general document
        return "general"
    
    def _process_p60(self, text: str) -> ExtractedData:
        """Process P60 annual tax statement"""
        
        # Extract key figures using regex patterns
        patterns = {
            'total_pay': r'total pay.*?£?([0-9,]+\.?[0-9]*)',
            'income_tax': r'income tax.*?£?([0-9,]+\.?[0-9]*)',
            'national_insurance': r'national insurance.*?£?([0-9,]+\.?[0-9]*)',
            'pension_contributions': r'pension.*?£?([0-9,]+\.?[0-9]*)',
            'tax_code': r'tax code.*?([0-9]+[A-Z]?)',
            'employer_name': r'employer.*?([A-Za-z\s]+)',
            'nino': r'([A-Z]{2}[0-9]{6}[A-Z])'
        }
        
        extracted_values = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = match.group(1).replace(',', '')
                try:
                    extracted_values[key] = float(value) if key not in ['tax_code', 'employer_name', 'nino'] else value
                except ValueError:
                    extracted_values[key] = value
        
        # Structure the extracted data
        income_streams = [{
            "type": "Employment",
            "source": extracted_values.get('employer_name', 'Unknown Employer'),
            "amount": extracted_values.get('total_pay', 0),
            "tax_deducted": extracted_values.get('income_tax', 0),
            "period": "2024/25",
            "confidence": 0.85
        }]
        
        tax_deductions = {
            "income_tax": extracted_values.get('income_tax', 0),
            "national_insurance": extracted_values.get('national_insurance', 0),
            "pension_contributions": extracted_values.get('pension_contributions', 0)
        }
        
        personal_details = {
            "nino": extracted_values.get('nino', ''),
            "tax_code": extracted_values.get('tax_code', ''),
            "employer": extracted_values.get('employer_name', '')
        }
        
        validation_flags = []
        if not extracted_values.get('total_pay'):
            validation_flags.append({
                "issue": "Total pay not clearly identified",
                "severity": "High",
                "recommendation": "Manual verification required"
            })
        
        return ExtractedData(
            income_streams=income_streams,
            expenses=[],
            tax_deductions=tax_deductions,
            personal_details=personal_details,
            validation_flags=validation_flags
        )
    
    def _process_bank_statement(self, text: str) -> ExtractedData:
        """Process bank statement for tax-relevant transactions"""
        
        # Extract transaction patterns
        transaction_pattern = r'(\d{2}/\d{2}/\d{4})\s+([A-Za-z\s]+)\s+£?([0-9,]+\.?[0-9]*)'
        transactions = re.findall(transaction_pattern, text)
        
        income_streams = []
        expenses = []
        
        for date, description, amount in transactions:
            amount_float = float(amount.replace(',', ''))
            
            # Categorize transactions
            desc_lower = description.lower()
            
            # Income indicators
            if any(keyword in desc_lower for keyword in ['salary', 'dividend', 'interest', 'rental']):
                income_type = "Employment" if 'salary' in desc_lower else "Investment"
                income_streams.append({
                    "type": income_type,
                    "source": description.strip(),
                    "amount": amount_float,
                    "date": date,
                    "confidence": 0.70
                })
            
            # Expense indicators
            elif any(keyword in desc_lower for keyword in ['repair', 'insurance', 'professional', 'travel']):
                expenses.append({
                    "category": "Business" if 'professional' in desc_lower else "Property",
                    "amount": amount_float,
                    "date": date,
                    "description": description.strip(),
                    "allowable": True,
                    "confidence": 0.65
                })
        
        return ExtractedData(
            income_streams=income_streams,
            expenses=expenses,
            tax_deductions={},
            personal_details={},
            validation_flags=[]
        )
    
    def _basic_text_processing(self, text: str) -> ExtractedData:
        """Basic text processing for general documents"""
        
        # Look for currency amounts
        amounts = re.findall(r'£([0-9,]+\.?[0-9]*)', text)
        
        income_streams = []
        if amounts:
            # Assume first large amount is income
            try:
                first_amount = float(amounts[0].replace(',', ''))
                if first_amount > 1000:  # Reasonable income threshold
                    income_streams.append({
                        "type": "General",
                        "source": "Document extraction",
                        "amount": first_amount,
                        "confidence": 0.50
                    })
            except ValueError:
                pass
        
        return ExtractedData(
            income_streams=income_streams,
            expenses=[],
            tax_deductions={},
            personal_details={},
            validation_flags=[{
                "issue": "Basic text processing used",
                "severity": "Medium",
                "recommendation": "Manual review recommended for accuracy"
            }]
        )
    
    def _calculate_metadata(self, text: str, extracted_data: ExtractedData, document_type: str) -> DocumentMetadata:
        """Calculate document processing metadata and confidence scores"""
        
        # Basic quality assessment
        text_length = len(text)
        extraction_count = len(extracted_data.income_streams) + len(extracted_data.expenses)
        
        if text_length < 100:
            quality = "Low"
            confidence = 0.3
        elif extraction_count == 0:
            quality = "Medium"
            confidence = 0.5
        elif len(extracted_data.validation_flags) > 2:
            quality = "Medium"
            confidence = 0.7
        else:
            quality = "High"
            confidence = 0.8
        
        return DocumentMetadata(
            document_type=document_type,
            confidence_score=confidence,
            processing_date=datetime.now().isoformat(),
            document_quality=quality,
            extraction_method="Pattern Matching (MVP)"
        )
    
    def _generate_processing_notes(self, extracted_data: ExtractedData) -> List[str]:
        """Generate processing notes and recommendations"""
        
        notes = []
        
        if not extracted_data.income_streams:
            notes.append("No income streams identified - manual review recommended")
        
        if extracted_data.validation_flags:
            notes.append(f"Found {len(extracted_data.validation_flags)} validation issues")
        
        notes.append("MVP version - consider upgrading for enhanced OCR capabilities")
        
        return notes
    
    def _load_document_patterns(self) -> Dict:
        """Load regex patterns for document processing"""
        
        return {
            "currency": r'£?([0-9,]+\.?[0-9]*)',
            "date_uk": r'(\d{1,2}/\d{1,2}/\d{4})',
            "nino": r'([A-Z]{2}[0-9]{6}[A-Z])',
            "tax_code": r'([0-9]+[A-Z]?)',
            "percentage": r'([0-9]+\.?[0-9]*)%'
        }

# Utility functions for document processing workflow
def batch_process_documents(file_paths: List[str], anthropic_api_key: str = None) -> Dict:
    """Process multiple documents in batch"""
    
    processor = DocumentProcessor(anthropic_api_key)
    results = {}
    
    for file_path in file_paths:
        try:
            result = processor.process_document(file_path)
            results[file_path] = result
        except Exception as e:
            results[file_path] = {
                "error": str(e),
                "processed": False
            }
    
    return results
