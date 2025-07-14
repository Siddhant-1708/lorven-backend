import os
import uuid
import shutil
import logging
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydub import AudioSegment

from faster_whisper_utils import transcribe_audio
from mood_utils import extract_mood
from musicgen_utils import generate_music_clip
from spotify_utils import search_tracks_for_mood

# === SETUP ===
os.makedirs("uploads", exist_ok=True)
os.makedirs("generated_tracks", exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

app = FastAPI()

# === CORS for frontend ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use ["http://localhost:5173"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Serve generated music files ===
app.mount("/generated_tracks", StaticFiles(directory="generated_tracks"), name="generated")

# === Upload + Process Voice ===
@app.post("/upload-voice/")
async def upload_voice(file: UploadFile = File(...), style: str = Form(...)):
    try:
        # Generate unique ID and save uploaded file
        file_id = str(uuid.uuid4())
        temp_path = f"uploads/{file_id}.wav"

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"[INFO] Saved uploaded file: {temp_path}")

        # Transcribe
        transcript = transcribe_audio(temp_path)
        logger.info(f"[INFO] Transcription: {transcript}")

        # Re-encode to clean WAV
        clean_path = f"uploads/{file_id}_clean.wav"
        try:
            audio = AudioSegment.from_file(temp_path)
            audio.export(clean_path, format="wav")
            logger.info(f"[INFO] Re-encoded file to: {clean_path}")
        except Exception as e:
            logger.warning(f"[WARN] Could not re-encode audio: {e}")
            clean_path = temp_path

        # Extract mood
        mood = extract_mood(transcript)
        logger.info(f"[INFO] Predicted Mood: {mood}")

        # Generate music
        logger.info(f"[INFO] Generating track for prompt: {mood} {style}")
        try:
            generated_path = generate_music_clip(mood, style)
            logger.info(f"[INFO] Generated Music Path: {generated_path}")
        except Exception as e:
            logger.error("[ERROR] Music generation failed", exc_info=True)
            return {"error": "Music generation failed"}

        # Get Spotify recommendations
        try:
            recommendations = search_tracks_for_mood(mood)
            logger.info(f"[INFO] Found {len(recommendations)} Spotify tracks")
        except Exception as e:
            logger.warning("[WARN] Failed to fetch recommendations", exc_info=True)
            recommendations = []

        # Return JSON response
        return {
            "transcript": transcript,
            "mood": mood,
            "music_path": f"/generated_tracks/{os.path.basename(generated_path)}",
            "recommendations": recommendations,
        }

    except Exception as e:
        logger.error("[ERROR] Failed to process voice input", exc_info=True)
        return {"error": "Failed to process voice input"}
