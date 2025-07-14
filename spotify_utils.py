import os
import logging
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

logger = logging.getLogger("spotify_utils")

client_id = os.getenv("SPOTIPY_CLIENT_ID") or "d610601b2f364da7941b3e8655c2eb37"
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET") or "b2babf3c50f041eda2c3e9bfc7945cac"

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = Spotify(auth_manager=auth_manager)

def search_tracks_for_mood(mood, limit=5):
    logger.info(f"[SPOTIFY] Searching tracks for mood: {mood}")
    query = f"{mood} mood"
    results = sp.search(q=query, type="track", limit=limit)
    return [
        {
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "url": track["external_urls"]["spotify"]
        }
        for track in results["tracks"]["items"]
    ]
