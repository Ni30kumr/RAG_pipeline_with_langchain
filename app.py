import streamlit as st
from lang_data import docsearch
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
groq_api_key = os.environ['GORQ_API_KEY']

# Initialize ChatGroq
chat = ChatGroq(
    groq_api_key=groq_api_key,
    model="Llama3-8b-8192"
)

# Define the prompt template
template = """
You need to answer the Question based on the Context. You are an Apple sales bot.

<Context>: {context}
<Question>: {question}
<Answer>: 
"""
prompt = PromptTemplate(
    template=template, 
    input_variables=["context", "question"]
)

# Set up the RAG chain
rag_chain = (
    {"context": docsearch.as_retriever(), "question": RunnablePassthrough()} 
    | prompt 
    | chat
    | StrOutputParser() 
)

# Streamlit app
st.title("Apple Product Q&A")

# User input
user_question = st.text_input("Ask a question about Apple products:")

if user_question:
    with st.spinner("Generating answer..."):
        # Generate answer
        result = rag_chain.invoke(user_question)
        
        # Display answer
        st.subheader("Answer:")
        st.write(result)
