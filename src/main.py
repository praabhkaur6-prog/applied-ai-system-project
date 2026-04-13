import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from recommender import load_songs, recommend_songs


def print_table(label: str, recommendations, mode: str = "balanced") -> None:
    """Prints a formatted ASCII table of recommendations."""
    print(f"\n{'='*80}")
    print(f"  Profile: {label}  |  Mode: {mode.upper()}")
    print(f"{'='*80}")
    print(f"  {'#':<3} {'Title':<25} {'Artist':<18} {'Score':<7} Why")
    print(f"  {'-'*3} {'-'*25} {'-'*18} {'-'*7} {'-'*35}")
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        title = song['title'][:24]
        artist = song['artist'][:17]
        print(f"  {i:<3} {title:<25} {artist:<18} {score:<7.2f} {explanation}")
    print()


def main() -> None:
    base = os.path.dirname(os.path.abspath(__file__))
    songs = load_songs(os.path.join(base, "..", "data", "songs.csv"))
    print(f"Loaded songs: {len(songs)}")

    # ── Profile 1: High-Energy Pop ──────────────────────────────────────────
    pop_prefs = {
        "genre": "pop", "mood": "happy", "energy": 0.85,
        "mood_tag": "euphoric", "prefers_popular": True, "preferred_era": "modern"
    }
    print_table("High-Energy Pop", recommend_songs(pop_prefs, songs, k=5, mode="balanced"))
    print_table("High-Energy Pop", recommend_songs(pop_prefs, songs, k=5, mode="genre-first"), mode="genre-first")

    # ── Profile 2: Chill Lofi ───────────────────────────────────────────────
    lofi_prefs = {
        "genre": "lofi", "mood": "chill", "energy": 0.38,
        "likes_acoustic": True, "mood_tag": "nostalgic", "preferred_era": "modern"
    }
    print_table("Chill Lofi", recommend_songs(lofi_prefs, songs, k=5, mode="balanced"))
    print_table("Chill Lofi", recommend_songs(lofi_prefs, songs, k=5, mode="mood-first"), mode="mood-first")

    # ── Profile 3: Deep Intense Rock ────────────────────────────────────────
    rock_prefs = {
        "genre": "rock", "mood": "intense", "energy": 0.90,
        "mood_tag": "aggressive", "preferred_era": "recent"
    }
    print_table("Deep Intense Rock", recommend_songs(rock_prefs, songs, k=5, mode="balanced"))
    print_table("Deep Intense Rock", recommend_songs(rock_prefs, songs, k=5, mode="energy-focused"), mode="energy-focused")


if __name__ == "__main__":
    main()