import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its attributes. Required by tests/test_recommender.py"""
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


@dataclass
class UserProfile:
    """Represents a user's taste preferences. Required by tests/test_recommender.py"""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP implementation of the recommendation logic. Required by tests/test_recommender.py"""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Scores and ranks songs for a given user profile, returning top k results."""
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
        """Returns a plain-language explanation of why a song was recommended."""
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
    """Loads songs from a CSV file and returns a list of dictionaries with typed values."""
    songs = []
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
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """Scores a single song against user preferences. Returns a (score, explanation) tuple."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre", ""):
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"] == user_prefs.get("mood", ""):
        score += 1.0
        reasons.append("mood match (+1.0)")

    target_energy = user_prefs.get("energy", 0.5)
    energy_gap = abs(song["energy"] - target_energy)
    energy_score = round(1.0 - energy_gap, 2)
    score += energy_score
    reasons.append(f"energy similarity (+{energy_score})")

    if user_prefs.get("mood") == "happy" and song["valence"] > 0.7:
        score += 0.5
        reasons.append("high valence bonus (+0.5)")

    if user_prefs.get("likes_acoustic", False) and song["acousticness"] > 0.6:
        score += 0.5
        reasons.append("acoustic preference (+0.5)")

    explanation = ", ".join(reasons)
    return round(score, 2), explanation


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores all songs, ranks them, and returns the top k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, explanation = score_song(user_prefs, song)
        scored.append((song, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]