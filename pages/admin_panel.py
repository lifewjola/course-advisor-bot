import pandas as pd
import time

import streamlit as st
st.set_page_config(page_title="Admin Panel", page_icon="🔒", layout="wide")

from clients import supabase
from modules.upserter import add_chunk, delete_chunk, update_chunk

from utils import load_css
load_css("app/styles.css")

def check_password():
    """Returns True if the user is logged in."""
    if st.session_state.get("password_correct", False):
        return True

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.header("🔒 Admin Login")
        password = st.text_input("Enter Admin Password", type="password")
        
        if st.button("Login"):
            if password == st.secrets["admin"]["password"]:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Incorrect password")
    return False

if not check_password():
    st.stop()  

def load_data(table_name):
    """Fetches all data from a table."""
    try:
        response = supabase.table(table_name).select("*").order('id', desc=True).execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Error loading {table_name}: {e}")
        return pd.DataFrame()

st.title("Admin Dashboard")
st.markdown("Manage AI bot knowledge base and view student interactions.")

tab1, tab2 = st.tabs(["Knowledge Base", "Chat Logs"])

with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Add New Content")
        with st.form("add_chunk_form"):
            new_text = st.text_area("Content text:", height=200)
            submitted = st.form_submit_button("Add to Knowledge Base")
            
            if submitted and new_text:
                with st.spinner("Embedding and saving..."):
                    if add_chunk(new_text):
                        st.success("Added successfully!")
                        time.sleep(1)
                        st.rerun()

    with col2:
        st.subheader("Existing Knowledge")
        df_kb = load_data('knowledge_base')
        
        if not df_kb.empty:
            st.dataframe(
                df_kb.drop(columns=['embedding']), 
                use_container_width=True,
                height=300
            )
            
            st.divider()
            st.write("### Edit or Delete")
            
            selected_id = st.selectbox("Select ID to modify:", df_kb['id'].tolist())
            
            current_row = df_kb[df_kb['id'] == selected_id].iloc[0]
            current_text = current_row['content']
            
            edit_text = st.text_area("Edit Content:", value=current_text, height=150)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Update Content"):
                    with st.spinner("Updating..."):
                        if update_chunk(selected_id, edit_text):
                            st.success("Updated!")
                            time.sleep(1)
                            st.rerun()
            
            with c2:
                if st.button("Delete Chunk", type="primary"):
                    with st.spinner("Deleting..."):
                        if delete_chunk(selected_id):
                            st.warning("Deleted.")
                            time.sleep(1)
                            st.rerun()
        else:
            st.info("Knowledge base is empty. Add some content on the left.")

with tab2:
    st.subheader("Student Interaction History")
    if st.button("Refresh Logs"):
        st.rerun()
    
    df_logs = load_data('chat_logs')
    
    if not df_logs.empty:
        cols = ['created_at', 'user_question', 'bot_answer']
        available_cols = [c for c in cols if c in df_logs.columns]
        
        st.dataframe(
            df_logs[available_cols], 
            use_container_width=True,
            height=600
        )
    else:
        st.info("No chat logs found yet.")