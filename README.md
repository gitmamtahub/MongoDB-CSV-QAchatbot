# MongoDB + LLM Query System

This project:
- Loads CSV data into MongoDB.
- Uses a local LLM (Salesforce/codegen-350M-multi) to generate MongoDB queries.
- Executes queries based on user input.
- Displays and saves results.

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Structure
1. Uploaded CSV file will be stored in ./data/input-x.csv (for reference)
2. Generated query will be stored in ./output/queries_generated.txt
3. Result of query run is saved in ./output/output-x.csv

## Models used
1. MongoDB local
2. local run transformers LLM "Salesforce/codegen-350M-multi"

## dir structure
--MongoDB-CSV-QA(root)
    -.gitignore
    -.README.md
    -utils.py
    -app.py
    -requirement.txt
    -/data/input-x.vsc
    -/output
        -output-x.csv
        -queries_generated.txt