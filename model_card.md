# 🎧 Model Card: AI Music Recommender System

---

## 1. Model Name

**VibeMatch AI 1.0**

---

## 2. Intended Use

This system is designed to recommend songs based on a user’s input such as genre, mood, or artist. It generates personalized suggestions by matching user preferences with song features.

The model assumes that users have a general idea of what they want (for example, “pop” or “chill”) and uses that as input.

This project is mainly for **classroom exploration**, not real-world deployment. It demonstrates how recommendation systems work in a simplified way.

---

## 3. How the Model Works

The system works in two main steps:

First, it **retrieves relevant songs** from the dataset based on the user’s input (this is the RAG step). For example, if a user enters “pop,” it filters songs that match that genre, mood, or artist.

Then, it **scores each song** based on how well it matches user preferences.

The model looks at features such as:

* Genre
* Mood
* Energy level
* Acousticness
* Popularity (in some cases)

Each song gets points depending on how closely it matches the user’s preferences. For example, matching genre gives higher points than other features.

After scoring, songs are ranked from highest to lowest, and the top results are returned with explanations.

Compared to the original version, I added:

* A retrieval step (RAG)
* Better explanation of recommendations
* Improved structure with modular files

---

## 4. Data

The dataset contains **20 songs** with different genres and moods such as pop, lofi, rock, ambient, jazz, and EDM.

Each song includes features like:

* Energy
* Tempo
* Valence (happiness level)
* Danceability
* Acousticness
* Popularity

The dataset is small and manually created, so it does not represent all types of music. Some genres are more common than others.

---

## 5. Strengths

The system works well when:

* The user provides clear inputs like “pop,” “chill,” or “rock”
* Songs strongly match genre and mood
* Energy levels align with user expectations

The scoring system does a good job of ranking songs in a logical way, and the explanations help users understand why a song was recommended.

---

## 6. Limitations and Bias

The system has several limitations:

* It relies heavily on genre, which can dominate the results
* Some genres (like pop and lofi) are overrepresented in the dataset
* It does not understand complex preferences like mixed moods
* It does not learn from user behavior over time

This means the system may favor certain types of music and may not work well for users with unique or complex tastes.

---

## 7. Evaluation

I tested the system using different inputs such as:

* pop
* happy
* rock

I checked whether:

* The system returned results
* The top songs matched expectations
* The explanations made sense

The system worked well for common queries, but struggled when the input did not clearly match the dataset.

The test file also verifies that:

* Recommendations are sorted correctly
* Explanations are not empty

---

## 8. Future Work

If I were to improve this system, I would:

* Add more songs to the dataset
* Include user history for better personalization
* Improve retrieval using smarter matching (not just keywords)
* Add more diverse recommendations
* Use a real machine learning model instead of rule-based scoring

---

## 9. Personal Reflection

This project helped me understand how recommendation systems actually work behind the scenes.

One interesting thing I learned is how much the results depend on the dataset and scoring rules. Even small changes in weights can completely change recommendations.

It also made me realize that real music apps are much more complex because they learn from user behavior over time.

---
