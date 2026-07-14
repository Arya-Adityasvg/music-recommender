"""Pure search and rendering functions — no Streamlit dependency."""
from difflib import get_close_matches
from html import escape


def find_song(df, query):
    """Tiered search: exact → partial (contains) → fuzzy matching.

    Returns (index, match_type) or (None, None) if no match.
    """
    query_lower = query.strip().lower()
    if not query_lower:
        return None, None

    # Tier 1: exact match
    exact = df[df['track_name'].str.lower() == query_lower]
    if not exact.empty:
        return exact.index[0], "exact"

    # Tier 2: partial match (query is contained in track name)
    partial = df[df['track_name'].str.lower().str.contains(query_lower, na=False)]
    if not partial.empty:
        return partial.index[0], "partial"

    # Tier 3: fuzzy match (close string similarity)
    all_titles = df['track_name'].str.lower().tolist()
    matches = get_close_matches(query_lower, all_titles, n=1, cutoff=0.6)
    if matches:
        fuzzy_idx = df[df['track_name'].str.lower() == matches[0]].index[0]
        return fuzzy_idx, "fuzzy"

    return None, None


def render_song_card(row):
    """Render a song card HTML with escaped data to prevent XSS."""
    title = escape(str(row['track_name']))
    artist = escape(str(row['artists']))
    genre = escape(str(row['track_genre']))
    return f"""
    <div class="song-card">
        <div>
            <div class="song-title">{title}</div>
            <div class="song-artist">{artist}</div>
        </div>
        <div class="song-artist">{genre}</div>
    </div>
    """
