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
    popularity: int
    release_decade: str
    mood_tag: str
    danceability_tag: str
    era_tag: str


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
            row["popularity"] = int(row["popularity"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict, mode: str = "balanced") -> Tuple[float, str]:
    """
    Scores a single song against user preferences using the selected ranking mode.
    Modes: 'balanced', 'genre-first', 'mood-first', 'energy-focused'
    Returns a (score, explanation) tuple.
    """
    score = 0.0
    reasons = []

    # --- Genre ---
    genre_weight = 3.0 if mode == "genre-first" else 2.0
    if song["genre"] == user_prefs.get("genre", ""):
        score += genre_weight
        reasons.append(f"genre match (+{genre_weight})")

    # --- Mood ---
    mood_weight = 3.0 if mode == "mood-first" else 1.0
    if song["mood"] == user_prefs.get("mood", ""):
        score += mood_weight
        reasons.append(f"mood match (+{mood_weight})")

    # --- Mood tag bonus ---
    if song.get("mood_tag") == user_prefs.get("mood_tag", ""):
        score += 0.5
        reasons.append("mood tag match (+0.5)")

    # --- Energy ---
    target_energy = user_prefs.get("energy", 0.5)
    energy_gap = abs(song["energy"] - target_energy)
    energy_weight = 2.0 if mode == "energy-focused" else 1.0
    energy_score = round(energy_weight * (1.0 - energy_gap), 2)
    score += energy_score
    reasons.append(f"energy similarity (+{energy_score})")

    # --- Valence bonus ---
    if user_prefs.get("mood") == "happy" and song["valence"] > 0.7:
        score += 0.5
        reasons.append("high valence bonus (+0.5)")

    # --- Acoustic preference ---
    if user_prefs.get("likes_acoustic", False) and song["acousticness"] > 0.6:
        score += 0.5
        reasons.append("acoustic preference (+0.5)")

    # --- Popularity bonus (new attribute) ---
    if user_prefs.get("prefers_popular", False) and song["popularity"] > 80:
        score += 0.5
        reasons.append(f"popularity bonus (+0.5, score={song['popularity']})")

    # --- Era preference (new attribute) ---
    preferred_era = user_prefs.get("preferred_era", "")
    if preferred_era and song.get("era_tag") == preferred_era:
        score += 0.5
        reasons.append(f"era match ({preferred_era}, +0.5)")

    explanation = ", ".join(reasons)
    return round(score, 2), explanation


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, mode: str = "balanced") -> List[Tuple[Dict, float, str]]:
    """
    Scores all songs using the selected mode, applies a diversity penalty to avoid
    repeat artists, and returns the top k as (song, score, explanation) tuples.

    Modes: 'balanced' | 'genre-first' | 'mood-first' | 'energy-focused'
    """
    scored = []
    for song in songs:
        score, explanation = score_song(user_prefs, song, mode=mode)
        scored.append((song, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)

    # Diversity penalty: penalize repeat artists
    results = []
    seen_artists = set()
    for song, score, explanation in scored:
        artist = song["artist"]
        if artist in seen_artists:
            score = round(score - 1.0, 2)
            explanation += ", diversity penalty (-1.0)"
        else:
            seen_artists.add(artist)
        results.append((song, score, explanation))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:k]