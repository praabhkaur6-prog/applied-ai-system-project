import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from recommender import load_songs, recommend_songs


def print_recommendations(label: str, recommendations) -> None:
    """Prints a formatted recommendation list for a given user profile."""
    print(f"\n{'='*50}")
    print(f" Profile: {label}")
    print(f"{'='*50}")
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"{i}. {song['title']} by {song['artist']}")
        print(f"   Score : {score:.2f}")
        print(f"   Why   : {explanation}")
        print()


def main() -> None:
    base = os.path.dirname(os.path.abspath(__file__))
    songs = load_songs(os.path.join(base, "..", "data", "songs.csv"))
    print(f"Loaded songs: {len(songs)}")

    # Profile 1: High-Energy Pop
    pop_prefs = {"genre": "pop", "mood": "happy", "energy": 0.85}
    pop_recs = recommend_songs(pop_prefs, songs, k=5)
    print_recommendations("High-Energy Pop", pop_recs)

    # Profile 2: Chill Lofi
    lofi_prefs = {"genre": "lofi", "mood": "chill", "energy": 0.38, "likes_acoustic": True}
    lofi_recs = recommend_songs(lofi_prefs, songs, k=5)
    print_recommendations("Chill Lofi", lofi_recs)

    # Profile 3: Deep Intense Rock
    rock_prefs = {"genre": "rock", "mood": "intense", "energy": 0.90}
    rock_recs = recommend_songs(rock_prefs, songs, k=5)
    print_recommendations("Deep Intense Rock", rock_recs)


if __name__ == "__main__":
    main()