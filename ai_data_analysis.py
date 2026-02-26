import json
import tempfile
import csv
import streamlit as st
import pandas as pd
from phi.model.openai import OpenAIChat
from phi.agent.duckdb import DuckDbAgent
from phi.tools.pandas import PandasTools
import re
def preprocess_and_save(file):
    try:
        # Handle different file types
        if file.name.endswith('.csv'):
            df = pd.read_csv(file, encoding='utf-8')
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
            
        # Clean and format data
        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].astype(str).replace({r'"': '""'}, regex=True)
            
        # Handle dates and numbers
        for col in df.columns:
            if 'date' in col.lower():
                df[col] = pd.to_datetime(df[col], errors='coerce')

# Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_path = temp_file.name
            df.to_csv(temp_path, index=False, quoting=csv.QUOTE_ALL)
            
        return temp_path, df.columns.tolist(), df
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return None, None, None

st.title("📊 Data Analyst Agent")

with st.sidebar:
    st.header("API Keys")
    openai_key = st.text_input("Enter your OpenAI API key:", type="password")
    if openai_key:
        st.session_state.openai_key = openai_key

uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    temp_path, columns, df = preprocess_and_save(uploaded_file)
    
    st.write("Uploaded Data:")
    st.dataframe(df)
    st.write("Uploaded columns:", columns)
semantic_model = {
    "tables": [
        {
            "name": "uploaded_data",
            "description": "Contains the uploaded dataset.",
            "path": "temp_path",
        }
    ]
}
duckdb_agent = DuckDbAgent(
    model=OpenAIChat(model="gpt-4o-mini", api_key=st.session_state.get("openai_key","")),
    semantic_model=json.dumps(semantic_model),
    tools=[PandasTools()],
    markdown=True,
    system_prompt="You are an expert data analyst. Generate SQL queries..."
)
user_query = st.text_area("Ask a query about the data:")

if st.button("Submit Query"):
    if user_query.strip() == "":
        st.warning("Please enter a query.")
    else:
        with st.spinner('Processing your query...'):
            response1 = duckdb_agent.run(user_query)
            response = duckdb_agent.print_response(
                user_query,
                stream=True
            )