from services.rag_service import search_documents

def rag_search(query):
    results = search_documents(query)
    return results

# Langchain tools temporarily disabled due to missing dependencies
# To enable, install: pip install langchain sentence_transformers faiss-cpu

def company_knowledge(query: str) -> str:
    """Search company documents for relevant information."""
    return search_documents(query)


