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

system = "you are an email replying assistant. you are supposed to reply to the email on behalf of the user. identify if an email has fields that are to be filled by the users. return only the the fields to be filled by user in form of a python list. reply should start with thanking the sender for his email and expressing your interest in the job opening described in the email. do not add square brackets other than for python list"
human = "{text}"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

model = ChatGroq(temperature=0, groq_api_key=gro_key, model_name="llama-3.1-70b-versatile")

output_parser=StrOutputParser()

chain = prompt | model | output_parser

input_text = st.text_input('Paste your email here')

st.write(chain.invoke({"text": input_text}))

