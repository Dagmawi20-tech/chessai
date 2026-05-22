# ♔ ChessAI

A fully featured terminal-based Chess game built from scratch in Python. Play against an AI opponent powered by the Minimax algorithm with Alpha-Beta pruning — the same logic used in real chess engines. Built as a Python learning project in one day.

---

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

---

## Prerequisites

What you need to install before running the game:

- Python 3.8 or higher
- pip3

Check if you have Python installed:

```bash
python3 --version
```

Install the required library:

```bash
pip3 install rich
```

---

## Installing

A step by step guide to get the game running on your machine.

**1. Clone the repository**

```bash
git clone https://github.com/Dagmawi20-tech/chessai.git
```

**2. Navigate into the project folder**

```bash
cd chessai
```

**3. Install dependencies**

```bash
pip3 install rich
```

**4. Run the game**

```bash
python3 main.py
```

You should see this:

```
♔  ChessAI  ♚
Welcome to ChessAI
You play as White ♙ vs Computer Black ♟
Built from scratch in Python
```

**5. Pick your difficulty**

```
Select Difficulty:
  1. Easy   (AI thinks 1 move ahead)
  2. Medium (AI thinks 2 moves ahead)
  3. Hard   (AI thinks 3 moves ahead)
```

**6. Make your first move**

```
Your move: e2 e4
```

The computer will respond and the game begins.

---

## Running the Tests

You can manually test the core features by running these scenarios after launch.

### Checkmate test (Scholar's Mate)

Test that the game detects checkmate correctly:

```
Your move: e2 e4
Your move: f1 c4
Your move: d1 h5
Your move: h5 f7
```

Expected output:

```
Checkmate! White wins! 🏆
```

### Conflict detection test

Test that illegal moves are rejected:

```
Your move: e2 e5
```

Expected output:

```
Illegal move.
```

### Castling test

Move your King-side pieces out first then test castling:

```
Your move: g1 f3
Your move: f1 c4
Your move: O-O
```

Expected output:

```
You castled kingside! ♔
```

### Hint test

```
Your move: hint
```

Expected output:

```
💡 Hint: try e2e4  (2 hints remaining)
```

### Save and load test

```
Your move: save
```

Quit the game, restart it, then:

```
Your move: load
```

Expected output:

```
Game loaded! ✅
```

### Export test

```
Your move: export
```

Expected output:

```
Game exported to game_20260521_143022.pgn ✅
```

Upload the `.pgn` file to [lichess.org/paste](https://lichess.org/paste) to replay your game move by move.

---

## Deployment

To make ChessAI launchable from anywhere on your Mac, add an alias to your shell config:

```bash
echo 'alias chessai="python3 ~/chessai/main.py"' >> ~/.zshrc
source ~/.zshrc
```

Now launch it from any terminal window by typing:

```bash
chessai
```

---

## Built With

* [Python](https://www.python.org/) - Core language
* [Rich](https://github.com/Textualize/rich) - Terminal UI and colored output
* [Minimax Algorithm](https://en.wikipedia.org/wiki/Minimax) - AI decision making
* [Alpha-Beta Pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning) - AI optimization

---

## Features

* Full chess rules — legal moves, check, checkmate, stalemate
* Castling — kingside and queenside
* En passant
* Pawn promotion
* AI opponent powered by Minimax with Alpha-Beta pruning
* Opening book — plays real famous openings (Italian, Sicilian, Ruy Lopez, etc.)
* 3 difficulty levels — Easy, Medium, Hard
* Move history panel
* Captured pieces display
* 5 minute chess clock
* 3 hints per game
* Save and load games
* Export games to PGN format

---

## Versioning

* **v1.0** — Core chess engine: board, pieces, legal moves, check/checkmate
* **v1.1** — Minimax AI with Alpha-Beta pruning
* **v1.2** — Rich terminal UI, move history, captured pieces
* **v1.3** — Castling, en passant, pawn promotion
* **v1.4** — Difficulty levels, opening book
* **v1.5** — Chess clock, hints, save/load, PGN export

---

## Authors

* **Dagmawi Mengistu** — Built this project from scratch in one day as a Python learning project

---

## Acknowledgments

* Built with guidance from Claude (Anthropic)
* Inspired by classic chess engines like Stockfish
* Thanks to the Rich open source community
* Opening lines sourced from classic chess theory
