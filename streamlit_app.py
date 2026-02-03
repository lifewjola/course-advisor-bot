import streamlit as st
st.set_page_config(page_title="Course Advisor AI", page_icon="🎓", layout="centered")

from modules.retriever import get_context
from modules.generator import get_answer
from modules.bot_logger import log_interaction

from utils import load_css
load_css("styles.css")

with st.sidebar:
    st.image("bucclogo.png", width=150) 
    st.title("Course Advisor AI")
    st.info(
        "I can assist with:\n"
        "- UMIS & Course Registration\n"
        "- CGPA & Grading Rules\n"
        "- Carryovers & Extra Units\n"
        "- Course Overload Applications"
    )
    if st.button("Start New Conversation", type="primary"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    if st.button("🔐 Admin Access"):
        st.switch_page("pages/admin_panel.py")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.image("babcock.png", )

st.title("Course Advisor AI")
st.markdown(
    """
    **Welcome.** I am here to help you navigate academics as a BUCC student. 
    """
)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your question here..."):
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        
        with st.spinner("Searching knowledge base..."):
            try:
                context_data = get_context(prompt)
                
                full_response = get_answer(
                    query=prompt, 
                    context=context_data, 
                    chat_history=st.session_state.messages
                )
                
                message_placeholder.markdown(full_response)
                
                log_interaction(prompt, full_response)

            except Exception as e:
                full_response = "I encountered an error connecting to the server. Please try again."
                message_placeholder.error(full_response)
                print(f"Error: {e}")

    st.session_state.messages.append({"role": "assistant", "content": full_response})