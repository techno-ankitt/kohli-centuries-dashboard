"""Kohli Centuries Explorer: FastAPI backend on top of kohli.db."""
import sqlite3
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, Query
from fastapi.responses import FileResponse

BASE = Path(__file__).resolve().parent
DB = BASE / "kohli.db"

app = FastAPI(title="Kohli Centuries Explorer")

WIN_PCT = "ROUND(AVG(CASE WHEN result = 'Won' THEN 1.0 ELSE 0 END) * 100, 1)"


def run_query(sql: str, params: list | tuple = ()) -> list[dict]:
    """Run a SELECT and return rows as a list of dicts."""
    # Read-only connection: Vercel's filesystem is read-only, and we only SELECT.
    with sqlite3.connect(DB.as_uri() + "?mode=ro", uri=True) as con:
        con.row_factory = sqlite3.Row
        return [dict(row) for row in con.execute(sql, params).fetchall()]


def filters(
    source: str = "intl",
    fmt: Optional[str] = Query(None, alias="format"),
    opponent: Optional[str] = None,
    ground: Optional[str] = None,
    result: Optional[str] = None,
    innings: Optional[int] = None,
    year: Optional[int] = None,
) -> tuple[str, list, str]:
    """Turn the optional query-string filters into (WHERE clause, params, table).

    source=ipl switches every endpoint to the separate ipl_centuries table.
    """
    ipl = source == "ipl"
    table = "ipl_centuries" if ipl else "centuries"
    columns = {
        "format": None if ipl else fmt,   # IPL rows have no format column
        "against": opponent,
        "ground": ground,
        "result": result,
        "innings": innings,
        "year": year,
    }
    clauses, params = [], []
    for column, value in columns.items():
        if value is not None:
            clauses.append(f"{column} = ?")
            params.append(value)
    where = "WHERE " + " AND ".join(clauses) if clauses else ""
    return where, params, table


@app.get("/api/filters")
def filter_options(source: str = "intl"):
    """Values for the dropdowns on the dashboard."""
    if source == "ipl":
        def col(c):
            return [r[c] for r in run_query(f"SELECT DISTINCT {c} FROM ipl_centuries ORDER BY {c}")]
        return {"formats": [], "opponents": col("against"), "grounds": col("ground"),
                "results": col("result"), "innings": col("innings"), "years": col("year")}
    return {
        "formats": [r["format"] for r in run_query(
            "SELECT DISTINCT format FROM centuries "
            "ORDER BY CASE format WHEN 'Test' THEN 1 WHEN 'ODI' THEN 2 ELSE 3 END")],
        "opponents": [r["against"] for r in run_query("SELECT DISTINCT against FROM centuries ORDER BY against")],
        "grounds": [r["ground"] for r in run_query("SELECT DISTINCT ground FROM centuries ORDER BY ground")],
        "results": [r["result"] for r in run_query("SELECT DISTINCT result FROM centuries ORDER BY result")],
        "innings": [r["innings"] for r in run_query("SELECT DISTINCT innings FROM centuries ORDER BY innings")],
        "years": [r["year"] for r in run_query("SELECT DISTINCT year FROM centuries ORDER BY year")],
    }


@app.get("/api/stats")
def stats(f=Depends(filters)):
    """Stat cards: totals, 150+ scores, not-outs, win rate."""
    where, params, table = f
    extra = (", COALESCE(ROUND(SUM(runs) * 100.0 / SUM(balls), 1), 0) AS strike_rate"
             if table == "ipl_centuries" else "")
    sql = f"""
        SELECT COUNT(*) AS total,
               COALESCE(SUM(runs), 0) AS total_runs,
               COALESCE(SUM(CASE WHEN runs >= 150 THEN 1 ELSE 0 END), 0) AS scores_150_plus,
               COALESCE(SUM(not_out), 0) AS not_outs,
               COALESCE({WIN_PCT}, 0) AS win_pct
               {extra}
        FROM {table} {where}
    """
    return run_query(sql, params)[0]


@app.get("/api/centuries")
def centuries(f=Depends(filters)):
    """Full list for the timeline / table, latest first."""
    where, params, table = f
    return run_query(f"SELECT * FROM {table} {where} ORDER BY match_date DESC", params)


@app.get("/api/by-year")
def by_year(f=Depends(filters)):
    where, params, table = f
    return run_query(
        f"SELECT year, COUNT(*) AS total FROM {table} {where} GROUP BY year ORDER BY year", params
    )


@app.get("/api/by-opponent")
def by_opponent(f=Depends(filters)):
    where, params, table = f
    return run_query(
        f"""SELECT against, COUNT(*) AS total, ROUND(AVG(runs), 1) AS avg_runs
            FROM {table} {where} GROUP BY against ORDER BY total DESC, against""",
        params,
    )


@app.get("/api/by-position")
def by_position(f=Depends(filters)):
    where, params, table = f
    if table == "ipl_centuries":
        return []
    return run_query(
        f"""SELECT batting_position, COUNT(*) AS total
            FROM {table} {where} GROUP BY batting_position ORDER BY batting_position""",
        params,
    )


@app.get("/api/by-ground")
def by_ground(f=Depends(filters)):
    """Home / Away / Neutral with win percentage."""
    where, params, table = f
    return run_query(
        f"""SELECT ground, COUNT(*) AS total, {WIN_PCT} AS win_pct
            FROM {table} {where} GROUP BY ground ORDER BY total DESC""",
        params,
    )


@app.get("/")
def index():
    """Serve the dashboard page."""
    return FileResponse(BASE / "static" / "index.html")


@app.get("/api/by-format")
def by_format(f=Depends(filters)):
    """Test / ODI / T20I with win percentage."""
    where, params, table = f
    if table == "ipl_centuries":
        return []
    return run_query(
        f"""SELECT format, COUNT(*) AS total, {WIN_PCT} AS win_pct
            FROM {table} {where} GROUP BY format
            ORDER BY CASE format WHEN 'Test' THEN 1 WHEN 'ODI' THEN 2 ELSE 3 END""",
        params,
    )