import streamlit as st
import sys
sys.path.append('..')
from src.queries import (
    top_genres_by_popularity,
    danceability_vs_popularity,
    explicit_vs_popularity,
    feature_correlations
)
import plotly.express as px

st.title("📊 Music Data Insights")
st.write("Exploring what drives song popularity, using SQL queries against a 81K-track dataset.")

# Chart 1: Top genres
st.subheader("Top Genres by Average Popularity")
genres_df = top_genres_by_popularity()
fig1 = px.bar(genres_df, x='track_genre', y='avg_popularity', 
              hover_data=['num_tracks'],
              labels={'track_genre': 'Genre', 'avg_popularity': 'Avg Popularity'})
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Danceability
st.subheader("Danceability vs Popularity")
dance_df = danceability_vs_popularity()
fig2 = px.bar(dance_df, x='danceability_group', y='avg_popularity',
              hover_data=['num_tracks'],
              labels={'danceability_group': 'Danceability Level', 'avg_popularity': 'Avg Popularity'})
st.plotly_chart(fig2, use_container_width=True)
st.caption("Note: popularity plateaus between medium and high danceability — it's not a straight-line relationship.")

# Chart 3: Explicit content
st.subheader("Explicit vs Non-Explicit Tracks")
explicit_df = explicit_vs_popularity()
explicit_df['explicit'] = explicit_df['explicit'].map({0: 'Non-explicit', 1: 'Explicit'})
fig3 = px.bar(explicit_df, x='explicit', y='avg_popularity',
              hover_data=['num_tracks'],
              labels={'explicit': '', 'avg_popularity': 'Avg Popularity'})
st.plotly_chart(fig3, use_container_width=True)

# Chart 4: Correlations
st.subheader("Which Audio Features Correlate with Popularity?")
corr = feature_correlations()
fig4 = px.bar(corr, orientation='h', labels={'value': 'Correlation with Popularity', 'index': 'Feature'})
st.plotly_chart(fig4, use_container_width=True)
st.caption("No single audio feature strongly predicts popularity on its own — correlations are all close to zero. This suggests popularity is driven more by factors like artist recognition and promotion than the song's raw sound.")