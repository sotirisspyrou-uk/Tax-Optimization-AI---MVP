# Tax Optimization AI - MVP

**Date:** 08-09-2025  
**Version:** 1.0  
**Authored by:** Sotiris Spyrou, CEO, VerityAI  

## Overview

Tax Optimization AI is a comprehensive UK tax calculation and optimization system designed to help taxpayers with multiple income streams achieve HMRC compliance while minimizing their tax liability.

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Claude API key from Anthropic

### Installation

1. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env file with your API keys
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
tax-optimization-ai/
├── main.py                          # Main application entry point
├── functions/                       # Core business logic
│   ├── uk_tax_calculations.py       # Tax calculation engine
│   ├── document_processing_tools.py # Document processing
│   ├── validation_reporting_functions.py # Validation and reports
│   └── optimization_engine_functions.py  # Optimization recommendations
├── tests/                          # Test suite
├── requirements.txt                # Python dependencies
└── .env.example                   # Environment configuration template
```

## 🎯 Key Features

- **UK Tax Calculations**: Income Tax, National Insurance, Capital Gains Tax
- **Document Processing**: Extract data from tax documents
- **Optimization Recommendations**: AI-powered tax efficiency strategies
- **HMRC Compliance**: Built-in compliance validation
- **Professional Reports**: Multiple output formats

## 💻 Usage

1. **Interactive Mode**: Run `python main.py` and follow prompts
2. **CLI Mode**: `python main.py --files document1.txt document2.csv`

## 🧪 Testing

```bash
python -m unittest tests/test_basic.py
```

## ⚠️ Disclaimer

This software provides tax calculations and optimization suggestions. It is not a substitute for professional tax advice. Consult qualified tax professionals for complex situations.

---

**Created by VerityAI** | **Contact:** support@verityai.co.uk
