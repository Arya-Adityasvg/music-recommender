import sys
import os
import pandas as pd
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.search import find_song, render_song_card


@pytest.fixture
def sample_df():
    """Small dataset for testing search logic."""
    return pd.DataFrame({
        'track_name': [
            'Blinding Lights',
            'Shape of You',
            'Bohemian Rhapsody',
            'Perfect',
            'Someone Like You',
            'Counting Stars',
            '<script>alert("xss")</script>',
            'Song {feat. Artist}',
            'Dragostea Din Tei',
        ],
        'artists': [
            'The Weeknd',
            'Ed Sheeran',
            'Queen',
            'Ed Sheeran',
            'Adele',
            'OneRepublic',
            'Evil Corp',
            'Unknown',
            'O-Zone',
        ],
        'track_genre': [
            'pop', 'pop', 'rock', 'pop', 'pop', 'pop', 'pop', 'pop', 'pop',
        ],
    })


# ── find_song: exact match ──

def test_exact_match(sample_df):
    idx, match_type = find_song(sample_df, 'Blinding Lights')
    assert idx == 0
    assert match_type == 'exact'


def test_exact_match_case_insensitive(sample_df):
    idx, match_type = find_song(sample_df, 'blinding lights')
    assert idx == 0
    assert match_type == 'exact'


def test_exact_match_with_spaces(sample_df):
    idx, match_type = find_song(sample_df, '  Blinding Lights  ')
    assert idx == 0
    assert match_type == 'exact'


# ── find_song: partial match ──

def test_partial_match_prefix(sample_df):
    idx, match_type = find_song(sample_df, 'blinding')
    assert idx == 0
    assert match_type == 'partial'


def test_partial_match_partial_phrase(sample_df):
    idx, match_type = find_song(sample_df, 'blinding light')
    assert idx == 0
    assert match_type == 'partial'


def test_partial_match_shared_prefix(sample_df):
    idx, match_type = find_song(sample_df, 'perfect')
    assert idx == 3
    assert match_type == 'exact'  # "Perfect" is in the dataset


def test_partial_match_middle_of_name(sample_df):
    idx, match_type = find_song(sample_df, 'bohemian')
    assert idx == 2
    assert match_type == 'partial'


# ── find_song: fuzzy match ──

def test_fuzzy_match_typo(sample_df):
    idx, match_type = find_song(sample_df, 'Bindng Lights')
    assert idx == 0
    assert match_type == 'fuzzy'


def test_fuzzy_match_misspelling(sample_df):
    idx, match_type = find_song(sample_df, 'Bohemian Rapsody')
    assert idx == 2
    assert match_type == 'fuzzy'


# ── find_song: no match ──

def test_no_match(sample_df):
    idx, match_type = find_song(sample_df, 'Nonexistent Song XYZ')
    assert idx is None
    assert match_type is None


def test_empty_query(sample_df):
    idx, match_type = find_song(sample_df, '')
    assert idx is None
    assert match_type is None


def test_whitespace_only_query(sample_df):
    idx, match_type = find_song(sample_df, '   ')
    assert idx is None
    assert match_type is None


# ── find_song: edge cases ──

def test_html_in_track_name_finds_it(sample_df):
    idx, match_type = find_song(sample_df, '<script>alert("xss")</script>')
    assert idx == 6
    assert match_type == 'exact'


def test_curly_brace_in_track_name(sample_df):
    idx, match_type = find_song(sample_df, 'Song {feat. Artist}')
    assert idx == 7
    assert match_type == 'exact'


def test_unicode_track_name(sample_df):
    idx, match_type = find_song(sample_df, 'Dragostea Din Tei')
    assert idx == 8
    assert match_type == 'exact'


# ── render_song_card: XSS prevention ──

def test_render_card_normal(sample_df):
    row = sample_df.iloc[0]
    html = render_song_card(row)
    assert 'Blinding Lights' in html
    assert 'The Weeknd' in html
    assert 'pop' in html
    assert '<div class="song-card">' in html


def test_render_card_xss_escaped(sample_df):
    row = sample_df.iloc[6]  # <script>alert("xss")</script>
    html = render_song_card(row)
    assert '<script>' not in html
    assert '&lt;script&gt;' in html
    assert 'Evil Corp' in html


def test_render_card_curly_braces(sample_df):
    row = sample_df.iloc[7]  # Song {feat. Artist}
    html = render_song_card(row)
    assert 'Song {feat. Artist}' in html
    assert '<div class="song-card">' in html


def test_render_card_html_entities(sample_df):
    """Ampersands and quotes should be escaped."""
    df_special = pd.DataFrame({
        'track_name': ['Tom & Jerry "Theme"'],
        'artists': ["Bob's Band"],
        'track_genre': ['soundtrack'],
    })
    html = render_song_card(df_special.iloc[0])
    assert 'Tom &amp; Jerry' in html
    assert '&quot;Theme&quot;' in html
    assert "Bob&#x27;s Band" in html
