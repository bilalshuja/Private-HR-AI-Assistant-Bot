import redis
from datetime import datetime, timedelta
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from core.config import Config

# Redis Client
redis_client = redis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=Config.REDIS_DB,
    decode_responses=True
)

def get_memory(user_id):
    """Returns RedisChatMessageHistory instance"""
    return RedisChatMessageHistory(session_id=user_id, url=Config.REDIS_URL)

def store_chat_history(user_id, query, response):
    memory = get_memory(user_id)
    
    # Duplicate Check
    existing_messages = [msg.content.strip().lower() for msg in memory.messages if isinstance(msg, HumanMessage)]
    if query.strip().lower() in existing_messages:
        return

    timestamp = datetime.now().timestamp()
    memory.add_messages([
        HumanMessage(content=query, additional_kwargs={"timestamp": timestamp}),
        AIMessage(content=response, additional_kwargs={"timestamp": timestamp})
    ])

def get_categorized_history(user_id):
    memory = get_memory(user_id)
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    categorized = {"Today": [], "Yesterday": [], "Older": []}

    for msg in memory.messages:
        timestamp = msg.additional_kwargs.get("timestamp")
        if not timestamp: continue
        
        msg_date = datetime.fromtimestamp(float(timestamp)).date()
        entry = {
            "type": "User" if isinstance(msg, HumanMessage) else "Bot",
            "message": msg.content
        }

        if msg_date == today:
            categorized["Today"].append(entry)
        elif msg_date == yesterday:
            categorized["Yesterday"].append(entry)
        else:
            categorized["Older"].append(entry)
            
    return categorized