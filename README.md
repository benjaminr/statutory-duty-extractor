# Statutory Duty Extractor

A prototype tool for extracting statutory duties from UK statutory instruments using LLMs. This project aims to automatically identify and structure legal obligations from PDF documents.

## Overview

This tool processes UK statutory instruments (in PDF format) and extracts:
- **Duty descriptions**: The specific legal obligations
- **Duty holders**: Who must fulfil each duty (e.g., "local authority", "Secretary of State")
- **Legislative references**: Where the duty appears (e.g., "regulation 3")

## Quick Start

1. **Set up environment**
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd statutory-duty-extractor

   # Install dependencies using UV
   uv sync

   # Copy and configure environment variables
   cp .env.example .env
   # Edit .env with your Azure OpenAI credentials
   ```

2. **Run extraction**
   ```bash
   # Extract from a single PDF
   uv run statutory-duty-extractor data/statutory_instruments_pdf/2089.pdf
   ```

## Project Structure

```
statutory-duty-extractor/
├── src/statutory_duty_extractor/
│   ├── models.py          # Pydantic models for duties
│   ├── extractor.py       # Core extraction logic
│   └── cli.py            # Command-line interface
├── data/
│   ├── statutory_instruments_pdf/  # Original PDF documents to process
│   ├── ground_truth_json/          # Simplified examples (matches data model)
│   └── ground_truth_raw/           # Complete labelled dataset (Excel format)
├── prompts/                        # Extraction prompts
│   ├── system_prompt.txt
│   └── user_prompt.txt
└── tests/                         # Unit tests
```

### Data Directory Structure

- **`statutory_instruments_pdf/`**: The original UK statutory instrument PDFs that need processing
- **`ground_truth_json/`**: Simplified ground truth examples in JSON format that match our minimal data model (3 fields per duty)
- **`ground_truth_raw/`**: The complete labelled dataset in Excel format with 20+ fields per duty, providing the full context and detailed annotations

## Current Implementation

The current approach:
1. Extracts text from PDFs using PyMuPDF
2. Sends the full text to Azure OpenAI with a prompt
3. Uses structured outputs to get back `StatutoryInstrument` objects
4. Displays results in a formatted table

## Known Issues & Limitations

### 1. **Prompt Specificity**
The current prompts are quite generic and miss important nuances:
- Doesn't distinguish between primary duties and subordinate requirements
- May confuse procedural requirements with substantive duties
- No guidance on handling conditional duties ("if X then must Y")

### 2. **Extraction Coverage**
Comparing with ground truth data shows:
- We're only extracting a subset of labelled duties
- Some duties are split incorrectly (one duty becomes two)
- Complex multi-part duties are often missed

### 3. **Data Model Simplicity**
We've opted for a minimal model with just three fields:
```python
class StatutoryDuty:
    duty_description: str
    duty_holder: str
    legislative_reference: str
```

The full ground truth includes additional context fields that might help with more accurate extraction.

### 4. **Text Matching Challenges**
The ground truth descriptions are paraphrased summaries, not direct quotes:
- Ground truth: "Hold meetings of decision-making bodies in public"
- Actual text: "A meeting of a decision-making body must be held in public"

This makes direct evaluation difficult.

### 5. **Document Processing**
Currently processing entire PDFs at once:
- No chunking strategy for long documents
- May exceed token limits on complex instruments
- Loses structural information (headings, sections)

### 6. **Ground Truth Subset**
The provided ground truth JSON files are a simplified subset:
- Originally contained 20+ fields per duty
- Converted to minimal 3-field model
- Some duties excluded if they didn't map cleanly

## Development

```bash
# Run tests
uv run pytest

# Format code
uv run ruff format .

# Type check
uv run mypy src/
```

## Notes

This is a prototype implementation focusing on demonstrating the basic extraction capability. The simplified approach makes it easier to understand the core challenges while leaving plenty of room for improvements in accuracy, coverage, and robustness.
