import streamlit as st
from clients import supabase
from modules.embedder import get_embedding

def add_chunk(content: str) -> bool:
    """
    Takes raw text, embeds it, and saves both text and vector to Supabase.
    Returns True if successful.
    """
    try:
        vector = get_embedding(content)
        if not vector:
            st.error("Failed to generate embedding.")
            return False
            
        data = {
            "content": content,
            "embedding": vector
        }
        
        supabase.table('knowledge_base').insert(data).execute()
        return True
        
    except Exception as e:
        st.error(f"Database Error: {e}")
        return False

def delete_chunk(chunk_id: int) -> bool:
    """
    Deletes a chunk by ID.
    """
    try:
        supabase.table('knowledge_base').delete().eq('id', chunk_id).execute()
        return True
    except Exception as e:
        st.error(f"Delete Failed: {e}")
        return False

def update_chunk(chunk_id: int, new_content: str) -> bool:
    """
    Updates text and RE-CALCULATES the vector.
    """
    try:
        new_vector = get_embedding(new_content)
        
        data = {
            "content": new_content, 
            "embedding": new_vector,
            "updated_at": "now()" 
        }
        supabase.table('knowledge_base').update(data).eq('id', chunk_id).execute()
        return True
    except Exception as e:
        st.error(f"Update Failed: {e}")
        return False