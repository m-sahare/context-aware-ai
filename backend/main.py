from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .response_strategy import get_response
from .memory_manager import save_message, get_conversation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    message: str

@app.post("/chat")
def chat(user_input: UserInput):
    try:
        user_message = user_input.message

        save_message("user", user_message)

        ai_reply, intent = get_response(user_message)

        save_message("ai", ai_reply)

        return {
            "intent": intent,
            "reply": ai_reply
        }

    except Exception as e:
        print("SERVER ERROR:", e)
        return {
            "intent": "error",
            "reply": "Sorry, something went wrong on the server."
        }
