# Project notes

## Problem and scope

Help a user choose a movie from a fixed catalog using examples of what they enjoy.
The deliverable is a local English-language application and a GitHub-ready source
project. It does not stream movies or connect to a commercial recommendation API.

## Architecture

The Streamlit UI reads a bundled or user-uploaded CSV. `load_movies` validates the
schema. `MovieRecommender` creates a sparse TF-IDF matrix cached by catalog bytes.
Each request creates a preference vector and computes an O(N) score vector rather
than storing a dense all-pairs similarity matrix. Only the filtered top results
and matching terms are displayed. Uploaded catalogs stay in server memory; no
application code sends them to a third-party service. Streamlit usage telemetry
is disabled in the bundled configuration.

The profile and each candidate explanation use dense vectors, so this version
is designed for small catalogs. A production version should limit upload size,
retain sparse profile operations, and consider an approximate-neighbor index.

## Evaluation plan

Current tests establish ranking invariants, exclusion of seed films, filter
behavior, input errors, explanation grounding, and the interactive discovery
flow. A space-survival query is a semantic smoke test, not a benchmark.

For a real evaluation, collect consented ratings or relevance judgments for a
separate candidate set. Define relevant, e.g. rating >= 4/5, before measuring.
Split interaction histories by time. Construct profiles from earlier interactions
only; never use a held-out liked film as a seed. Keep test candidates eligible
at the evaluation date and document whether previously seen films are excluded.
Compare the recommender against random and a training-only popularity baseline.
Report Precision@K, Recall@K, NDCG@K, catalog coverage, and the number of evaluated
users. Use validation data for tuning; keep the test data untouched until the
final comparison. Account for incomplete relevance judgments before interpreting
unobserved films as disliked. No such measured results are included here.

## Suggested presentation (3–5 minutes)

1. Explain the choice-overload problem and the demo scope.
2. Show the dataset columns and explain why no user history is needed.
3. Demonstrate Interstellar-based recommendations and genre filtering.
4. Explain TF-IDF, averaging, cosine similarity, and shared feature terms.
5. Show the test suite and discuss the absence of real preference evaluation.
6. Describe larger licensed data and embeddings as future experiments.

## Questions you should be able to answer

- Why can this recommend to a new user? They supply favorites or a text query.
- Why is it AI/ML related? It uses learned corpus text features for retrieval and ranking.
- Why not deep learning? This baseline is small, explainable, and works without a GPU.
- Is a 0.6 score a 60% chance of liking a film? No; it measures vector alignment.
- Can two people receive different results? Yes, when their input profiles differ.
- Does feedback train it? No; this version does not collect or learn from feedback.
- Why are some good films absent? The catalog is limited and lexical similarity is imperfect.
