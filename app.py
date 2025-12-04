import uuid
from flask import Flask, request, jsonify, render_template, session
from core.config import Config
from core.chat_memory import store_chat_history, get_categorized_history, get_memory, redis_client
from core.rag_pipeline import generate_ai_response
from langchain_core.messages import HumanMessage, AIMessage

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# --- 👇 HELPER FUNCTION: Get or Create User ID ---
def get_user_id():
   
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())  
    return session['user_id']

@app.route("/", methods=["GET", "POST"])
def home():
    user_id = get_user_id()  
    if request.method == 'POST':
        query = request.form.get('query', '')
        
        memory = get_memory(user_id)
        existing = [msg.content.strip().lower() for msg in memory.messages if isinstance(msg, HumanMessage)]
        
        if query.strip().lower() in existing:
            
             pass
        response = generate_ai_response(query)
        store_chat_history(user_id, query, response)
        return jsonify({"response": response})

    history = get_memory(user_id).messages
    return render_template('index.html', history=history)

@app.route("/history", methods=["GET"])
def history_endpoint():
    user_id = get_user_id() 
    return jsonify({"history": get_categorized_history(user_id)})

@app.route("/clear-history", methods=["POST"])
def clear_history():
    user_id = get_user_id()
    try:
        get_memory(user_id).clear()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/delete-history-item", methods=["POST"])
def delete_history_item():
    user_id = get_user_id()
    data = request.get_json()
    msg_to_del = data.get("message", "").strip().lower()
    
    memory = get_memory(user_id)
    msgs = memory.messages
    
    filtered = [m for m in msgs if not (isinstance(m, HumanMessage) and m.content.strip().lower() == msg_to_del)]
    
    redis_client.delete(f"message_store:{user_id}") 
    
    for m in filtered: memory.add_message(m)
    
    return jsonify({"status": "success"})

# Helper route to check response (Updated to use dynamic ID)
@app.route("/get-response", methods=["POST"])
def get_response_route():
    user_id = get_user_id()
    data = request.get_json()
    query = data.get("query", "").strip().lower()
    
    memory = get_memory(user_id)
    messages = memory.messages
    
    for i, msg in enumerate(messages):
        if isinstance(msg, HumanMessage) and msg.content.strip().lower() == query:
            if i + 1 < len(messages) and isinstance(messages[i+1], AIMessage):
                return jsonify({"response": messages[i+1].content})
                
    return jsonify({"response": None})

if __name__ == "__main__":
    app.run(debug=True, port=5000)