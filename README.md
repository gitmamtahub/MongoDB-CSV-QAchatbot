# MongoDB + LLM Query System

This project:
- Loads CSV data into MongoDB.
- Uses a local LLM (Salesforce/codegen-350M-multi) to generate MongoDB queries.
- Executes queries based on user input.
- Displays and saves results.

## Setup Instructions

1. Install dependencies:
   ```bash
   python -m venv venv
   venv/Scripts/Activate
   pip install -r requirements.txt
   streamlit run app.py

## Structure
1. Uploaded CSV file will be stored in ./data/input-x.csv (for reference)
2. Generated query will be stored in ./output/queries_generated.txt
3. Result of query run is saved in ./output/output-x.csv

## Models used
1. MongoDB localhost:27017
2. local run transformers LLM "Salesforce/codegen-350M-multi"
3. python version 3.10

## dir structure
### --MongoDB-CSV-QA(root)
    -.gitignore
    -.README.md
    -utils.py
    -app.py
    -requirement.txt
#### -/data
         -input-x.vsc
#### -/output
         -output-x.csv
         -queries_generated.txt

## Test Case Output
### test-results folder
#### Sample_data.csv is used and three different queries run with just natural language
#### example1 - what are the products with rating greater than 4.5 ?
#### example2 - what are the products with reviewcount less than 200?
#### example3 - what are the products with price greater than $50 ?
