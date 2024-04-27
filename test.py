import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS 
from langchain_community.vectorstores.utils import DistanceStrategy
import streamlit

# Load Tokens
def load_configurations():
    load_dotenv()
    access_token = os.getenv("TOKEN")
    model_id = "google/gemma-2b-it"
    return access_token, model_id

model, token = load_configurations()

print(token)