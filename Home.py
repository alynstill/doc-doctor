import streamlit as st

st.set_page_config(page_title="Doc Doctor", page_icon="🩺", layout="centered")

st.title("Doc Doctor")
st.subheader("Tools for preparing academic career documents")

st.markdown(
    """
    Use the sidebar to select a tool.

    ---

    ### Available tools

    **Reverse Section Numbering**
    Renumbers the items in each section of a `.docx` CV so that the oldest
    entry becomes #1 (true chronological order). Items are assumed to start in
    reverse chronological order (newest = 1). Numbers restart with each new
    section.

    **Add Section Prefixes**
    Adds a short section-based code to each numbered entry — for example
    turning `2. Author (2024).` into `RJA2. Author (2024).` Run *Reverse
    Section Numbering* on your file first, then use this tool. The prefix
    mapping is fully editable in the UI: start from the bundled academic CV
    defaults or build your own from scratch.

    ---

    All processing happens in your browser session — your files are never
    stored on a server.
    """
)
