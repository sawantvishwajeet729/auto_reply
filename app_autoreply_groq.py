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

gro_key = st.secrets("groq_key")

st.set_page_config(page_title="Chatbot", page_icon=":desktop_computer:", layout="wide")

system = "You are a helpful assistant."
human = "{text}"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

model = ChatGroq(temperature=0, groq_api_key=gro_key, model_name="llama-3.1-70b-versatile")
chain = prompt | model
chain.invoke({"text": "Explain the importance of low latency LLMs."})


st.write(chain.invoke({"text": "Explain the importance of low latency LLMs."}))

