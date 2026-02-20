import numpy as np

# Note: faiss and sentence_transformers are not installed by default
# They are optional dependencies. To enable RAG functionality, install:
# pip install faiss-cpu sentence_transformers

# Stub implementation for RAG service
documents = []
embeddings = None
index = None

def build_index(text_chunks):
    """Build FAISS index from text chunks. Requires: pip install faiss-cpu sentence_transformers"""
    global embeddings, index, documents
    try:
        from sentence_transformers import SentenceTransformer
        import faiss
        
        model = SentenceTransformer('all-MiniLM-L6-v2')
        documents = text_chunks
        embeddings = model.encode(text_chunks)
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings))
    except ImportError as e:
        print(f"RAG dependencies not installed: {e}")
        print("Install with: pip install faiss-cpu sentence_transformers")

def retrieve(query):
    """Retrieve similar documents. Requires: pip install faiss-cpu sentence_transformers"""
    if index is None or embeddings is None:
        return []
    
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        query_embedding = model.encode([query])
        distances, indices = index.search(query_embedding, k=3)
        return [documents[i] for i in indices[0] if i < len(documents)]
    except ImportError:
        return []

def search_documents(query):
    """Search documents by query."""
    if not documents:
        return [{"content": "No documents indexed", "score": 0}]
    
    results = retrieve(query)
    return [{"content": doc, "score": 1.0/(i+1)} for i, doc in enumerate(results)]
