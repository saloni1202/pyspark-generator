import os
import json
import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set your Groq API key
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# LangChain prompt template
template = """
You are a senior PySpark developer.

Given the following JSON data:
{json_data}

And the following business logic:
"{logic}"

Generate only the PySpark code that implements the logic. Do not include any explanation, comments, or extra text. Return only the code.
"""
prompt = ChatPromptTemplate.from_template(template)

# Initialize LLM
llm = ChatGroq(
    model_name="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0.2,
)
parser = StrOutputParser()
chain = prompt | llm | parser

# Streamlit UI
st.set_page_config(page_title="PySpark Code Generator", layout="centered")
st.title("🧠 PySpark Code Generator from JSON + Business Logic")

uploaded_file = st.file_uploader("Upload JSON file", type=["json"])
business_logic = st.text_area("Enter Business Logic", height=100)

if uploaded_file and business_logic:
    try:
        json_data = json.load(uploaded_file)
        st.subheader("📦 Uploaded JSON")
        st.json(json_data)

        with st.spinner("Generating PySpark code..."):
            response = chain.invoke({
                "json_data": json.dumps(json_data, indent=2),
                "logic": business_logic
            })

        st.subheader("🧾 Generated PySpark Code")
        st.code(response, language="python")

    except Exception as e:
        st.error(f"Error: {e}")
