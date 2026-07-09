import pandas as pd
import sqlite3

def get_connection():
    return sqlite3.connect('data/music.db')

def top_genres_by_popularity(n=15):
    conn = get_connection()
    query = f"""
    SELECT track_genre, ROUND(AVG(popularity), 2) AS avg_popularity, COUNT(*) AS num_tracks
    FROM tracks
    GROUP BY track_genre
    ORDER BY avg_popularity DESC
    LIMIT {n}
    """
    return pd.read_sql(query, conn)

def danceability_vs_popularity():
    conn = get_connection()
    query = """
    SELECT 
      CASE 
        WHEN danceability < 0.33 THEN 'Low'
        WHEN danceability < 0.66 THEN 'Medium'
        ELSE 'High'
      END AS danceability_group,
      ROUND(AVG(popularity), 2) AS avg_popularity,
      COUNT(*) AS num_tracks
    FROM tracks
    GROUP BY danceability_group
    ORDER BY avg_popularity DESC
    """
    return pd.read_sql(query, conn)

def explicit_vs_popularity():
    conn = get_connection()
    query = """
    SELECT explicit, ROUND(AVG(popularity), 2) AS avg_popularity, COUNT(*) AS num_tracks
    FROM tracks
    GROUP BY explicit
    """
    return pd.read_sql(query, conn)

def feature_correlations():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM tracks", conn)
    features = ['popularity', 'danceability', 'energy', 'valence', 'tempo', 'acousticness', 'loudness', 'speechiness']
    return df[features].corr()['popularity'].drop('popularity').sort_values(ascending=False)