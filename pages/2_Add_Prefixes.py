import pandas as pd
import streamlit as st

from core.docx_prefixes import (
    DEFAULT_MULTI_LIST_SECTIONS,
    DEFAULT_PREFIX_MAP,
    multi_list_to_rows,
    prefix_map_to_rows,
    process_docx,
    rows_to_multi_list,
    rows_to_prefix_map,
)

st.set_page_config(page_title="Add Section Prefixes", page_icon="🏷️", layout="wide")

st.title("Add Section Prefixes")
st.markdown(
    """
    Adds a short section code to each numbered entry — e.g. `2. Author (2024).`
    becomes `RJA2. Author (2024).`

    **Run *Reverse Section Numbering* on your file first**, then upload the
    result here. The prefix assigned to each item is determined by its
    surrounding H2 and H3 headings.

    - Only `.docx` files are supported.
    - Edit the mapping tables below before processing — start from the bundled
      academic CV defaults or clear them and build your own.
    """
)

st.divider()

# ── File upload ──────────────────────────────────────────────────────────────

uploaded = st.file_uploader("Upload your CV (.docx)", type=["docx"])

# ── Standard prefix map ──────────────────────────────────────────────────────

st.subheader("Standard section prefixes")
st.caption(
    "Each row maps an (H2 heading, H3 heading) pair to a prefix string. "
    "Leave H3 Heading blank for sections with no H3."
)

default_rows = prefix_map_to_rows(DEFAULT_PREFIX_MAP)
prefix_df = pd.DataFrame(default_rows)

edited_prefix_df = st.data_editor(
    prefix_df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "H2 Heading": st.column_config.TextColumn("H2 Heading", width="large"),
        "H3 Heading": st.column_config.TextColumn("H3 Heading", width="large"),
        "Prefix":     st.column_config.TextColumn("Prefix",     width="small"),
    },
    key="prefix_map_editor",
)

# ── Multi-list sections ──────────────────────────────────────────────────────

st.subheader("Multi-list sections (no H3 dividers)")
st.caption(
    "Some H2 sections contain several unnested lists with no H3 heading "
    "between them (e.g. *Works in Progress*). List the prefixes in order, "
    "comma-separated — the first prefix is applied to the first list found, "
    "the second to the second, and so on."
)

default_multi_rows = multi_list_to_rows(DEFAULT_MULTI_LIST_SECTIONS)
multi_df = pd.DataFrame(default_multi_rows)

edited_multi_df = st.data_editor(
    multi_df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "H2 Heading":                st.column_config.TextColumn("H2 Heading",                width="large"),
        "Prefixes (comma-separated)": st.column_config.TextColumn("Prefixes (comma-separated)", width="medium"),
    },
    key="multi_list_editor",
)

# ── Process ──────────────────────────────────────────────────────────────────

st.divider()

if uploaded and st.button("Process", type="primary"):
    prefix_map = rows_to_prefix_map(edited_prefix_df.to_dict("records"))
    multi_list = rows_to_multi_list(edited_multi_df.to_dict("records"))

    if not prefix_map and not multi_list:
        st.warning("The prefix mapping is empty — nothing to do.")
        st.stop()

    docx_bytes = uploaded.read()

    with st.spinner("Processing…"):
        try:
            result_bytes, warnings = process_docx(docx_bytes, prefix_map, multi_list)
        except Exception as e:
            st.error(f"Processing failed: {e}")
            st.stop()

    if warnings:
        with st.expander(f"{len(warnings)} warning(s) — some items were left unchanged", expanded=True):
            for w in warnings:
                st.warning(w)
    else:
        st.success("Done — all items matched a prefix rule.")

    out_name = uploaded.name.replace(".docx", "-prefixed.docx")
    st.download_button(
        label="Download result",
        data=result_bytes,
        file_name=out_name,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
elif not uploaded:
    st.info("Upload a file above to enable processing.")
