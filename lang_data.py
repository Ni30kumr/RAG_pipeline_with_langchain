from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader,PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
import os


from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()


model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
hf = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)
pinecone_api_key =os.getenv("PINECONE_API_KEY")

import time

# index_name = "applevision"  # change if desired
pc = Pinecone(api_key=pinecone_api_key)



def create_user_index(username, pdf_path):
    index_name = f"user-{username}-index"
    print(index_name)
    if index_name not in [index_info["name"] for index_info in pc.list_indexes()]:
        pc.create_index(
            name=index_name,
            dimension=768,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    
    index = pc.Index(index_name)
    docsearch = PineconeVectorStore.from_documents(pages, hf, index_name=index_name)
    
    return docsearch