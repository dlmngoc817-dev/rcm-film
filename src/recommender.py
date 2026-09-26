"""Content-based movie recommendations with transparent feature contributions."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

COLUMNS = ['movie_id', 'title', 'year', 'genres', 'keywords', 'overview']
DEFAULT_DATA = Path(__file__).resolve().parents[1] / 'data' / 'movies.csv'


def load_movies(source=DEFAULT_DATA):
    """Read and validate a catalog; reject ambiguous IDs and malformed metadata."""
    df = pd.read_csv(source, dtype=str, keep_default_na=False)
    missing = set(COLUMNS) - set(df.columns)
    if missing:
        raise ValueError('Missing columns: ' + ', '.join(sorted(missing)))
    df = df[COLUMNS].copy()
    for col in COLUMNS:
        df[col] = df[col].str.strip()
    for col in ['movie_id', 'title', 'genres', 'overview']:
        if df[col].eq('').any():
            raise ValueError(f'{col} must not be empty.')
    if len(df) < 2:
        raise ValueError('At least two movies are required.')
    if df.movie_id.duplicated().any():
        raise ValueError('movie_id values must be unique.')
    years = pd.to_numeric(df.year, errors='coerce')
    if years.isna().any() or (years % 1 != 0).any() or not years.between(1888, 2100).all():
        raise ValueError('year must be an integer between 1888 and 2100.')
    df['year'] = years.astype(int)
    return df.reset_index(drop=True)


class MovieRecommender:
    def __init__(self, movies):
        self.movies = movies.reset_index(drop=True).copy()
        # Repeat short metadata to give genres and curated keywords more influence.
        documents = (self.movies.genres.str.replace(',', ' ', regex=False) + ' ') * 2
        documents += (self.movies.keywords + ' ') * 2 + self.movies.overview
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), sublinear_tf=True)
        self.matrix = self.vectorizer.fit_transform(documents)
        self.features = self.vectorizer.get_feature_names_out()
        self.positions = {mid: i for i, mid in enumerate(self.movies.movie_id)}

    def recommend(self, selected_ids=(), query='', top_k=10, genres=(), year_range=None):
        """Rank candidates against the normalized mean seed/query profile.

        Similarity is not a probability. Zero-overlap candidates are omitted.
        When both are supplied, the query contributes one additional seed vector.
        """
        if not isinstance(top_k, int) or top_k < 1:
            raise ValueError('top_k must be a positive integer.')
        ids = list(dict.fromkeys(str(x) for x in selected_ids))
        unknown = set(ids) - set(self.positions)
        if unknown:
            raise ValueError('Unknown movie ID: ' + ', '.join(sorted(unknown)))
        if not ids and not query.strip():
            raise ValueError('Choose at least one movie or describe what you want to watch.')
        vectors = [self.matrix[self.positions[mid]].toarray()[0] for mid in ids]
        if query.strip():
            q = self.vectorizer.transform([query]).toarray()[0]
            if q.any():
                vectors.append(q)
        if not vectors:
            return []
        profile = np.mean(vectors, axis=0).reshape(1, -1)
        scores = cosine_similarity(profile, self.matrix).ravel()
        candidates = self.movies[~self.movies.movie_id.isin(ids)].copy()
        if genres:
            allowed = set(genres)
            candidates = candidates[candidates.genres.apply(lambda s: bool(allowed & {g.strip() for g in s.split(',')}))]
        if year_range:
            if year_range[0] > year_range[1]:
                raise ValueError('Minimum year must not exceed maximum year.')
            candidates = candidates[candidates.year.between(*year_range)]
        candidates['similarity'] = scores[candidates.index]
        candidates = candidates[candidates.similarity > 1e-12]
        candidates = candidates.sort_values(['similarity', 'title', 'movie_id'], ascending=[False, True, True]).head(top_k)
        results = []
        for idx, row in candidates.iterrows():
            contribution = self.matrix[idx].toarray()[0] * profile.ravel()
            terms = [str(self.features[j]) for j in np.argsort(-contribution) if contribution[j] > 0][:4]
            result = row.to_dict()
            result['matching_terms'] = terms
            results.append(result)
        return results
