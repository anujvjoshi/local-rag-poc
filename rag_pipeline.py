from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from config import *

def split_docs(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    return splitter.split_documents(documents)

def build_qa_chain(vectorstore):

    template = """
You are a strict document assistant.

Answer ONLY from the given context.
If the answer is not in the context say:
"I cannot find this information in the document."

Do NOT use outside knowledge.

Context:
{context}

Question:
{question}

Answer:
"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

    llm = Ollama(model=LLM_MODEL)

    retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )

    return qa
