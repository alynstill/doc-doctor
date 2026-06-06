import streamlit as st

st.set_page_config(page_title="Doc Doctor", page_icon="🩺", layout="centered")

st.markdown(
    """
    <style>
    [data-testid="stPageLink"] p {
        font-size: 1.25rem;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Doc Doctor")
st.subheader("Get back to research & teaching — let the tools handle the formatting")

st.markdown(
    """
    ### Quick Start:

    1. Use the sidebar to select a tool.
    2. Upload your `.docx` file. Faculty Success exports `.doc` — open it in Word or Google Docs and Save As `.docx` first.
    3. Review the default settings and adjust if needed.
    4. Download the processed file.

    All processing happens in your browser session — your files are never
    stored on a server.

    ### About these tools:

    These tools came from frustration at how time-consuming formatting your academic CV for different purposes can be.
    Time you spend manually editing Word files and proofreading for formatting errors is time taken away from research and teaching — and an unnecessary source of stress when you're already juggling many responsibilities.

    So naturally, we wrote some code.

    The tools here automate common tasks you face when preparing annual reviews, grant applications, and other activity and resume-based documents.
    They've been built and tested for a small number of users but should work with any `.docx` file.
    If you have suggestions for other tools or improvements, please send them to [dev@tomatotomato.co.uk](mailto:dev@tomatotomato.co.uk).

    Each tool performs a single task, so you can use them independently or in combination depending on what you need.
    **Note** Most tools work with `.docx` files.
    If Faculty Success outputs a `.doc` file, open and save it as a `.docx` file before using these tools.
    ---

    ### Available tools
    """
)

st.page_link("pages/1_Reverse_Numbering.py", label="Reverse Section Numbering", icon="🔢")
st.markdown(
    """
    If your CV is in reverse chronological order (newest = 1), this tool will reverse the numbering so that the oldest entry becomes #1.

    This is useful for applications that require true chronological order, and to ensure that numbering doesn't change as new entries are added.
    Numbers restart with each new section.
    """
)

st.page_link("pages/2_Add_Prefixes.py", label="Add Section Prefixes", icon="🏷️")
st.markdown(
    """
    Adds a short section-based code to each numbered entry — for example
    turning `2. AuthorName (2024).` into `RJA2. Author (2024).`

    This is useful when you want to reference items in a cover letter or other document,
    and want to make it easy for reviewers to find the relevant entry in your CV.

    The tool uses the headings in your document to determine the prefix.
    It comes with a default mapping of common academic CV sections to prefixes,
    but you can edit this mapping in the UI to fit your document structure and preferences.

    ---

    All processing happens in your browser session — your files are never
    stored on a server.
    """
)
