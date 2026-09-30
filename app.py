import joblib
import streamlit as st
import pickle
import time

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch – Movie Recommender",
    page_icon="🎬",
    layout="centered",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

/* ── Hide heading anchor links ── */
h1 a, h2 a, h3 a, h4 a, h5 a, h6 a { display: none !important; }

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
    color: #e0e0e0;
}

/* ── Remove bottom blank scroll space ── */
.main .block-container { padding-bottom: 0 !important; margin-bottom: 0 !important; }
footer[data-testid="stBottom"], footer { display: none !important; }
.stAppViewBlockContainer { padding-bottom: 0 !important; }

/* ── Hero Header ── */
.hero-header { text-align: center; padding: 2.5rem 1rem 1.5rem; }
.hero-header h1 {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #f7971e, #ffd200, #ff6a00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.25rem;
    letter-spacing: -1px;
}
.hero-header p { font-size: 1.05rem; color: #a0a0c0; font-weight: 300; }

/* ── Selectbox label ── */
.stSelectbox label {
    color: #c0b8d8 !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.03em;
}

/* ── Button ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #f7971e, #ffd200);
    color: #1a1a2e;
    font-weight: 700;
    font-size: 1rem;
    border: none;
    border-radius: 10px;
    padding: 0.75rem 2rem;
    cursor: pointer;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    letter-spacing: 0.04em;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(247,151,30,0.45);
}
.stButton > button:active { transform: translateY(0); }

/* ── Spinner ── */
.stSpinner > div { color: #ffd200 !important; }

/* ── Movie result cards ── */
.movie-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 0.9rem 1.4rem;
    margin: 0.55rem 0;
    transition: background 0.2s ease, transform 0.2s ease;
    animation: fadeSlideIn 0.4s ease both;
}
.movie-card:hover {
    background: rgba(247,151,30,0.12);
    transform: translateX(4px);
    border-color: rgba(247,151,30,0.4);
}
.movie-rank { font-size: 1.5rem; font-weight: 800; color: #ffd200; min-width: 2rem; text-align: center; }
.movie-title { font-size: 1.05rem; font-weight: 500; color: #e8e8f5; }

@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Results section ── */
.section-label {
    font-size: 0.8rem; font-weight: 600; letter-spacing: 0.12em;
    text-transform: uppercase; color: #ffd200; margin-bottom: 0.4rem;
}
.result-title { font-size: 1.15rem; font-weight: 600; color: #e0dff5; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

# ─── Load Data (cached) ─────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_data():
    with open('movies_data.pickle', 'rb') as m:
        movies = pickle.load(m)
    similarities = joblib.load('similarities_data.joblib')
    return movies, similarities

# ─── Recommendation Logic ────────────────────────────────────────────────────────
def get_recommendations(movie, movies, similarities):
    movie_index = movies[movies['title'] == movie].index[0]
    scores = similarities[movie_index]
    movies_sorted = sorted(enumerate(scores), reverse=True, key=lambda x: x[1])[1:6]
    return [movies.iloc[i[0]].title for i in movies_sorted]

# ─── Hero Header ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <h1>🎬 CineMatch</h1>
    <p>Discover your next favourite film — powered by AI similarity search</p>
</div>
""", unsafe_allow_html=True)

# ─── Load data ──────────────────────────────────────────────────────────────────
with st.spinner("⚙️ Loading movie database..."):
    movies, similarities = load_data()

# ─── Input ──────────────────────────────────────────────────────────────────────
selected_movie = st.selectbox(
    "🎥  Choose a movie you enjoyed",
    movies["title"].values,
    help="Start typing to search across thousands of movies"
)

recommend_clicked = st.button("**Find Similar Movies**")

# ─── Results ────────────────────────────────────────────────────────────────────
if recommend_clicked:
    with st.spinner("🔍  Analysing movie similarities and fetching recommendations..."):
        time.sleep(0.8)
        results = get_recommendations(selected_movie, movies, similarities)

    st.markdown(f"""
    <div class="section-label">Top 5 Picks</div>
    <div class="result-title">Because you liked <em style="color:#ffd200;">{selected_movie}</em></div>
    """, unsafe_allow_html=True)

    for i, title in enumerate(results, start=1):
        delay = i * 0.08
        st.markdown(f"""
        <div class="movie-card" style="animation-delay:{delay}s;">
            <span class="movie-rank">#{i}</span>
            <span class="movie-title">{title}</span>
        </div>
        """, unsafe_allow_html=True)
