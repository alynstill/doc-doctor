import streamlit as st

from core.docx_numbering import process_docx

st.set_page_config(page_title="Reverse Section Numbering", page_icon="🔢", layout="centered")

st.title("Reverse Section Numbering")
st.markdown(
    """
    Renumbers the items in each section of your CV so the oldest entry becomes
    **#1** (true chronological order), while preserving all content and
    formatting.

    - Items must currently be numbered **newest-first** (1, 2, 3 … from the top).
    - Numbers reset at each section boundary (detected by a reset to "1.").
    - Only `.docx` files are supported. Convert `.doc` files in Word or Google
      Docs first.
    """
)

st.divider()

uploaded = st.file_uploader("Upload your CV (.docx)", type=["docx"])

if uploaded:
    docx_bytes = uploaded.read()

    if st.button("Process", type="primary"):
        with st.spinner("Processing…"):
            try:
                result_bytes, stats = process_docx(docx_bytes)
            except Exception as e:
                st.error(f"Processing failed: {e}")
                st.stop()

        st.success(
            f"Done — {stats['sections']} section(s), "
            f"{stats['items']} item(s) found, "
            f"{stats['renumbered']} renumbered."
        )

        out_name = uploaded.name.replace(".docx", "-chrono-numbered.docx")
        st.download_button(
            label="Download result",
            data=result_bytes,
            file_name=out_name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
