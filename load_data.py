"""Load the Kohli centuries CSV into a clean SQLite database (kohli.db)."""
import sqlite3
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
CSV = BASE / "data" / "Virat-Kohli-International-Cricket-Centuries.csv"
IPL_CSV = BASE / "data" / "Virat-Kohli-IPL-Centuries.csv"
DB = BASE / "kohli.db"

# The CSV has no format column. Wikipedia's list of Kohli's centuries gives the
# match start date of every Test and T20I century; every other century is an ODI.
# (Two Test centuries share 2014-12-09: both innings of the Adelaide Test.)
TEST_DATES = {
    "2012-01-24", "2012-08-31", "2012-12-13", "2013-02-22", "2013-12-18",
    "2014-02-14", "2014-12-09", "2014-12-26", "2015-01-06", "2015-08-12",
    "2016-07-21", "2016-10-08", "2016-11-17", "2016-12-08", "2017-02-09",
    "2017-07-26", "2017-11-16", "2017-11-24", "2017-12-02", "2018-01-13",
    "2018-08-01", "2018-08-18", "2018-10-04", "2018-12-14", "2019-10-10",
    "2019-11-22", "2023-03-09", "2023-07-20", "2024-11-22",
}
T20I_DATES = {"2022-09-08"}

df = pd.read_csv(CSV)

# "102*" -> runs = 102, not_out = 1
df["not_out"] = df["Runs"].str.contains("*", regex=False).astype(int)
df["runs"] = df["Runs"].str.replace("*", "", regex=False).astype(int)

# "24-Dec-09" -> "2009-12-24" (ISO dates sort and compare correctly in SQL)
dates = pd.to_datetime(df["Date"], format="%d-%b-%y")
df["match_date"] = dates.dt.strftime("%Y-%m-%d")
df["year"] = dates.dt.year

# Test / ODI / T20I, matched on the match start date
df["format"] = df["match_date"].map(
    lambda d: "Test" if d in TEST_DATES else ("T20I" if d in T20I_DATES else "ODI")
)

# "Eden Gardens, Kolkata" -> stadium + city
parts = df["Venue"].str.rsplit(",", n=1, expand=True)
df["stadium"] = parts[0].str.strip()
df["city"] = parts[1].str.strip() if parts.shape[1] > 1 else None

clean = df.rename(
    columns={
        "No.": "century_no",
        "Against": "against",
        "Position": "batting_position",
        "Innings": "innings",
        "Ground": "ground",
        "Result": "result",
    }
)[
    [
        "century_no", "runs", "not_out", "against", "batting_position",
        "innings", "format", "stadium", "city", "ground", "match_date",
        "year", "result",
    ]
]

with sqlite3.connect(DB) as con:
    clean.to_sql("centuries", con, if_exists="replace", index=False)

print(f"Loaded {len(clean)} rows into {DB.name}")
print(clean.head(3).to_string(index=False))

# Sanity check against Wikipedia: 30 Test, 55 ODI, 1 T20I (86 in total)
counts = clean["format"].value_counts().to_dict()
print("\nCenturies by format:", counts)
if counts.get("Test") != 30 or counts.get("T20I") != 1:
    print("Check this: expected 30 Test and 1 T20I. Some dates may not have matched.")


# ---------------------------------------------------------------------------
# IPL centuries: separate table, so the 86 international centuries (and every
# win rate / stat built on them) stay exactly as they were.
# ---------------------------------------------------------------------------
ipl = pd.read_csv(IPL_CSV)
ipl["not_out"] = ipl["Runs"].str.contains("*", regex=False).astype(int)
ipl["runs"] = ipl["Runs"].str.replace("*", "", regex=False).astype(int)
ipl_dates = pd.to_datetime(ipl["Date"], format="%d-%b-%y")
ipl["match_date"] = ipl_dates.dt.strftime("%Y-%m-%d")
ipl["year"] = ipl_dates.dt.year
ipl_parts = ipl["Venue"].str.rsplit(",", n=1, expand=True)
ipl["stadium"] = ipl_parts[0].str.strip()
ipl["city"] = ipl_parts[1].str.strip()

ipl_clean = ipl.rename(
    columns={"No.": "century_no", "Balls": "balls", "Against": "against",
             "Innings": "innings", "Ground": "ground", "Result": "result"}
)[["century_no", "runs", "not_out", "balls", "against", "innings",
   "stadium", "city", "ground", "match_date", "year", "result"]]

with sqlite3.connect(DB) as con:
    ipl_clean.to_sql("ipl_centuries", con, if_exists="replace", index=False)

print(f"\nLoaded {len(ipl_clean)} IPL rows into table ipl_centuries")