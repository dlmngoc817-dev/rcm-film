# RCM Film 🎬

**Find your next story.** An explainable, content-based movie recommender with
an English interface, a local demo catalog, and no API-key requirement.

Built as a personal AI/ML portfolio project using Python, scikit-learn, and
Streamlit. Code and demo descriptions were created with AI assistance; review
and understand them before presenting the project as your work.

## Features

- Select up to five favorite movies, enter an English description, or combine both.
- Rank unseen titles using TF-IDF and cosine similarity.
- Filter by release year and genre; request 3–20 results.
- Inspect the shared text features behind each match.
- Search all 50 demo films and export recommendations as CSV.
- Upload your own compatible CSV without changing code.
- Run locally without API keys; internet is needed for initial package installation.

## Quick start on Windows

1. Install **Python 3.11 or 3.12** from https://www.python.org/downloads/.
   Enable **Add Python to PATH** during setup. Python 3.10 is not supported by
   the pinned package set.
2. Extract the ZIP completely. Open the `rcm-film` folder.
3. Double-click **`start.bat`**. First launch creates `.venv` and installs packages.
4. Your browser should open the app. If it does not, open http://localhost:8501.
5. Keep the terminal open while using the app. Press **Ctrl+C** to stop.

Subsequent starts reuse the local environment. If you change requirements,
run `.venv\Scripts\python -m pip install -r requirements.txt` manually.
The launcher has not been executed on a Windows machine in this delivery;
a Windows/Python test matrix is included in GitHub Actions.

## Manual installation

From the project directory on Windows:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m streamlit run app.py
```

On macOS/Linux, install Python 3.11/3.12, then run:

```bash
bash start.sh
```

The application binds to your local machine. It is not a publicly hosted website.

## Try the demo

1. Select **Interstellar (2014)** and click **Find my next film**.
2. Examine the results and their **Shared signals**.
3. Add **The Martian (2015)** to update your preference profile.
4. Alternatively, clear the favorites and enter `robots artificial intelligence`.
5. Try the Animation genre filter, then download a CSV of your results.

Results are calculated from features, not a hard-coded list. Similarity is shown
as a decimal, not as a predicted satisfaction percentage. Fewer than the requested
number are returned when too few candidates have positive overlap.

## How the recommendation engine works

1. Validate the CSV and preserve stable movie IDs.
2. Combine genres, keywords, and overview; repeat genres and keywords twice to
   give this short metadata more influence on the document representation.
3. Fit `TfidfVectorizer` with English stop words, unigrams and bigrams, and
   sublinear term frequency on the catalog.
4. Average the TF-IDF vectors of selected films. A recognized optional text query
   contributes one additional vector with equal weight to one selected film.
5. Compute cosine similarity between the profile and every candidate.
6. Exclude selected films, apply filters, remove zero-overlap candidates, and rank.
7. Explain each result with the four highest positive term-product contributions.

For vectors p and m, cosine similarity is `(p · m) / (||p|| * ||m||)`.
Repeating metadata changes TF-IDF weights; it does not imply an exact 2:1 final
feature weighting. Ties are resolved deterministically by title and movie ID.
Unknown query words are ignored; a query with no known terms produces no matches
unless valid favorite films were also supplied.

This is a classic content-based recommender. It fits a vocabulary and IDF weights;
it does not train a supervised rating predictor or a neural network. No paid LLM
or external inference service is involved.

## Project layout

| Path | Purpose |
|---|---|
| `app.py` | Streamlit interface and input/result state |
| `src/recommender.py` | CSV validation, TF-IDF features, ranking, explanations |
| `data/movies.csv` | 50-film demo catalog |
| `data/README.md` | Provenance, limitations, and custom CSV schema |
| `tests/` | Ranking, validation, and application-flow tests |
| `.github/workflows/tests.yml` | Linux/Windows CI on Python 3.11 and 3.12 |
| `.streamlit/config.toml` | Theme and local server configuration |
| `start.bat` / `start.sh` | Local launchers |
| `docs/PROJECT_NOTES.md` | Architecture, evaluation plan, presentation notes |

## Tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

These tests check software behavior, not recommendation accuracy. There are no
real user relevance labels in this project, so no Precision@K, Recall@K, or
accuracy percentage is claimed.

## Put the code on GitHub

Create a new **empty** repository named `rcm-film` in your own GitHub account.
Do not initialize that remote with a README or license. Open a terminal in the
extracted `rcm-film` folder and run:

```bash
git init
git add .
git commit -m "Initial release: RCM Film movie recommender"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/rcm-film.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username. If Git requests identity,
configure your name and email before committing. Authentication is handled by
Git/GitHub; do not put passwords or tokens into the code. `.gitignore` excludes
the virtual environment, caches, and local secrets. Upload the extracted project
files, not just the ZIP. GitHub stores your code; this step does not host the app.

Suggested repository description:
> Explainable movie recommendations with TF-IDF, cosine similarity, and Streamlit.

## Limitations and next steps

The included catalog is small and manually curated. Matching depends on shared
words; synonyms, nuanced preferences, and negative requests such as “no horror”
are not reliably understood. Use genre filters for structured preferences.
There are no accounts, persistent user histories, collaborative filtering,
streaming links, or automatic feedback learning. The app is intended for a trusted
local environment, not an unreviewed public upload service.

Next steps: use a larger appropriately licensed dataset; collect consented user
relevance judgments; compare against random and popularity baselines; add semantic
embeddings or collaborative filtering and measure whether they improve ranking.

## Troubleshooting

- **Python not found:** reinstall Python with PATH enabled, then reopen the terminal.
- **Install failed:** check your internet connection and Python version; rerun.
- **Port 8501 busy:** stop the other instance or run with `--server.port 8502`.
- **No recommendations:** broaden the year range, remove genre filters, or try
  vocabulary present in the catalog.
- **CSV error:** follow the schema in `data/README.md`; save as UTF-8 CSV.

## References

- [TF-IDF vectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
- [Cosine similarity](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html)
- [Streamlit AppTest](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest)

## License

Project code and project-authored descriptions are distributed under the MIT
license. See `LICENSE` and `data/README.md` for scope.
