from io import StringIO
import pytest
from src.recommender import load_movies, MovieRecommender

@pytest.fixture(scope='module')
def engine():
    return MovieRecommender(load_movies())

def test_ranked_unique_and_excludes_seeds(engine):
    results = engine.recommend(['1', '2'], top_k=10)
    ids = [r['movie_id'] for r in results]
    assert len(results) == 10 and len(ids) == len(set(ids))
    assert not {'1', '2'} & set(ids)
    scores = [r['similarity'] for r in results]
    assert scores == sorted(scores, reverse=True)
    assert all(0 < s <= 1 + 1e-9 for s in scores)

def test_space_query_returns_relevant_movie(engine):
    titles = [r['title'] for r in engine.recommend(query='space survival astronaut Mars', top_k=3)]
    assert 'The Martian' in titles

def test_filters(engine):
    results = engine.recommend(['1'], genres=['Animation'], year_range=(2000, 2020))
    assert results
    assert all('Animation' in r['genres'].split(',') and 2000 <= r['year'] <= 2020 for r in results)

def test_no_candidate(engine):
    assert engine.recommend(['1'], genres=['NotAGenre']) == []

def test_unknown_query(engine):
    assert engine.recommend(query='qzxwvvv') == []

def test_explanations_are_shared_features(engine):
    results = engine.recommend(['1'])
    seed_features = set(engine.features[engine.matrix[0].indices])
    for result in results:
        assert result['matching_terms']
        target = engine.matrix[engine.positions[result['movie_id']]]
        assert set(result['matching_terms']) <= seed_features & set(engine.features[target.indices])

def test_duplicate_seeds_do_not_change_ranking(engine):
    assert engine.recommend(['1']) == engine.recommend(['1', '1'])

@pytest.mark.parametrize('kwargs', [{}, {'selected_ids':['missing']}, {'query':'space','top_k':0}, {'query':'space','year_range':(2020,2000)}])
def test_invalid_inputs(engine, kwargs):
    with pytest.raises(ValueError): engine.recommend(**kwargs)

@pytest.mark.parametrize('change', ['duplicate', 'empty', 'year', 'missing'])
def test_invalid_catalog(change):
    df = load_movies().head(2).copy()
    if change == 'duplicate': df.loc[1,'movie_id'] = df.loc[0,'movie_id']
    if change == 'empty': df.loc[0,'title'] = ' '
    if change == 'year': df['year'] = 'unknown'
    if change == 'missing': df = df.drop(columns='overview')
    with pytest.raises(ValueError): load_movies(StringIO(df.to_csv(index=False)))
