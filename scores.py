# scores.py
import json
import os

SCORES_FILE = "scores.json"

def load_scores():
    if not os.path.exists(SCORES_FILE):
        return {"wins": 0, "losses": 0, "draws": 0, "games": 0}
    with open(SCORES_FILE) as f:
        return json.load(f)

def save_scores(scores):
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f, indent=2)

def record_result(result):
    scores = load_scores()
    scores["games"] += 1
    if result == "win":
        scores["wins"] += 1
    elif result == "loss":
        scores["losses"] += 1
    elif result == "draw":
        scores["draws"] += 1
    save_scores(scores)
    return scores

def display_scores(console):
    scores = load_scores()
    from rich.table import Table
    from rich import box
    table = Table(
        title="Your Record",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold red",
        title_style="bold red"
    )
    table.add_column("Games",    style="white",  justify="center", width=8)
    table.add_column("Wins",     style="green",  justify="center", width=8)
    table.add_column("Losses",   style="red",    justify="center", width=8)
    table.add_column("Draws",    style="yellow", justify="center", width=8)
    table.add_column("Win Rate", style="cyan",   justify="center", width=10)

    games    = scores["games"]
    win_rate = f"{(scores['wins'] / games * 100):.1f}%" if games > 0 else "N/A"
    table.add_row(
        str(games),
        str(scores["wins"]),
        str(scores["losses"]),
        str(scores["draws"]),
        win_rate
    )
    console.print()
    console.print(table)
    console.print()