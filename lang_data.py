from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader,PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
import os


loader = PyPDFLoader("Apple_Vision_Pro_Privacy_Overview.pdf")
pages = loader.load_and_split()

# loader = TextLoader("dialogs.txt")
# documents = loader.load()
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
# docs = text_splitter.split_documents(documents)
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

index_name = "applevision"  # change if desired
pc = Pinecone(api_key=pinecone_api_key)

existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)

index = pc.Index(index_name)

docsearch = PineconeVectorStore.from_documents(pages, hf, index_name=index_name)