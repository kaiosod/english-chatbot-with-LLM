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

# Load GemmaLLM
@streamlit.cache_resource
def initialize_model(model_id, access_token):
    tokenizer = AutoTokenizer.from_pretrained(model_id,token=access_token)
    quantization_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16)
    model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", quantization_config=quantization_config)
    model.eval()
    return model, tokenizer

# Generate a response
def generate(question,context,tokenizer,model):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    prompt = f"Using the information contained in the context, give a detailed answer to the question. \n context:"

    chat = [{"role":"user", "content":prompt}]
    formatted_prompt = tokenizer.apply_chat_template(chat,tokenize = False, add_generation_prompt=True)
    inputs = tokenizer.encode(formatted_prompt, add_special_tokens=False, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model.generate(input_ids=inputs, max_new_tokens=512, do_sample=False)
    response = tokenizer.decode(outputs[0], skip_special_tokens=False)
    response = response[len(formatted_prompt):].replace("<eos>","")
    return response

# Load PDF -> character.pdf
@streamlit.cache_resource
def process_documents(tokenizer_model):
    loaders = [PyPDFLoader("character.pdf")]
    pages = []
    for loader in loaders:
        pages.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        tokenizer=AutoTokenizer.from_pretrained(tokenizer_model),
        chunk_size=256, chunk_overlap=int(256/10), strip_whitespace=True
    )
    docs = text_splitter.split_documents(pages)
    return docs

# Database FAISS
def create_faiss_db(docs, encoder):
    faiss_db = FAISS.from_documents(docs, encoder, distance_strategy = DistanceStrategy.COSINE)
    return faiss_db

# Streamlit
def streamlit_chat_interface(faiss_db, tokenizer, model):
    streamlit.title("Chatbot")

    # Starting message history 
    if "messages" not in streamlit.session_state:
        streamlit.session_state.messages = []
    for message in streamlit.session_state.messages:
        with streamlit.chat_message(message["role"]):
            streamlit.markdown(message["content"])
        
        # Show user question
        if prompt := streamlit.chat_input("Ask me anything!"):
            streamlit.session_state.messages.append({"role":"user", "content":prompt})
            with streamlit.chat_message("user"):
                streamlit.markdown(prompt)

            # Show the chatbot response
            with streamlit.chat_message("assistant"):
                retrieved_docs = faiss_db.similarity_search(prompt,k=3)
                context = "".join(doc.page_content + "\n" for doc in retrieved_docs)
                answer = generate(prompt, context, tokenizer, model)
                streamlit.write(answer)
            streamlit.session_state.messages.append({"role":"assistant", "content": answer})

if __name__ == "__main__": 
    access_token , model_id = load_configurations()
    model, tokenizer = initialize_model(model_id, access_token)
    docs = process_documents('sentence-transformers/all-MiniLM-L12-v2')
    encoder = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L12-v2', model_kwargs= {'device':"cuda"})
    faiss_db = create_faiss_db(docs, encoder)
    streamlit_chat_interface(faiss_db,tokenizer,model)
