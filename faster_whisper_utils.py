from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")

def transcribe_audio(file_path):
    segments, _ = model.transcribe(file_path)
    transcription = " ".join([segment.text for segment in segments])
    return transcription.strip()
