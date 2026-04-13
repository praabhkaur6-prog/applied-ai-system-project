# 🎵 Music Recommender Simulation

## Project Summary

This project simulates a content-based music recommendation system. It represents songs as data with attributes like genre, mood, and energy, and scores them against a user's taste profile to generate personalized suggestions. The system explains every recommendation in plain language, and the project includes bias analysis and evaluation across multiple user profiles.

---

## How The System Works

Real-world platforms like Spotify combine two main strategies to generate recommendations. **Collaborative filtering** identifies users with similar listening histories and recommends what those users enjoyed. **Content-based filtering** analyzes the audio features of songs themselves — tempo, energy, mood, genre — and finds tracks that match a specific user's taste profile. This simulation focuses entirely on content-based filtering, scoring every song in the catalog against a user's preferences and returning the highest-ranked results.

### Algorithm Recipe

Each song is scored using the following weighted rules:

| Rule | Points |
|---|---|
| Genre matches user's favorite genre | +2.0 |
| Mood matches user's favorite mood | +1.0 |
| Energy closeness (1.0 minus the gap) | 0.0 – 1.0 |
| High valence bonus (when mood is "happy" and valence > 0.7) | +0.5 |
| Acoustic preference bonus (when user likes acoustic and acousticness > 0.6) | +0.5 |

Songs are then sorted highest to lowest score and the top K results are returned.

### Features Used

**Song object attributes:** `genre`, `mood`, `energy`, `valence`, `acousticness`, `tempo_bpm`, `danceability`

**UserProfile attributes:** `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`

### Data Flow

```
Input (User Preferences)
        ↓
For each song in songs.csv:
    → score_song(user_prefs, song)
        ↓
Sorted list of (song, score, explanation)
        ↓
Output: Top K Recommendations
```

### Potential Biases

- Genre carries the highest weight (+2.0), so songs from an underrepresented genre will rarely surface even if they match mood and energy perfectly.
- The dataset has more pop and lofi songs than other genres, which may cause those genres to dominate results even for users who didn't specify them.
- The system has no memory — it treats every session as a fresh start with no learning over time.

---

## Terminal Output Screenshots

### High-Energy Pop Profile
```
Profile: High-Energy Pop
1. Good Vibes Only by Indigo Parade  | Score: 4.50
2. Sunrise City by Neon Echo         | Score: 4.47
3. Golden Hour by Sunset Dial        | Score: 4.43
4. Gym Hero by Max Pulse             | Score: 3.42
5. Rooftop Lights by Indigo Parade   | Score: 2.41
```

### Chill Lofi Profile
```
Profile: Chill Lofi
1. Library Rain by Paper Lanterns    | Score: 4.47
2. Midnight Coding by LoRoom         | Score: 4.46
3. Rainy Seoul by Cafe Hana          | Score: 4.45
4. Focus Flow by LoRoom              | Score: 3.48
5. Spacewalk Thoughts by Orbit Bloom | Score: 2.40
```

### Deep Intense Rock Profile
```
Profile: Deep Intense Rock
1. Storm Runner by Voltline          | Score: 3.99
2. Thunder Protocol by Voltline      | Score: 3.98
3. Broken Strings by The Hollow      | Score: 2.82
4. Gym Hero by Max Pulse             | Score: 1.97
5. Neon Jungle by Circuit Rex        | Score: 1.94
```