# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json, os
from .response_strategy import generate_response_llm

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your domain in production
    allow_methods=["*"],
    allow_headers=["*"]
)

HISTORY_FILE = "user_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_history(data):
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.get("/get_history")
async def get_history(user_id: str):
    histories = load_history()
    return histories.get(user_id, [])

@app.post("/save_history")
async def save_user_history(request: Request):
    data = await request.json()
    user_id = data["user_id"]
    history = data["history"]

    histories = load_history()
    histories[user_id] = history
    save_history(histories)
    return {"status": "success"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_id = data["user_id"]
    message = data["message"]

    histories = load_history()
    user_history = histories.get(user_id, [])

    # Generate AI response (LLM or fallback)
    reply, intent = generate_response_llm(message, user_history)

    # Update history
    user_history.append({"type": "user", "text": message})
    user_history.append({"type": "ai", "text": reply, "intentClass": f"intent-{intent}"})

    histories[user_id] = user_history
    save_history(histories)

    return {"reply": reply, "intent": intent}
