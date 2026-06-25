from sqlalchemy import inspect
import uuid
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from core.config import Config
from core.database import db
from core.models import User
from core.chat_memory import store_chat_history, get_categorized_history, get_memory, redis_client
from core.rag_pipeline import generate_ai_response
from routes.auth import auth_bp
from langchain_core.messages import HumanMessage, AIMessage
from routes.admin_routes import admin_bp

app = Flask(__name__)
app.config.from_object(Config)

# --- 1. Database & Login Setup ---
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login' # Agar login nahi hai to yahan bhejo

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Auth Routes Register karein
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

# --- 2. Main Chat Routes (Secure) ---

@app.route("/", methods=["GET", "POST"])
@login_required  # 🔒 LOCK: Bina login koi access nahi kar sakta
def home():
    # ✅ CHANGE: Pehle 'get_user_id()' tha, ab database user id hai
    user_id = str(current_user.id) 
    
    if request.method == 'POST':
        query = request.form.get('query', '')
        
        # Memory Check (Aapka purana logic)
        memory = get_memory(user_id)
        existing = [msg.content.strip().lower() for msg in memory.messages if isinstance(msg, HumanMessage)]
        
        if query.strip().lower() in existing:
             pass # Logic skip for brevity, same as before

        # Generate Response
        response = generate_ai_response(query)
        store_chat_history(user_id, query, response)
        return jsonify({"response": response})

    # Load History
    history = get_memory(user_id).messages
    # User object bhi bhej rahe hain taake frontend par naam dikha sakein
    return render_template('index.html', history=history, user=current_user) 

@app.route("/history", methods=["GET"])
@login_required
def history_endpoint():
    # ✅ Sirf apni history dikhegi
    return jsonify({"history": get_categorized_history(str(current_user.id))})

@app.route("/clear-history", methods=["POST"])
@login_required
def clear_history():
    try:
        get_memory(str(current_user.id)).clear()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/delete-history-item", methods=["POST"])
@login_required
def delete_history_item():
    user_id = str(current_user.id)
    data = request.get_json()
    msg_to_del = data.get("message", "").strip().lower()
    
    memory = get_memory(user_id)
    msgs = memory.messages
    
    filtered = [m for m in msgs if not (isinstance(m, HumanMessage) and m.content.strip().lower() == msg_to_del)]
    
    redis_client.delete(f"message_store:{user_id}")
    
    for m in filtered: memory.add_message(m)
    
    return jsonify({"status": "success"})

@app.route("/get-response", methods=["POST"])
@login_required
def get_response_route():
    user_id = str(current_user.id)
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