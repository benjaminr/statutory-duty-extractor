# Statutory Duty Extractor 📜🤖

**Note: This repository contains proprietary materials for authorised use only. Do not share further. See [LICENSE](./LICENSE) for important usage restrictions.**

## The Mission 🎯

The Prime Minister's Office has issued an urgent request: Local Authorities across the UK are drowning in statutory instruments, struggling to identify their legal obligations buried within thousands of pages of legislation. Your mission is to build an AI-powered solution that can automatically extract and index statutory duties from these documents, helping councils understand exactly what they're legally required to do.

This prototype tool uses cutting-edge LLMs to transform impenetrable legal PDFs into clear, structured data about who must do what under UK law.

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
├── prompts/                        # Extraction prompts
│   ├── system_prompt.txt
│   └── user_prompt.txt
└── tests/                         # Unit tests
```

### Data Directory Structure

- **`statutory_instruments_pdf/`**: The original UK statutory instrument PDFs that need processing
- **`ground_truth_json/`**: Simplified ground truth examples in JSON format that match our minimal data model (3 fields per duty)

## Current Implementation

The current approach:
1. Extracts text from PDFs using PyMuPDF
2. Sends the full text to Azure OpenAI with a prompt
3. Uses structured outputs to get back `StatutoryInstrument` objects
4. Displays results in a formatted table

## Development

```bash
# Run tests
uv run pytest

# Format code
uv run ruff format .

# Type check
uv run mypy src/
```
