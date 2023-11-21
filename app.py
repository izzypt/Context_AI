import os
import dotenv
import streamlit as st
from html_templates import css, bot_template, user_template
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings, OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

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
    #embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vector_store):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever=vector_store.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state['chat_history'] = response['chat_history']

    for i, message in enumerate(st.session_state['chat_history']):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
 
def main():
    dotenv.load_dotenv()
    st.set_page_config(page_title="Provide context to your AI", page_icon=":books:")
    
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state['conversation'] = None
    if "chat_history" not in st.session_state:
        st.session_state['chat_history'] = None

    st.header("Import your documents :books:")
    user_question = st.text_input("Ask a question about the documents you provided:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Choose your PDF's for upload...", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get the pdf text
                raw_text = get_pdf_text(pdf_docs)
                # get the text chuncks
                text_chunks = get_text_chunks(raw_text)
                # create vector embbeddings
                vector_store = get_vectorstore(text_chunks)
                # create conversation chain
                st.session_state['conversation'] = get_conversation_chain(vector_store) 


if __name__ == "__main__":
    main()
    # use "streamlit run app.py" to run the script