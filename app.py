import streamlit as st
import pandas as pd
import joblib

# Load everything we saved earlier
df = pd.read_csv('data/clean_tracks.csv')
model = joblib.load('models/nn_model.pkl')
scaler = joblib.load('models/scaler.pkl')

feature_cols = ['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'loudness', 'speechiness']
X_scaled = scaler.transform(df[feature_cols])

# Page title
st.title("🎵 Music Recommender")
st.write("Type a song name and get 10 similar songs back.")

# Text input box
song_input = st.text_input("Song name:")

if song_input:
    matches = df[df['track_name'].str.lower() == song_input.lower()]
    
    if matches.empty:
        st.error("Song not found. Try a different spelling or song.")
    else:
        idx = matches.index[0]
        distances, indices = model.kneighbors([X_scaled[idx]], n_neighbors=11)
        similar_indices = indices[0][1:]
        
        results = df.iloc[similar_indices][['track_name', 'artists']]
        st.write("### Recommended songs:")
        st.table(results)