import streamlit as st
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
LANGCHAIN_API_KEY = st.secrets.get("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = st.secrets.get("LANGCHAIN_PROJECT", "Summrly")

os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY if LANGCHAIN_API_KEY else ""
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT

st.set_page_config(page_title="Summrly AI", page_icon="⚡", layout="wide")

if "mode" not in st.session_state:
    st.session_state.mode = "PDF"

st.title("Summrly AI")
st.caption("Understand more. Read less.")

with st.sidebar:
    st.header("⚙️ Settings")
    summary_length = st.slider("Summary Length", 50, 500, 200)

    if st.button("Clear / New"):
        st.session_state.clear()
        st.rerun()

mode = st.radio("Select Input Type", ["PDF", "Text"], horizontal=True)

if mode != st.session_state.mode:
    st.session_state.clear()
    st.session_state.mode = mode
    st.rerun()

pdf_file = None
text_input = None

if mode == "PDF":
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"])

if mode == "Text":
    text_input = st.text_area("Paste your text here", height=200)

summarize = st.button("Generate Summary")

if GROQ_API_KEY:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=GROQ_API_KEY,
        temperature=0.3
    )
else:
    st.warning("Add GROQ_API_KEY in secrets.toml")

map_prompt = PromptTemplate.from_template("Summarize:\n{text}")
reduce_prompt = PromptTemplate.from_template("Final summary in {length} words:\n{text}")

map_chain = map_prompt | llm | StrOutputParser()
reduce_chain = reduce_prompt | llm | StrOutputParser()

if summarize:
    if not GROQ_API_KEY:
        st.error("API key missing")
    else:
        try:
            docs = None

            if mode == "PDF" and pdf_file is not None:
                with open("temp.pdf", "wb") as f:
                    f.write(pdf_file.read())
                loader = PyPDFLoader("temp.pdf")
                docs = loader.load()

            elif mode == "Text" and text_input and text_input.strip():
                docs = [Document(page_content=text_input)]

            else:
                st.error("Please provide input")

            if docs:
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1200,
                    chunk_overlap=100
                )

                split_docs = splitter.split_documents(docs)[:8]

                progress = st.progress(0)
                partial_summaries = []

                for i, doc in enumerate(split_docs):
                    s = map_chain.invoke({"text": doc.page_content})
                    partial_summaries.append(s)
                    progress.progress((i + 1) / len(split_docs))

                combined = " ".join(partial_summaries)

                placeholder = st.empty()
                final_summary = ""

                for chunk in reduce_chain.stream({
                    "text": combined,
                    "length": summary_length
                }):
                    final_summary += chunk
                    placeholder.markdown(final_summary + "▌")

                placeholder.markdown(final_summary)

        except Exception as e:
            error_msg = str(e).lower()

            if "token" in error_msg or "rate_limit" in error_msg or "request too large" in error_msg:
                st.error("⚠️ Content too large or server busy. Try smaller input or try again later.")
            else:
                st.error("⚠️ Something went wrong. Please try again.")

st.markdown("---")
st.markdown(
    "<h5 style='text-align: center; color: grey;'>Built with  ❤️  by <a href='https://github.com/paranjaysoni' target='_blank' style='color: grey; text-decoration: none;'>Paranjay Soni</a></h5>",
    unsafe_allow_html=True
)
