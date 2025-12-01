import os
import re
import logging
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain.prompts import PromptTemplate
from core.config import Config
from langchain_community.retrievers import PineconeHybridSearchRetriever
from pinecone_text.sparse import BM25Encoder
from pinecone import Pinecone

logger = logging.getLogger(__name__)

# Singleton Global Retriever
_retriever = None

def get_retriever():
    """Initializes and returns the Hybrid Retriever (Singleton Pattern)"""
    global _retriever
    if _retriever is not None:
        return _retriever

    if not os.path.exists(Config.BM25_PARAMS_PATH):
        logger.error("BM25 not found! Run ingest.py first.")
        return None

    try:
        embeddings = OllamaEmbeddings(model=Config.EMBEDDING_MODEL)
        
        bm25_encoder = BM25Encoder().default()
        bm25_encoder.load(Config.BM25_PARAMS_PATH)
        pc = Pinecone(api_key=Config.PINECONE_API_KEY)
        index = pc.Index(Config.PINECONE_INDEX_NAME)

        _retriever = PineconeHybridSearchRetriever(
            embeddings=embeddings,
            sparse_encoder=bm25_encoder,
            index=index,
            top_k=4,     
            alpha=0.5    # 50% Keyword importance, 50% Meaning importance
        )
        logger.info("Pinecone Native Hybrid Retriever initialized.")
        return _retriever

    except Exception as e:
        logger.error(f"Error initializing retriever: {e}")
        return None

prompt_template = PromptTemplate(
    input_variables=["context", "query"],
    template="""You are an expert HR Assistant. Your goal is to answer based ONLY on the provided documents.

INSTRUCTIONS:
1. If the user asks for a short answer (e.g., "in 1 line", "briefly", "yes or no"), provide strictly a single sentence.
2. If the user asks for details, provide a comprehensive answer.
3. If no specific length is requested, keep it concise (2-3 sentences max).
4. Do NOT use phrases like "According to the document" or "Based on the text". Just give the answer.
5. NEVER mention phrases like "According to the document", "As stated in the text", "In document [X]", or "Based on the provided context".
6. If the user input is a closing remark like "ok", "thank you", "thanks", "great", or "understood", DO NOT look in the context. Instead, reply professionally: "You're welcome! Feel free to reach out if you have more questions regarding HR policies."
7. NEVER mention page numbers or file names.

CONTEXT:
{context}

USER QUESTION:
{query}

YOUR ANSWER:"""
)

def generate_ai_response(query):
    retriever = get_retriever()
    if not retriever:
        return "System Error: Knowledge base not loaded."

    relevant_docs = retriever.invoke(query)
    if not relevant_docs:
        return "I can only answer questions related to HR policies."

    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    full_prompt = prompt_template.format(context=context, query=query)
    
    # Generate
    llm = OllamaLLM(model=Config.LLM_MODEL)
    raw_response = llm.invoke(full_prompt)
    
    # Clean <think> tags
    clean_response = re.sub(r'<think>.*?</think>', '', raw_response, flags=re.DOTALL).strip()
    return clean_response