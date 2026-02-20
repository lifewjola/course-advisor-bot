from clients import gemini_client
from google.genai import types

EMBEDDING_MODEL = "gemini-embedding-001"

def get_embedding(text: str) -> list[float]:
    """
    Generates a vector embedding for the given text using the new Google GenAI SDK.
    """
    try:
        response = gemini_client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=768
            )
        )
        
        return response.embeddings[0].values

    except Exception as e:
        print(f"Embedding failed: {e}")
        return []
