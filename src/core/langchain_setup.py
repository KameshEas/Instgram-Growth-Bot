from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from src.config import settings
from src.logger import setup_logger

logger = setup_logger("langchain_setup")

def initialize_llm():
    """Initialize LangChain LLM with Groq"""
    logger.info("Initializing LLM (Groq)...")
    
    llm = ChatGroq(
        model_name=settings.GROQ_MODEL,
        temperature=settings.GROQ_TEMPERATURE,
        groq_api_key=settings.GROQ_API_KEY,
        max_tokens=2000,
    )
    
    logger.info(f"✅ LLM initialized: {settings.GROQ_MODEL}")
    return llm

def initialize_memory():
    """Initialize conversation memory"""
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        max_token_limit=2048
    )
    return memory

# Initialize on module load
try:
    llm = initialize_llm()
    memory = initialize_memory()
    logger.info("✅ LangChain setup complete")
except Exception as e:
    logger.warning(f"⚠️ LangChain initialization: {str(e)} (this is OK during setup)")
