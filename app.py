import streamlit as st
import pandas as pd
import joblib
import sys
sys.path.append('.')
from src.styling import load_css

st.set_page_config(page_title="Music Recommender", page_icon="🎵", layout="wide")
load_css()

df = pd.read_csv('data/clean_tracks.csv')
model = joblib.load('models/nn_model.pkl')
scaler = joblib.load('models/scaler.pkl')

feature_cols = ['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'loudness', 'speechiness']
X_scaled = scaler.transform(df[feature_cols])

st.title("🎵 Music Recommender")
st.write("Find songs that sound similar to your favorites.")

song_input = st.text_input("Search for a song")

if song_input:
    matches = df[df['track_name'].str.lower() == song_input.lower()]

    if matches.empty:
        st.error("Song not found. Try a different spelling or song.")
    else:
        idx = matches.index[0]
        distances, indices = model.kneighbors([X_scaled[idx]], n_neighbors=11)
        similar_indices = indices[0][1:]
        results = df.iloc[similar_indices]

        st.write("### Recommended for you")
        for _, row in results.iterrows():
            st.markdown(f"""
            <div class="song-card">
                <div>
                    <div class="song-title">{row['track_name']}</div>
                    <div class="song-artist">{row['artists']}</div>
                </div>
                <div class="song-artist">{row['track_genre']}</div>
            </div>
            """, unsafe_allow_html=True)