from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL

def create_vector_store(documents, path):
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    db = FAISS.from_documents(documents, embeddings)
    db.save_local(path)
    return db

def load_vector_store(path):
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
