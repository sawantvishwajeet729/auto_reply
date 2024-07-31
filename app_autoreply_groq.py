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


st.set_page_config(page_title="Chatbot", page_icon=":desktop_computer:", layout="wide")


model = ChatGroq(temperature=0, groq_api_key="YOUR_API_KEY", model_name="llama-3.1-70b-versatile")

input_txt = st.text_input('your text')

st.write(model.invoke(input_txt))