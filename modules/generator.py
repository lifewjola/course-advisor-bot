from clients import gemini_client
from modules.prompts import format_prompt, SYSTEM_INSTRUCTION
from google.genai import types

MODEL_NAME = "gemini-2.5-flash-lite"


def get_answer(query: str, context: str, chat_history: list) -> str:
    """
    Sends the prompt to Gemini WITH conversation history.
    
    Args:
        query: The new user question.
        context: The text chunks retrieved from Supabase.
        chat_history: List of dicts [{"role": "user", "content": "hi"}, ...]
    """
    
    contents = []

    for msg in chat_history:
        role = "model" if msg["role"] == "assistant" else "user"
        
        contents.append(types.Content(
            role=role,
            parts=[types.Part(text=msg["content"])]
        ))

    final_prompt = format_prompt(query, context)
    
    contents.append(types.Content(
        role="user",
        parts=[types.Part(text=final_prompt)]
    ))

    google_search_tool = types.Tool(
        google_search=types.GoogleSearch()
    )
    
    try:
        response = gemini_client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
            response_mime_type="text/plain",
            tools=[google_search_tool],
            temperature=0.3,
            max_output_tokens=1000,
            system_instruction=SYSTEM_INSTRUCTION
            )
        )
        return response.text
        
    except Exception as e:
        return f"I encountered an error generating the response: {e}"