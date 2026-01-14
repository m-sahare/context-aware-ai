# response_strategy.py
import os

# Optional: OpenAI / Gemini imports
try:
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
    LLM_AVAILABLE = True
except:
    LLM_AVAILABLE = False

def generate_response_llm(message, history):
    """
    Returns (reply_text, intent)
    Uses LLM if available, otherwise fallback keyword-based responses.
    """
    # Fallback keyword-based logic
    fallback_reply, fallback_intent = keyword_response(message)

    if not LLM_AVAILABLE:
        return fallback_reply, fallback_intent

    # Prepare LLM messages
    llm_messages = []
    for m in history:
        role = "user" if m["type"] == "user" else "assistant"
        llm_messages.append({"role": role, "content": m["text"]})
    llm_messages.append({"role": "user", "content": message})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or replace with Gemini model
            messages=llm_messages,
            temperature=0.7
        )
        reply_text = response.choices[0].message.content.strip()

        # Simple intent detection
        lower = reply_text.lower()
        if any(word in lower for word in ["exam", "stress", "worried"]):
            intent = "comforting"
        elif any(word in lower for word in ["fun", "party", "excited", "hungry", "food"]):
            intent = "fun"
        elif any(word in lower for word in ["help", "emergency", "urgent"]):
            intent = "urgent"
        else:
            intent = "default"

        return reply_text, intent

    except Exception as e:
        print("LLM error:", e)
        return fallback_reply, fallback_intent

def keyword_response(message):
    """
    Fallback keyword-based responses
    """
    msg = message.lower()
    if "exam" in msg or "stressed" in msg:
        return "Don't worry, you can do it! Stay calm and focus.", "comforting"
    elif "hungry" in msg or "food" in msg:
        return "Maybe grab a snack or a meal!", "fun"
    elif "fun" in msg or "party" in msg or "excited" in msg:
        return "That sounds exciting! Enjoy yourself!", "fun"
    elif "help" in msg or "emergency" in msg:
        return "I'm here to help! What exactly is happening?", "urgent"
    else:
        return "I'm here to chat with you about anything you want!", "default"
