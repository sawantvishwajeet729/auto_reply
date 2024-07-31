#Libraries to be imported
import time
import os
import requests
import random
import re
import streamlit as st

#---Langchain Libraries---
from langchain_core.prompts import ChatPromptTemplate
from groq import Groq
from langchain_core.output_parsers import StrOutputParser
import ast

#Output parser
class FieldsToFillParser(StrOutputParser):
    def parse(self, text: str):
        # Extract the Python code block content
        code_block = text.strip().strip('```').strip()
        
        # Use ast.literal_eval to safely evaluate the list
        try:
            # Compile and evaluate the code block to extract the list
            fields_to_fill = ast.literal_eval(code_block.split('=')[1].strip())
            return fields_to_fill
        except (ValueError, SyntaxError) as e:
            raise ValueError("Failed to parse fields_to_fill list.") from e

# Regular expression pattern to match content within square brackets
pattern = r"\[(.*?)\]"

# Example usage
parser = FieldsToFillParser()

#---Env variables---
os.environ['LANGCHAIN_TRACING_V2'] = 'False'
groq_api_Key = st.secrets["groq_key"]

#create streamlit webpage
st.set_page_config(page_title="Chatbot", page_icon=":desktop_computer:", layout="wide")

#ChatGPT model
model=Groq(model="llama-3.1-70b-versatile", groq_api_key = groq_api_Key,
           temperature=1,
           max_tokens=1024,
           top_p=1,
           stream=True,
           stop=None)

output_parser=StrOutputParser()

#create prompt template
prompt = ChatPromptTemplate.from_template("""
                                          "you are an email replying assistant. you are supposed to reply to the email on behalf of the user. identify if an email has fields that are to be filled by the users. return only the the fields to be filled by user in form of a python list. reply should start with thanking the sender for his email and expressing your interest in the job opening described in the email. do not add square brackets other than for python list " 
                                          Question: {input}""")


chain = prompt| model | output_parser


with st.container():
    st.subheader('Paste your email below')
    txt_input = st.text_area('-', height=250)

    response = chain.invoke({'input': txt_input})

    # Find all matches using re.findall
    matches = re.findall(pattern, response)

    # Process matches if needed
    if matches:
        # Convert the string representation of the list into an actual list
        req_list = eval(matches[0])
    else:
        req_list = ['Name', 'Current Company', 'Position']


with st.container():
    text_1, text_2 = st.columns((1, 2))

    with text_1:
        with st.form(key='my_form', clear_on_submit=True):
            d = {}
            for i in req_list:
                d["{0}".format(i)] = st.text_input(i)

            submit_button = st.form_submit_button(label='Submit')

    with text_2:
        if submit_button:
            st.subheader('You entered the following details are:')

            for i in d:
                st.write(i, ' : ' ,d[i])
