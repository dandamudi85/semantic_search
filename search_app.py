"""
    Create an Streamlit app that does the following:

    - Reads an input from the user
    - Embeds the input
    - Search the vector DB for the entries closest to the user input
    - Outputs/displays the closest entries found
"""
import streamlit as st

st.write("""
# Movie Search
""")
st.text_input("Search",key="search",label_visibility="hidden")
value = st.session_state.search
print("Value:",value)