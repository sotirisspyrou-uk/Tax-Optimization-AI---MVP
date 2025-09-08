# Tax Optimization AI - MVP

**Date:** 08-09-2025  
**Version:** 1.0  
**Authored by:** Sotiris Spyrou, CEO, VerityAI  
**File Path:** //documents/README_08092025.md

## Overview

Tax Optimization AI is a comprehensive UK tax calculation and optimization system designed to help taxpayers with multiple income streams achieve HMRC compliance while minimizing their tax liability. The system processes tax documents, performs accurate calculations, and provides actionable optimization recommendations.

## 🎯 Key Features

- **Comprehensive UK Tax Calculations**: Income Tax, National Insurance, Capital Gains Tax, rental income, and dividend tax
- **Intelligent Document Processing**: Automatic extraction from P60s, P45s, bank statements, rental records, and investment statements
- **Advanced Optimization Engine**: AI-powered recommendations for tax efficiency strategies
- **HMRC Compliance Validation**: Built-in compliance checking against current UK tax regulations
- **Professional Reports**: Multi-format outputs (HTML, PDF, Excel, JSON) suitable for professional review
- **Real-time Analysis**: Processing of complex tax scenarios with confidence scoring

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Claude API key from Anthropic
- 4GB RAM minimum
- Internet connection for API calls

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/overunityai/tax-optimization-ai.git
   cd tax-optimization-ai
   ```

2. **Run Setup Script**
   ```bash
   chmod +x setup_project.sh
   ./setup_project.sh
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env file with your API keys
   CLAUDE_API_KEY=your_claude_api_key_here
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### First Run

```bash
python main.py
```

Follow the interactive prompts to:
1. Upload your tax documents
2. Review extracted data
3. Generate tax calculations
4. Receive optimization recommendations

## 📁 Project Structure

```
tax-optimization-ai/
├── main.py                          # Main application entry point
├── functions/
│   ├── uk_tax_calculations.py       # Core tax calculation engine
│   ├── document_processing_tools.py # Document OCR and extraction
│   ├── validation_reporting_functions.py # Data validation and reports
│   └── optimization_engine_functions.py  # Optimization recommendations
├── documents/
│   ├── README_08092025.md
│   ├── Workflow_Flowchart_08092025.md
│   ├── Claude_08092025.md
│   └── User_Instructions_08092025.md
├── prompts/
│   ├── master_system_prompt.py
│   ├── tax_rules_engine_prompt.py
│   ├── document_processing_prompt.py
│   └── optimization_recommendation_prompt.py
├── tests/
│   └── test_suite.py
├── requirements.txt
├── .env.example
└── setup_project.sh
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required
CLAUDE_API_KEY=your_claude_api_key_here

# Optional
LOG_LEVEL=INFO
CONFIDENCE_THRESHOLD=0.8
HMRC_API_KEY=your_hmrc_api_key_here  # Future enhancement
```

### System Settings

Key configuration options in `main.py`:

```python
# Document processing settings
CONFIDENCE_THRESHOLD = 0.8
MAX_FILE_SIZE = 10  # MB
SUPPORTED_FORMATS = ['pdf', 'jpg', 'png', 'xlsx', 'csv']

# Tax calculation settings
TAX_YEAR = "2024/25"
DEFAULT_PERSONAL_ALLOWANCE = 12570
```

## 💻 Usage Examples

### Basic Tax Calculation

```python
from functions.uk_tax_calculations import calculate_comprehensive_tax_liability

# Prepare income data
income_data = {
    'employment_income': 75000,
    'rental_income': {
        'gross_income': 15000,
        'expenses': 3000,
        'mortgage_interest': 8000
    },
    'pension_contributions': 5000,
    'gift_aid_donations': 500
}

# Calculate tax liability
result = calculate_comprehensive_tax_liability(income_data)
print(f"Total tax liability: £{result['net_total_tax']:,.2f}")
```

### Document Processing

```python
from functions.document_processing_tools import DocumentProcessor

processor = DocumentProcessor(anthropic_api_key="your_key")
result = processor.process_document("path/to/p60.pdf")

print(f"Confidence: {result['metadata']['confidence_score']:.2%}")
print(f"Income extracted: £{result['extracted_data']['income_streams'][0]['amount']:,.2f}")
```

### Generate Optimization Report

```python
from functions.optimization_engine_functions import generate_comprehensive_optimization_plan

# Generate recommendations
optimization_plan = generate_comprehensive_optimization_plan(tax_result)

print(f"Potential savings: £{optimization_plan['summary']['potential_savings']:,.2f}")
print(f"Immediate actions: {optimization_plan['summary']['immediate_actions']}")
```

## 🎯 Tax Year 2024/25 Thresholds

The system includes current UK tax thresholds:

| Component | Threshold/Rate |
|-----------|----------------|
| Personal Allowance | £12,570 |
| Basic Rate (20%) | £12,571 - £50,270 |
| Higher Rate (40%) | £50,271 - £125,140 |
| Additional Rate (45%) | Above £125,140 |
| CGT Allowance | £6,000 |
| Dividend Allowance | £1,000 |
| ISA Allowance | £20,000 |
| Pension Annual Allowance | £60,000 |

## 🔍 Supported Document Types

- **P60**: Annual tax statements from employers
- **P45**: Leaving certificates from previous employers
- **Bank Statements**: For income and expense tracking
- **Rental Records**: Property income and expense documentation
- **Investment Statements**: Dividend and capital gains records
- **Pension Statements**: Contribution and benefit summaries
- **Mortgage Statements**: For rental property interest calculations

## ⚡ Performance

### Benchmarks
- Document processing: <30 seconds per file
- Tax calculations: <5 seconds for complete analysis
- Report generation: <10 seconds all formats
- Memory usage: <500MB typical operation

### Scalability
- Handles portfolios up to 50 properties
- Processes investment accounts with 1000+ transactions
- Supports multiple tax years (future enhancement)

## 🛡️ Security & Privacy

### Data Protection
- No persistent storage of sensitive data
- Local processing with API calls only for analysis
- Automatic data cleanup after session
- Encryption in transit for all API communications

### Compliance
- GDPR compliant data handling
- HMRC calculation methodology adherence
- Professional accounting standards alignment
- Audit trail maintenance for all calculations

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

Test categories:
- **Unit Tests**: Individual function validation
- **Integration Tests**: End-to-end workflow testing
- **Calculation Tests**: Tax calculation accuracy verification
- **Document Tests**: OCR and extraction validation

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch (`git checkout -b feature/enhancement`)
3. Commit changes (`git commit -am 'Add enhancement'`)
4. Push to branch (`git push origin feature/enhancement`)
5. Create Pull Request

### Code Standards
- PEP 8 compliance for Python code
- Comprehensive docstrings for all functions
- Type hints for function parameters and returns
- Error handling for all external dependencies

## 📞 Support

### Getting Help
- Check the [User Instructions](documents/User_Instructions_08092025.md) for common questions
- Review the [Claude.md](documents/Claude_08092025.md) for technical details
- Open an issue for bugs or feature requests

### Professional Services
For complex tax situations requiring professional advice:
- Engage qualified tax advisors for strategy implementation
- Use generated reports as supporting documentation
- Consider annual reviews for ongoing optimization

## 🔮 Roadmap

### v1.1 (Q4 2025)
- Real-time HMRC API integration
- Multi-year tax planning optimization
- Advanced investment structure analysis
- Mobile app interface

### v1.2 (Q1 2026)
- Machine learning enhanced document processing
- International tax considerations
- Automated form completion and submission
- Advanced scenario modeling

### v2.0 (Q2 2026)
- Full estate planning integration
- Business tax optimization
- Real-time legislative update integration
- Professional advisor collaboration tools

## 📄 License

MIT License - see LICENSE file for details.

## ⚠️ Disclaimer

This software provides tax calculations and optimization suggestions based on current UK tax law. It is not a substitute for professional tax advice. Users should consult qualified tax professionals for complex situations and verify all calculations independently. The software is provided "as is" without warranty of any kind.

## 📊 Version History

- **v1.0** (08-09-2025): Initial MVP release with core functionality
- **v0.9** (01-09-2025): Beta testing and validation
- **v0.8** (25-08-2025): Alpha release for internal testing

---
