from musicgen_utils import generate_music_clip

print("[TEST] Starting manual generation...")
path = generate_music_clip("angry")  # only one argument now
print(f"[TEST] Done. Track saved at: {path}")

