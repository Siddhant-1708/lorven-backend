def predict_mood(transcription, tone_features):
    text = transcription.lower()
    pitch = tone_features.get("pitch", 0)
    energy = tone_features.get("energy", 0)
    tempo = tone_features.get("tempo", 0)

    if "sad" in text or energy < 0.01:
        return "sad"
    elif "angry" in text or tempo > 150:
        return "angry"
    elif "excited" in text or pitch > 3000:
        return "excited"
    else:
        return "happy"
