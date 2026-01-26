from clients import supabase
from modules.embedder import get_embedding

def get_context(query: str, match_threshold=0.5, match_count=5) -> str:
    """
    1. Embeds the user query.
    2. Searches Supabase for matching chunks.
    3. Returns a single string of combined context.
    """
    query_vector = get_embedding(query)
    if not query_vector:
        return ""

    params = {
        "query_embedding": query_vector,
        "match_threshold": match_threshold,
        "match_count": match_count
    }
    
    try:
        response = supabase.rpc("match_documents", params).execute()
        
        matches = response.data
        if not matches:
            return ""
            
        context_text = "\n\n---\n\n".join([match['content'] for match in matches])
        return context_text
        
    except Exception as e:
        print(f"Retriever Error: {e}")
        return ""