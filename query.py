from lang_data import docsearch,hf
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import os
query = "Which school do you attend?"
from dotenv import load_dotenv
load_dotenv()
groq_api_key=os.environ['GORQ_API_KEY']


chat = ChatGroq(
    groq_api_key=groq_api_key,
    model="Llama3-8b-8192"
    # temperature=0,
    # model="llama3-8b-8192",
    # api_key=groq_api_key
)
# print(chat)

template = """
you need to answer Question based on Context.

<Context>: {context}
<Question>: {question}
<Answer>: 

"""
prompt = PromptTemplate(
  template=template, 
  input_variables=["context", "question"]
)

from langchain_core.runnables import  RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

rag_chain = (
  {"context": docsearch.as_retriever(),  "question": RunnablePassthrough()} 
  | prompt 
  | chat
  | StrOutputParser() 
)

result = rag_chain.invoke(query)
print(result)
# document_chain=create_stuff_documents_chain(chat,template)
# retriever=docsearch.as_retriever()
# retrival_chain=create_retrieval_chain(retriever,document_chain)
# response=retrival_chain.invoke({'input':query})
# print(response['answer'])


# docs = docsearch.similarity_search(query)
# print(docs[0].page_content)