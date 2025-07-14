import os
import logging
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write

logger = logging.getLogger()

model = MusicGen.get_pretrained('facebook/musicgen-small')
model.set_generation_params(duration=10)

def generate_music_clip(mood, style):
    prompt = f"{mood} {style}"
    logger.info(f"[INFO] Generating track for prompt: {prompt}")
    wav = model.generate([prompt])
    filename = f"generated_tracks/{mood}_{style}.wav"
    audio_write(filename[:-4], wav[0].cpu(), model.sample_rate, strategy="loudness", format="wav")
    return filename
