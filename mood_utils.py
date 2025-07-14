# mood_utils.py
import librosa
import numpy as np
import logging

logger = logging.getLogger(__name__)

# Mapping moods to related keywords
MOOD_KEYWORDS = {
    "happy": ["happy", "joy", "excited", "glad", "smile", "cheerful", "wonderful", "great"],
    "sad": ["sad", "down", "unhappy", "cry", "depressed", "blue", "gloomy", "miserable"],
    "angry": ["angry", "mad", "furious", "irritated", "annoyed", "rage"],
    "relaxed": ["relaxed", "calm", "peaceful", "chill", "easygoing", "laid back"],
    "romantic": ["love", "romantic", "affection", "sweetheart", "passion", "crush"],
    "motivated": ["motivated", "determined", "focus", "ambition", "goal", "driven", "productive"],
    "anxious": ["anxious", "nervous", "worried", "stress", "panic", "uneasy"],
    "bored": ["bored", "meh", "dull", "tired", "lazy", "uninspired"],
}

def extract_mood(transcription: str) -> str:
    logger.info(f"[MOOD] Analyzing transcription: {transcription}")
    transcription_lower = transcription.lower()

    # Initialize a score tracker for each mood
    mood_scores = {mood: 0 for mood in MOOD_KEYWORDS}

    # Count keyword occurrences per mood
    for mood, keywords in MOOD_KEYWORDS.items():
        for word in keywords:
            if word in transcription_lower:
                mood_scores[mood] += 1

    # Select the mood with the highest keyword match
    best_mood = max(mood_scores, key=mood_scores.get)

    logger.info(f"[MOOD] Scores: {mood_scores}")
    logger.info(f"[MOOD] Predicted Mood: {best_mood}")

    return best_mood
