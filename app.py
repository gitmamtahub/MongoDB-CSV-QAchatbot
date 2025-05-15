import streamlit as st
import pandas as pd
from utils import get_run_counter , load_csv_to_mongodb, save_csv
from utils import generate_query_from_question, query_and_output, extract_filter_dict
import warnings
warnings.filterwarnings("ignore")

run_count  = get_run_counter()

# UI Title
st.title("🔍 MongoDB Natural Language Query Generator")

# File Upload
uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("CSV file loaded successfully!")

    # Show a preview
    st.subheader("📊 Data Preview")
    st.dataframe(df.head())
    
    # save input file
    input_file = f"input_{run_count}"
    in_msg = save_csv(df, "data", input_file)
    st.success(in_msg)
    
    # load csv to mongodb
    msg, collection = load_csv_to_mongodb(df, run_count)
    st.success(msg)

    # User Inputs
    selected_column = st.selectbox("📌 Select a column for querying:", df.columns)
    question = st.text_input("❓ Enter your natural language question:")
    
    if st.button("Run Query"):
        decoded = generate_query_from_question(selected_column,question)
        st.text_area("🧠 Generated MongoDB Query", decoded, height=100)
        cond, query = extract_filter_dict(decoded)
        
        if cond==0 :
            flag, results = query_and_output(query, collection)

            if flag == 0:
                result_df = pd.DataFrame(results)
                st.subheader("✅ Query Results")
                st.dataframe(result_df)

                # Save to CSV
                output_file = f"output_{run_count}"
                out_msg = save_csv(result_df, "output",output_file)
                st.success(out_msg)
            else :
                st.error(f"Error evaluating query: {results}")
                
        else :
            st.warning(query)