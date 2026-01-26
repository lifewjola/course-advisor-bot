import streamlit as st
from supabase import create_client, Client
from google import genai

try:
    SUPABASE_URL = st.secrets["supabase"]["url"]
    SUPABASE_KEY = st.secrets["supabase"]["key"]
    GEMINI_API_KEY = st.secrets["gemini"]["GEMINI_API_KEY"]
except (FileNotFoundError, KeyError) as e:
    st.error(f"Secrets configuration error: {e}")
    st.stop()

# 2. INITIALIZE GEMINI (New SDK)
@st.cache_resource
def get_gemini_client() -> genai.Client:
    """
    Initializes the Google GenAI client (v1.0+).
    Cached to avoid re-instantiating on every rerun.
    """
    return genai.Client(api_key=GEMINI_API_KEY)

# 3. INITIALIZE SUPABASE
@st.cache_resource
def get_supabase_client() -> Client:
    """
    Initializes the Supabase client.
    """
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# Expose clients for imports
gemini_client = get_gemini_client()
supabase = get_supabase_client()