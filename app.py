import streamlit as st
import pandas as pd
import joblib
import sys

sys.path.append('.')
from src.styling import load_css
from src.search import find_song, render_song_card

st.set_page_config(page_title="Music Recommender", page_icon="🎵", layout="wide")
load_css()


@st.cache_resource
def load_model():
    return joblib.load('models/nn_model.pkl')


@st.cache_resource
def load_scaler():
    return joblib.load('models/scaler.pkl')


@st.cache_data
def load_data():
    return pd.read_csv('data/clean_tracks.csv')


df = load_data()
model = load_model()
scaler = load_scaler()

feature_cols = ['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'loudness', 'speechiness']
X_scaled = scaler.transform(df[feature_cols])

st.title("🎵 Music Recommender")
st.write("Find songs that sound similar to your favorites.")

song_input = st.text_input("Search for a song")

if song_input:
    idx, match_type = find_song(df, song_input)

    if idx is None:
        st.error("Song not found. Try a different spelling or song.")
    else:
        distances, indices = model.kneighbors([X_scaled[idx]], n_neighbors=11)
        similar_indices = indices[0][1:]
        results = df.iloc[similar_indices]

        if match_type != "exact":
            matched_name = df.loc[idx, 'track_name']
            st.info(f"Showing results for: **{matched_name}**")

        st.write("### Recommended for you")
        for _, row in results.iterrows():
            st.markdown(render_song_card(row), unsafe_allow_html=True)
