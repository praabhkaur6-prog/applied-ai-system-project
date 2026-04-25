import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from recommender import recommend_songs
from retriever import retrieve_candidates


def print_table(label: str, recommendations, mode: str = "balanced") -> None:
    """Print formatted recommendation results"""
    print(f"\n{'='*80}")
    print(f"  Query: {label}  |  Mode: {mode.upper()}")
    print(f"{'='*80}")
    print(f"  {'#':<3} {'Title':<25} {'Artist':<18} {'Score':<7} Why")
    print(f"  {'-'*3} {'-'*25} {'-'*18} {'-'*7} {'-'*35}")

    for i, (song, score, explanation) in enumerate(recommendations, 1):
        title = song['title'][:24]
        artist = song['artist'][:17]
        print(f"  {i:<3} {title:<25} {artist:<18} {score:<7.2f} {explanation}")

    print()


def main():
    try:
        # 🔹 USER INPUT
        query = input("Enter genre, mood, or artist: ").strip().lower()

        if not query:
            print("❌ Please enter a valid input.")
            return

        # 🔹 STEP 1: RETRIEVAL (RAG)
        candidates = retrieve_candidates(query)

        if not candidates:
            print("❌ No matching songs found.")
            return

        print(f"\n✅ Retrieved {len(candidates)} candidate songs.")

        # 🔹 STEP 2: AI REASONING
        user_prefs = {
            "genre": query,
            "mood": query,
            "energy": 0.5,
            "likes_acoustic": False
        }

        recommendations = recommend_songs(user_prefs, candidates, k=5)

        if not recommendations:
            print("❌ No recommendations generated.")
            return

        # 🔹 STEP 3: OUTPUT
        print_table(query, recommendations)

    except Exception as e:
        print(f"⚠️ Error occurred: {e}")


if __name__ == "__main__":
    main()