def predict_mood(text: str, tone: dict) -> str:
    text = text.lower()

    # Sentiment keywords (expandable)
    if any(word in text for word in ["happy", "excited", "fun", "yay"]):
        return "happy"
    elif any(word in text for word in ["sad", "tired", "down", "lonely"]):
        return "sad"
    elif any(word in text for word in ["calm", "relaxed", "peaceful"]):
        return "calm"
    elif any(word in text for word in ["angry", "mad", "annoyed"]):
        return "angry"

    # Tone fallback if text is neutral
    if tone["rms"] > 0.05 and tone["tempo"] > 120:
        return "energetic"
    elif tone["tempo"] < 70:
        return "calm"

    return "neutral"
