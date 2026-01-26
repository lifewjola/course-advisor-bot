import streamlit as st

def load_css(file_name="app/styles.css"):
    """
    Injects CSS styles into the Streamlit app.
    """
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        print(f"Warning: {file_name} not found.")