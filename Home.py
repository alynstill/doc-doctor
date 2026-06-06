import streamlit as st

pg = st.navigation({
    "": [st.Page("pages/home.py", title="Home", icon="🩺", default=True)],
    "Watermark": [
        st.Page("pages/1_Reverse_Numbering.py", title="Reverse Section Numbering", icon="🔢"),
        st.Page("pages/2_Add_Prefixes.py", title="Add Section Prefixes", icon="🏷️"),
    ],
})
pg.run()
