from lang_data import hf
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import os
from langchain_pinecone import PineconeVectorStore

from langchain_core.runnables import  RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
load_dotenv()
groq_api_key=os.environ['GORQ_API_KEY']


chat = ChatGroq(
    groq_api_key=groq_api_key,
    model="Llama3-8b-8192"
)



def get_user_rag_chain(docsearch):
    template = """
    You need to answer the Question based on Context and you are an Apple sales bot. Your job is to present the answer in such a way that the user gets impressed by the product.
    <Context>: {context}
    <Question>: {question}
    <Answer>:
    """
    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )
    
    rag_chain = (
        {"context": docsearch.as_retriever(), "question": RunnablePassthrough()}
        | prompt
        | chat
        | StrOutputParser()
    )
    
    return rag_chain