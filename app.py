from flask import Flask, request, jsonify, render_template
from core.config import Config
from core.chat_memory import store_chat_history, get_categorized_history, get_memory, redis_client
from core.rag_pipeline import generate_ai_response
from langchain_core.messages import HumanMessage, AIMessage

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

@app.route("/", methods=["GET", "POST"])
def home():
    user_id = "user1"
    
    if request.method == 'POST':
        query = request.form.get('query', '')
        
        # Check Memory First
        memory = get_memory(user_id)
        existing = [msg.content.strip().lower() for msg in memory.messages if isinstance(msg, HumanMessage)]
        
        # (Simplified duplicate check logic)
        if query.strip().lower() in existing:
             # Find previous response logic here if needed
             pass

        # Generate New Response
        response = generate_ai_response(query)
        store_chat_history(user_id, query, response)
        return jsonify({"response": response})

    # Load History for UI
    history = get_memory(user_id).messages
    return render_template('index.html', history=history)

@app.route("/history", methods=["GET"])
def history_endpoint():
    return jsonify({"history": get_categorized_history("user1")})

@app.route("/clear-history", methods=["POST"])
def clear_history():
    try:
        get_memory("user1").clear()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/delete-history-item", methods=["POST"])
def delete_history_item():
    user_id = "user1"
    data = request.get_json()
    msg_to_del = data.get("message", "").strip().lower()
    
    memory = get_memory(user_id)
    msgs = memory.messages
    
    filtered = [m for m in msgs if not (isinstance(m, HumanMessage) and m.content.strip().lower() == msg_to_del)]
    
    redis_client.delete(f"message_store:{user_id}")
    for m in filtered: memory.add_message(m)
    
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)