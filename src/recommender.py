import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

    # ✅ FIX: add default values (prevents test crashes)
    popularity: int = 0
    release_decade: str = ""
    mood_tag: str = ""
    danceability_tag: str = ""
    era_tag: str = ""


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP implementation of the recommendation logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Scores and ranks songs for a given user profile."""
        scored = []

        for song in self.songs:
            score = 0.0

            if song.genre == user.favorite_genre:
                score += 2.0

            if song.mood == user.favorite_mood:
                score += 1.0

            energy_gap = abs(song.energy - user.target_energy)
            score += (1.0 - energy_gap)

            if user.likes_acoustic and song.acousticness > 0.6:
                score += 0.5

            scored.append((song, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [s for s, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns explanation of recommendation."""
        reasons = []

        if song.genre == user.favorite_genre:
            reasons.append(f"genre match ({song.genre})")

        if song.mood == user.favorite_mood:
            reasons.append(f"mood match ({song.mood})")

        energy_gap = abs(song.energy - user.target_energy)
        reasons.append(f"energy similarity ({1.0 - energy_gap:.2f} pts)")

        if user.likes_acoustic and song.acousticness > 0.6:
            reasons.append("acoustic preference match")

        return ", ".join(reasons) if reasons else "general match"


def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs safely from CSV."""
    songs = []

    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                row = {k.strip(): v.strip() for k, v in row.items()}

                row["id"] = int(row["id"])
                row["energy"] = float(row["energy"])
                row["tempo_bpm"] = float(row["tempo_bpm"])
                row["valence"] = float(row["valence"])
                row["danceability"] = float(row["danceability"])
                row["acousticness"] = float(row["acousticness"])
                row["popularity"] = int(row.get("popularity", 0))

                songs.append(row)

    except FileNotFoundError:
        print("❌ songs.csv not found.")
    except Exception as e:
        print(f"⚠️ Error loading songs: {e}")

    return songs


def score_song(user_prefs: Dict, song: Dict, mode: str = "balanced") -> Tuple[float, str]:
    """Scores a song with explanation."""

    score = 0.0
    reasons = []

    # Genre
    genre_weight = 3.0 if mode == "genre-first" else 2.0
    if song["genre"] == user_prefs.get("genre", ""):
        score += genre_weight
        reasons.append(f"genre match (+{genre_weight})")

    # Mood
    mood_weight = 3.0 if mode == "mood-first" else 1.0
    if song["mood"] == user_prefs.get("mood", ""):
        score += mood_weight
        reasons.append(f"mood match (+{mood_weight})")

    # Mood tag
    if song.get("mood_tag") == user_prefs.get("mood_tag", ""):
        score += 0.5
        reasons.append("mood tag match (+0.5)")

    # Energy
    target_energy = user_prefs.get("energy", 0.5)
    energy_gap = abs(song["energy"] - target_energy)
    energy_weight = 2.0 if mode == "energy-focused" else 1.0
    energy_score = round(energy_weight * (1.0 - energy_gap), 2)

    score += energy_score
    reasons.append(f"energy similarity (+{energy_score})")

    # Valence bonus
    if user_prefs.get("mood") == "happy" and song["valence"] > 0.7:
        score += 0.5
        reasons.append("high valence bonus (+0.5)")

    # Acoustic
    if user_prefs.get("likes_acoustic", False) and song["acousticness"] > 0.6:
        score += 0.5
        reasons.append("acoustic preference (+0.5)")

    # Popularity
    if user_prefs.get("prefers_popular", False) and song["popularity"] > 80:
        score += 0.5
        reasons.append(f"popularity bonus (+0.5)")

    # Era
    if user_prefs.get("preferred_era") == song.get("era_tag"):
        score += 0.5
        reasons.append("era match (+0.5)")

    return round(score, 2), ", ".join(reasons)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, mode: str = "balanced"):
    """Returns top k recommendations with diversity penalty."""

    scored = [(*score_song(user_prefs, s, mode), s) for s in songs]
    scored = [(s, sc, exp) for sc, exp, s in scored]

    scored.sort(key=lambda x: x[1], reverse=True)

    results = []
    seen_artists = set()

    for song, score, explanation in scored:
        if song["artist"] in seen_artists:
            score -= 1.0
            explanation += ", diversity penalty (-1.0)"
        else:
            seen_artists.add(song["artist"])

        results.append((song, round(score, 2), explanation))

    results.sort(key=lambda x: x[1], reverse=True)

    return results[:k]