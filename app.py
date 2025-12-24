import streamlit as st
from main import main  # change if your function name is different

st.set_page_config(page_title="Python App", layout="centered")

st.title("Python Live App")

if st.button("Run Program"):
    try:
        result = main()
        st.write(result)
    except Exception as e:
        st.error(e)
