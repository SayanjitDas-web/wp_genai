import streamlit as st

st.set_page_config(layout="wide")
st.title("Website Preview")

container = st.container()

if 'htmlvalue' not in st.session_state:
    container.write("No preview available")
else:
    container.html(
        st.session_state.htmlvalue if len(st.session_state.htmlvalue) != 0 else "<h1>Somthing went wrong while creating the website</h1>"
    )

