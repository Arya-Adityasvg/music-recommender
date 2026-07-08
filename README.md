# 🎵 Music Recommendation System

A content-based music recommender that suggests similar songs based on audio characteristics like danceability, energy, tempo, and mood.

## How it works

Each song is represented as a set of audio features (danceability, energy, valence, tempo, acousticness, loudness, speechiness). The recommender uses a Nearest Neighbors model with cosine similarity to find songs that are "close" to a given song in this feature space.

## Dataset

[Spotify Tracks Dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset) — ~114,000 tracks with audio features, cleaned down to ~81,000 unique songs after removing duplicate genre-tagged entries.

## Tech stack

- Python, pandas, numpy — data cleaning and processing
- scikit-learn — Nearest Neighbors model for similarity search
- Streamlit — web interface

## How to run locally

\`\`\`bash
pip install -r requirements.txt
streamlit run app.py
\`\`\`

## Future improvements

- Add collaborative filtering using real user listening data
- Deploy publicly
- Add audio feature visualizations for recommended songs