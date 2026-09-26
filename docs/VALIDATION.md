# Delivery validation

- Environment: Linux, Python 3.12.
- Command: `python -m pytest -q` from the project root.
- Result: **17 passed**.
- Streamlit server launched successfully; `/_stcore/health` returned `ok`.
- Streamlit AppTest verified selecting favorites, generating recommendations,
  hiding stale results after changing inputs, empty-input feedback, and unmatched queries.
- The core suite verified ranked unique candidates, seed exclusions, valid score
  range, genre/year filters, grounded explanation terms, malformed catalogs,
  invalid inputs, and a space-survival query.

Windows launcher execution and GitHub Actions have not been performed in this
Linux delivery environment. The included CI workflow will run on push after the
project is uploaded to GitHub. These results verify software behavior, not
accuracy against real viewer preferences. No pixel-level browser review was run.
