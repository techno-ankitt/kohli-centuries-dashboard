# Virat Kohli Centuries Explorer

An interactive dashboard to explore every century scored by Virat Kohli, in international cricket and in the IPL (for RCB). Filter by opponent, venue type, result, innings or year and watch every chart, card and table update instantly.

Built with **FastAPI**, **SQLite** and a single-page **vanilla JavaScript** frontend, with no frontend build step.

## Features

- **International / IPL toggle** to switch between the two data sets.
- **Filters** for format (international only), opponent, venue type (Home / Away / Neutral), result, innings and year, plus a one-click "Clear filters".
- **Summary cards:** total centuries, total runs, highest score, 150+ scores (strike rate in IPL mode), not outs and team win rate.
- **Every century, in order:** a bar chart where bar height is runs scored and colour shows the result (won / lost / drawn or tied). Hover a bar for details.
- **Breakdowns:** centuries per year, per opponent, by batting position and by format (international), and win rate by venue type.
- **Best batting ranking** (international) and **Best of IPL** cards, which are static and independent of the filters.
- **All centuries table:** scrollable, with runs (a star means not out), opponent, venue, date, result and balls faced in IPL mode.
- Light and dark theme, following your system setting.

## Tech stack

| Layer    | Technology                               |
| -------- | ---------------------------------------- |
| Backend  | Python, FastAPI                          |
| Database | SQLite (`kohli.db`)                      |
| Frontend | HTML, CSS and vanilla JavaScript         |
| Data     | CSV files loaded into SQLite by a script |

## Project structure

```
.
├── data/              # Source CSV files (international and IPL centuries)
├── static/
│   └── index.html     # The whole dashboard (HTML, CSS and JS)
├── main.py            # FastAPI app and API endpoints
├── load_data.py       # Builds kohli.db from the CSV files
├── kohli.db           # SQLite database
├── queries.sql        # SQL practice queries
├── my_queries.sql     # My own solved SQL queries
└── requirements.txt   # Python dependencies
```

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. (Optional) Rebuild the database

`kohli.db` is already included. To rebuild it from the CSV files in `data/`:

```bash
python load_data.py
```

### 4. Run the app

```bash
uvicorn main:app --reload
```

Open <http://127.0.0.1:8000> in your browser.

## API

All endpoints accept the same filter query parameters (`format`, `opponent`, `ground`, `result`, `innings`, `year`). Add `source=ipl` to query the IPL data instead of the international data. The `format` filter is ignored for IPL.

| Endpoint              | Description                                                    |
| --------------------- | -------------------------------------------------------------- |
| `/`                   | Serves the dashboard                                           |
| `/api/filters`        | Values available for each filter dropdown                      |
| `/api/stats`          | Summary numbers (adds `strike_rate` for IPL)                   |
| `/api/centuries`      | The list of centuries matching the filters                     |
| `/api/by-year`        | Centuries per year                                             |
| `/api/by-opponent`    | Centuries per opponent                                         |
| `/api/by-position`    | Centuries by batting position (empty for IPL)                  |
| `/api/by-ground`      | Win rate by venue type                                         |
| `/api/by-format`      | Centuries and win rate by format (empty for IPL)               |

Example:

```
/api/centuries?opponent=Australia&result=Won
/api/stats?source=ipl&year=2016
```

## Updating the data

When Kohli scores a new century:

1. Add a row to the relevant CSV file in `data/`.
2. Run `python load_data.py` to rebuild `kohli.db`.
3. Restart the server and refresh the page.

## Notes

- A star next to runs means the batter was not out.
- In Tests, a drawn match counts as not won when calculating the win rate.
- The "Best batting ranking" and "Best of IPL" cards are hardcoded in `static/index.html`, so edit them there if the numbers change.

## Acknowledgements

Built as a learning project combining SQL, FastAPI and a vanilla JavaScript frontend.
