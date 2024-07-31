#Libraries to be imported
import time
import os
import requests
import re
import streamlit as st

#---Langchain Libraries---
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from groq import Groq
from langchain_core.output_parsers import StrOutputParser
import ast

#set groq key
gro_key = st.secrets["groq_key"]

# Regular expression pattern to match content within square brackets
pattern = r"\[(.*?)\]"

st.set_page_config(page_title="Chatbot", page_icon=":desktop_computer:", layout="wide")

system_1 = "you are an email replying assistant. you are supposed to reply to the email on behalf of the user. identify if an email has fields that are to be filled by the users. return only the the fields to be filled by user in form of a python list. reply should start with thanking the sender for his email and expressing your interest in the job opening described in the email."
human_1 = "{text}"
prompt = ChatPromptTemplate.from_messages([("system", system_1), ("human", human_1)])

model = ChatGroq(temperature=0, groq_api_key=gro_key, model_name="llama-3.1-70b-versatile", max_tokens=1024)

output_parser=StrOutputParser()

chain = prompt | model | output_parser


with st.container():
    st.subheader('Paste your email below')
    txt_input = st.text_area('-', height=250)
    

    if st.button('Confirm'):
        response = chain.invoke({'text': txt_input})

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