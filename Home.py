import streamlit as st

st.set_page_config(page_title="Doc Doctor", page_icon="🩺", layout="centered")

st.title("Doc Doctor")
st.subheader("Tools for academics who prefer research and teaching over formatting their CVs")

st.markdown(
    """
    ### Quick Start:

    1. Use the sidebar to select a tool.
    2. Upload the file (usually a `.docx` exported from Faculty Success).
    3. Review the default settings for the tool and adjust if needed.
    4. Download the processed file.

    All processing happens in your browser session — your files are never
    stored on a server.
    
    ### About these tools:

    These tools are born from frustration seeing how time-consuming the process of formatting academic CVs for different purposes was.
    The time spent manually editing word files and proof-reading for formatting errors is time taken away from research and teaching, and a source of stress for academics who are already juggling many responsibilities.

    No good nerd can see a problem like that without trying to write code to solve it, so here we are!

    The tools here are the result of automating some of the common tasks needed for junior faculty at University of Maryland when preparing annual review materials, grant applications and other activity and resume-based documents.
    They've been built and tested for a small number of users but should work with any `.docx` file.
    If you have suggestions for other tools or improvements to these, please let me know! You can send suggestions to [dev@tomatotomato.co.uk](mailto:dev@tomatotomato.co.uk).

    Each tool is designed to perform a single task, so you can use them independently or in combination, depending on the format you need to generate.

    **Note** Most tools work with `.docx` files.
    Faculty success often outputs only a `.doc` file, so you may need to open the exported file and save it as a `.docx` file before using these tools.

    ---

    ### Available tools

    **Reverse Section Numbering**
    If you CV is in reverse chronological order (newest = 1), this tool will reverse the numbering so that the oldest entry becomes #1. 

    This is useful for applications that require true chronological order, and to ensure that numbering doesn't change as new entries are added.
    Numbers restart with each new section.

    **Add Section Prefixes**
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
