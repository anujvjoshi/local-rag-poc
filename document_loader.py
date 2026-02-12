import pandas as pd
from langchain.schema import Document
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader

def load_document(file_path):
    ext = file_path.split(".")[-1].lower()

    if ext == "pdf":
        return PyPDFLoader(file_path).load()

    elif ext == "docx":
        return Docx2txtLoader(file_path).load()

    elif ext == "txt":
        return TextLoader(file_path).load()

    elif ext in ["xls", "xlsx"]:
        df = pd.read_excel(file_path)
        return [Document(page_content=df.to_string())]

    else:
        raise ValueError("Unsupported format")
