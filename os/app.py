import streamlit as st

st.set_page_config(page_title="OS Visualizer", layout="wide")

pg = st.navigation(
    [
        st.Page("home.py", title="Home", default=True),
        st.Page("pages/1_CPU_Scheduling.py", title="CPU Scheduling"),
        st.Page("pages/2_Page_Replacement.py", title="Page Replacement"),
        st.Page("pages/3_Bankers_Algorithm.py", title="Banker's Algorithm"),
    ],
    position="top",
)
pg.run()
