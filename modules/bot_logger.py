from clients import supabase

def log_interaction(user_question: str, bot_answer: str):
    """
    Saves the Q&A pair to the database asynchronously (fire and forget).
    """
    data = {
        "user_question": user_question,
        "bot_answer": bot_answer
    }
    
    try:
        supabase.table("chat_logs").insert(data).execute()
    except Exception as e:
        print(f"Logging Error: {e}")