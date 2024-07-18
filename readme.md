# Dynamic RAG-based Question Answering System

This project implements a dynamic Retrieval-Augmented Generation (RAG) system for question answering using LangChain, Pinecone, and Groq.

## Features

- Dynamic document loading and splitting
- Embedding generation using Hugging Face models
- Vector storage with Pinecone
- Question answering using Groq's language models

## Prerequisites

- Python 3.7+
- Pinecone API key
- Groq API key

## Installation

1. Clone the repository:
2. Install required packages: pip -r requirements.txt
3. Set up environment variables:
Create a `.env` file in the project root and add your API keys:
## Usage

1. Prepare your data:
Place your text data in a file named `dialogs.txt` in the project root.

2. Configure `lang_data.py`:
- Adjust `chunk_size` and `chunk_overlap` in `RecursiveCharacterTextSplitter` as needed.
- Modify the Hugging Face model name if desired.
- Change the Pinecone index name and settings if necessary.

3. Run the data processing and indexing:
4. Use the question answering system:
Edit `query.py` to set your question, then run:

## Customization

- To use a different document loader, modify the `loader` in `lang_data.py`.
- To change the embedding model, update the `model_name` in `lang_data.py`.
- To use a different Groq model, modify the `model` parameter in `ChatGroq` initialization in `query.py`.
- Adjust the prompt template in `query.py` to customize the system's behavior.

