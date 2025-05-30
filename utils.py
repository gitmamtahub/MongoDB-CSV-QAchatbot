import os
import pandas as pd
from pymongo import MongoClient
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
import ast
import re
import warnings
warnings.filterwarnings("ignore")


# 1    Get Run_counter to save each and every output
def get_run_counter():
    """Reads and updates the run counter from a file inside 'output' folder."""
    os.makedirs("output", exist_ok=True)  # Ensure 'output' folder exists
    counter_file = "output/run_counter.txt"
    
    if os.path.exists(counter_file):
        with open(counter_file, "r") as f:
            run_count = int(f.read().strip())
    else:
        run_count = 1  # Start from 1 if no file exists
    
    # Increment and update the file
    with open(counter_file, "w") as f:
        f.write(str(run_count + 1))
    
    return run_count

def save_csv(df,d, f):
    """Reads and updates the run counter from a file inside 'output' folder."""
    os.makedirs(d, exist_ok=True)  # Ensure 'output' folder exists
    csv_file = f"{d}/{f}.csv"
    df.to_csv(csv_file, index = False)
    return f"CSV file stored as {csv_file}"

# 3  load_csv_to_mongodb.py
def load_csv_to_mongodb(df, run_count):
    db_name = 'DB' + str(run_count)
    collection_name = 'Collection' + str(run_count)
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client[db_name]
    collection = db[collection_name]

    # Load CSV
    data = df.to_dict(orient='records')

    # Insert into MongoDB
    collection.drop()  # Clear previous data
    collection.insert_many(data)
    
    return "Data inserted into MongoDB.", collection


# Load local LLM
model_name = "Salesforce/codegen-350M-mono"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_query_from_question(selected_column,question):
    # Generate Prompt
        prompt = f"""You are a MongoDB expert. Convert the following question into a valid MongoDB query in Python pymongo-style syntax.
                    Use only the field '{selected_column}' from the collection.
                    Question: {question}
                    Output: db.collection.find("""""

        # LLM Generate
        inputs = tokenizer(prompt, return_tensors="pt").to("cpu")
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=True,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id
        )
        decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
        

        # Save to queries_generated.txt
        with open("output/queries_generated.txt", "a") as log:
            log.write(f"\nColumn: {selected_column}\nQuestion: {question}\nGenerated Query: {decoded}\n")

        
        # Extract only the MongoDB query part
        query_start = decoded.find("db.collection.find")
        if query_start != -1:
            return decoded[query_start:].split("\n")[0]
        return "Error: Failed to generate valid MongoDB query."
    
def extract_filter_dict(query_str):
    match = re.search(r'db\.collection\.find\s*\((\{.*?\})\)', query_str)
    if not match:
        return 1, "Could not extract a valid filter dictionary from the generated query."

    try:
        return 0, ast.literal_eval(match.group(1))  # safely convert string to dict
    except Exception as e:
        return 1, f"Failed to parse filter dict: {e}"

    
def query_and_output(query, collection):
    if query == "Error: Failed to generate valid MongoDB query." :
        return 1, "⚠️ Query could not be parsed. Check the LLM output."

    results = list(collection.find(query))
    if not results:
        return 1, "⚠️ No records found."

    return 0, results