import os
import dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores.faiss import FAISS

def get_pdf_text(pdf_docs):
    """Initialize empty text, loop through all documents and read them appending to text."""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(raw_text):
    """Returns a list of text chunks"""
    text_splitter = CharacterTextSplitter(
        separator="\n", 
        chunk_size=1024, 
        chunk_overlap= 200, 
        length_function=len
    )
    chuncks = text_splitter.split_text(raw_text)
    return chuncks

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def main():
    dotenv.load_dotenv()
    st.set_page_config(page_title="Provice context to your AI", page_icon=":books:")
    st.header("Import your documents :books:")
    st.text_input("Ask a question about the documents you provided:")
    
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Choose your PDF's for upload...", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get the pdf text
                raw_text = get_pdf_text(pdf_docs)
                # get the text chuncks
                text_chunks = get_text_chunks(raw_text)
                st.write(text_chunks)
                # create vector embbeddings
                vector_store = get_vectorstore(text_chunks)

if __name__ == "__main__":
    main()
    # use "streamlit run app.py" to run the script