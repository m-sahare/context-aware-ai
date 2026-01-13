def detect_intent(text: str) -> str:
    text = text.lower()

    if "exam" in text or "test" in text:
        return "exam_stress"
    elif "sad" in text or "depressed" in text:
        return "emotional_support"
    elif "hello" in text or "hi" in text:
        return "greeting"
    else:
        return "general"


def get_response(message: str):
    intent = detect_intent(message)

    if intent == "exam_stress":
        return (
            "I understand exams can be stressful. Try revising key topics and take short breaks.",
            intent
        )

    if intent == "emotional_support":
        return (
            "I'm here for you. Do you want to talk about what's making you feel this way?",
            intent
        )

    if intent == "greeting":
        return (
            "Hello! How can I help you today?",
            intent
        )

    return (
        "Thanks for sharing. Tell me more.",
        intent
    )
