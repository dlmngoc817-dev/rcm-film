# Demo catalog and provenance

`movies.csv` includes 50 manually curated records for an educational demo.
The short descriptions and keyword labels were authored for this project with AI
assistance; they are not copied from IMDb, TMDB, or MovieLens. Titles and release
years refer to real films; genre assignments are editorial, not authoritative.
The catalog has not been independently audited. It is deliberately small and is
not a benchmark dataset. No audience ratings, popularity counts, posters, or
viewing histories are represented or fabricated.

The included text may be used under the project license. Film titles and any
associated third-party rights remain with their owners. No film footage or
third-party artwork is distributed.

## Bring your own data

Upload a UTF-8 CSV through the sidebar, or replace `data/movies.csv` and restart.
Use these exact columns:

| Column | Format | Required |
|---|---|---|
| movie_id | Unique nonempty identifier, treated as text | Yes |
| title | Nonempty display title | Yes |
| year | Integer from 1888 through 2100 | Yes |
| genres | Comma-separated genre labels; quote the CSV field | Yes |
| keywords | Space-separated English terms; may be empty | Column required |
| overview | Nonempty English description | Yes |

At least two rows are required. Duplicate IDs, missing columns, blank required
values, and invalid years are rejected with a visible error. Blank optional
keywords are retained as empty text. Use consistent genre capitalization.
Only upload data that you have permission to use and redistribute. An external
dataset may have different licensing terms; do not assume the project license
covers it. No external dataset is downloaded automatically.
