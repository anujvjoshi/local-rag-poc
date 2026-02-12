import streamlit as st
import os
from auth import *
from document_loader import load_document
from vector_store import create_vector_store, load_vector_store
from rag_pipeline import split_docs, build_qa_chain

init_db()

st.title("🔒 Local RAG System (POC)")

if "user" not in st.session_state:
    st.session_state.user = None

menu = ["Login", "Register"]

if not st.session_state.user:
    choice = st.sidebar.selectbox("Menu", menu)

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if choice == "Register":
        if st.sidebar.button("Register"):
            if register(username, password):
                st.success("Registered successfully")
            else:
                st.error("User already exists")

    if choice == "Login":
        if st.sidebar.button("Login"):
            if login(username, password):
                st.session_state.user = username
                st.success("Logged in")
            else:
                st.error("Invalid credentials")

else:
    st.sidebar.write(f"Logged in as: {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None

    user_folder = f"db/{st.session_state.user}"
    os.makedirs(user_folder, exist_ok=True)

    uploaded_file = st.file_uploader("Upload document")

    if uploaded_file:
        file_path = os.path.join(user_folder, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        docs = load_document(file_path)
        split_documents = split_docs(docs)
        vectorstore = create_vector_store(split_documents, user_folder)

        st.success("Document indexed!")

    if os.path.exists(os.path.join(user_folder, "index.faiss")):
        vectorstore = load_vector_store(user_folder)
        qa = build_qa_chain(vectorstore)

        question = st.text_input("Ask a question")

        if question:
            answer = qa.run(question)
            st.write("### Answer")
            st.write(answer)
