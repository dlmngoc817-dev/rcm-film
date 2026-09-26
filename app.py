"""English-language Streamlit interface for RCM Film."""
from io import BytesIO
import pandas as pd
import streamlit as st
from src.recommender import load_movies, MovieRecommender, DEFAULT_DATA

st.set_page_config(page_title='RCM Film | Find your next story', page_icon='🎬', layout='wide')
st.markdown('''<style>
.block-container {max-width:1150px;padding-top:2.5rem;}
h1 {letter-spacing:-2px;font-size:3.8rem!important;}
[data-testid="stSidebar"] {border-right:1px solid #293047;}
[data-testid="stMetricValue"] {color:#bbacff;}
</style>''', unsafe_allow_html=True)

@st.cache_resource
def build_engine(raw):
    return MovieRecommender(load_movies(BytesIO(raw)))

with st.sidebar:
    st.title('🎬 RCM Film')
    st.caption('A good film starts with a good match.')
    st.divider()
    uploaded = st.file_uploader('Use your own catalog', type=['csv'], help='Required columns: movie_id, title, year, genres, keywords, overview.')
    st.caption('The included catalog contains 50 curated demo films. No account or API key needed.')

raw = uploaded.getvalue() if uploaded is not None else DEFAULT_DATA.read_bytes()
try:
    engine = build_engine(raw)
except (ValueError, pd.errors.ParserError, UnicodeError) as exc:
    st.error(f'Unable to load this catalog: {exc}')
    st.stop()
movies = engine.movies
with st.sidebar:
    genres = sorted({g.strip() for value in movies.genres for g in value.split(',') if g.strip()})
    chosen_genres = st.multiselect('Filter by genre', genres)
    low, high = int(movies.year.min()), int(movies.year.max())
    years = st.slider('Release years', low, high, (low, high)) if low < high else (low, high)
    count = st.slider('Number of recommendations', 3, 20, 10)
    st.divider()
    st.caption('Built with Python · scikit-learn · Streamlit')

st.caption('YOUR NEXT MOVIE NIGHT, SORTED')
st.title('Find your next story.')
st.write('Start with films you love. Discover something that feels like you.')
a,b,c = st.columns(3)
a.metric('Films to explore', len(movies))
b.metric('Genres', len(genres))
c.metric('API keys needed', '0')
st.divider()
recommend_tab, catalog_tab, about_tab = st.tabs(['Discover', 'Film catalog', 'How it works'])
with recommend_tab:
    labels = {row.movie_id: f'{row.title} ({row.year})' for row in movies.itertuples()}
    selected = st.multiselect('Pick up to 5 films you enjoy', list(labels), format_func=labels.get, max_selections=5, key='seeds')
    query = st.text_input('Or describe your movie mood in English', placeholder='e.g. space survival, friendship, robots, time travel', key='mood')
    st.caption('You can combine favorite films and a description. Genre filters match any selected genre.')
    # A result is tied to its input signature, so changing controls never displays stale matches.
    signature = (raw, tuple(selected), query, tuple(chosen_genres), years, count)
    if st.button('Find my next film', type='primary', key='recommend'):
        try:
            results = engine.recommend(selected, query, count, chosen_genres, years)
            st.session_state['result_bundle'] = (signature, results)
        except ValueError as exc:
            st.warning(str(exc))
    bundle = st.session_state.get('result_bundle')
    if bundle and bundle[0] == signature:
        results = bundle[1]
        st.subheader(f'{len(results)} films for your next movie night')
        if not results:
            st.info('No matching films found. Try broader keywords, different favorites, or fewer filters.')
        else:
            st.caption('Similarity compares film descriptions and metadata; it is not a probability that you will like a film.')
            columns = st.columns(2)
            for rank, film in enumerate(results, 1):
                with columns[(rank-1) % 2]:
                    with st.container(border=True):
                        st.caption(f"MATCH {rank:02d} · {film['year']} · SIMILARITY {film['similarity']:.3f}")
                        st.subheader(film['title'])
                        st.caption(film['genres'].replace(',', ' · '))
                        st.write(film['overview'])
                        st.markdown('**Shared signals:** ' + ', '.join(film['matching_terms']))
            exported = pd.DataFrame(results)
            exported['matching_terms'] = exported.matching_terms.str.join(', ')
            st.download_button('Download recommendations as CSV', exported.to_csv(index=False).encode('utf-8-sig'), 'rcm-film-recommendations.csv', 'text/csv')
    else:
        st.info('Choose a favorite such as Interstellar or Toy Story, then select Find my next film.')
with catalog_tab:
    search = st.text_input('Search the catalog', placeholder='Title, genre, or keyword', key='catalog_search')
    mask = movies[['title','genres','keywords']].agg(' '.join, axis=1).str.contains(search, case=False, regex=False)
    st.dataframe(movies.loc[mask, ['title','year','genres','overview']], hide_index=True, use_container_width=True)
    st.download_button('Download catalog / CSV template', raw, 'movies.csv', 'text/csv')
with about_tab:
    st.subheader('Recommendations you can explain')
    st.write('RCM Film converts genres, keywords, and short descriptions into TF-IDF vectors. It averages the vectors of your favorite films and optional description, then ranks unseen titles by cosine similarity.')
    st.write('Shared signals show terms contributing to a match. Release-year and genre filters narrow the results. Selected films and zero-overlap results are excluded.')
    st.info('This is a content-based learning project, not a streaming service or a deep-learning model. The demo metadata is manually curated and the short descriptions are project-authored. No audience ratings or behavioral data are included.')
    st.write('The system does not understand synonyms like a language model. Recommendation quality has not been measured against real user preferences. After dependencies are installed, the included demo works offline.')
