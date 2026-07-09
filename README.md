# 🎵 Music Recommendation System

A hybrid content-based and collaborative filtering music recommender built with Python, Pandas, and scikit-learn, wrapped in an interactive Streamlit app with a SQL-backed analytics dashboard.

**🔗 Live Demo:** [music-recommender-puuoytrtflrxd7gbhqd7ns.streamlit.app](https://music-recommender-puuoytrtflrxd7gbhqd7ns.streamlit.app/)

---

## Overview

This project recommends tracks to users by combining two approaches:

- **Content-based filtering** — recommends songs with similar audio/metadata features (e.g. tempo, genre, acoustic properties) to a track the user likes
- **Collaborative filtering** — recommends songs based on patterns across users with similar listening behavior

The hybrid approach helps address the cold-start problem common to pure collaborative filtering, while still surfacing personalized results beyond simple content similarity.

Built on the **Maharshi Pandya Spotify Tracks Dataset** (~81K unique tracks after cleaning).

## Features

- 🔍 Search and get recommendations for any track in the dataset
- 📊 Interactive analytics dashboard (SQL-backed) exploring track features, genre distributions, and dataset trends
- ⚡ Fast nearest-neighbor lookups via a pre-trained model, with pre-computed embeddings for low-latency serving
- 🎨 Custom-styled UI built on top of Streamlit

## Tech Stack

| Layer | Tools |
|---|---|
| Language | Python |
| Data Processing | Pandas, NumPy |
| Modeling | scikit-learn (Nearest Neighbors) |
| Database | SQLite |
| Visualization | Plotly |
| Frontend / App | Streamlit |
| Data Source | Maharshi Pandya Spotify Tracks Dataset (Kaggle) |

## Project Structure

```
music-recommender/
├── app.py                  # Main Streamlit app entry point
├── pages/
│   └── 1_Dashboard.py      # SQL-backed analytics dashboard
├── src/
│   ├── queries.py          # SQL query functions
│   └── styling.py          # Custom CSS loader
├── assets/
│   └── style.css           # App styling
├── data/
│   ├── clean_tracks.csv    # Cleaned dataset
│   └── music.db            # SQLite database for dashboard queries
├── models/
│   ├── nn_model.pkl        # Trained Nearest Neighbors model
│   └── scaler.pkl          # Feature scaler
├── sql_analysis.ipynb      # Exploratory SQL analysis
├── M1_LOG1.ipynb           # Model development notebook
└── requirements.txt
```

## Running Locally

```bash
# Clone the repo
git clone https://github.com/Arya-Adityasvg/music-recommender.git
cd music-recommender

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Future Improvements

- Add user-based collaborative filtering with real interaction data (currently simulated/derived from static features)
- Expand evaluation with additional metrics beyond hypothesis testing
- Add caching for faster cold-start load times on larger datasets

## Author

**Arya Aditya**
[LinkedIn](https://www.linkedin.com/in/arya-aditya-372800261/) · [GitHub](https://github.com/Arya-Adityasvg)
