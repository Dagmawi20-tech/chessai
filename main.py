# main.py
import re
import copy
from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.text import Text
from board import Board
from engine import best_move
from openings import OpeningBook
import time
from saves import save_game, load_game
from scores import record_result, display_scores
from pgn import export_pgn

console = Console()

COLS = 'abcdefgh'

def parse_move(text):
    text = text.strip().lower().replace(' ', '')
    m = re.match(r'^([a-h][1-8])([a-h][1-8])$', text)
    if not m:
        return None
    def to_coords(s):
        col = COLS.index(s[0])
        row = 8 - int(s[1])
        return row, col
    return to_coords(m.group(1)), to_coords(m.group(2))

def draw_board(board, legal, selected):
    table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
    for _ in range(9):
        table.add_column(justify="center", width=3)

    for row in range(8):
        cells = [Text(str(8 - row), style="dim")]
        for col in range(8):
            piece     = board.grid[row][col]
            is_light  = (row + col) % 2 == 0
            is_sel    = selected and selected == (row, col)
            is_target = selected and (selected[0], selected[1], row, col) in legal

            if is_sel:
                bg = "on yellow"
            elif is_target:
                bg = "on green"
            elif is_light:
                bg = "on grey82"
            else:
                bg = "on grey42"

            symbol = str(piece) if piece else " "
            if piece:
                fg = "white" if piece.color == 'white' else "black"
                cells.append(Text(f" {symbol} ", style=f"{fg} {bg}"))
            else:
                cells.append(Text("   ", style=bg))
        table.add_row(*cells)

    labels = [Text(" ")] + [Text(c, style="dim") for c in COLS]
    table.add_row(*labels)
    console.print(table)

def format_move(fr, fc, tr, tc):
    return f"{COLS[fc]}{8-fr}{COLS[tc]}{8-tr}"

def draw_captured(captured_white, captured_black):
    if captured_white:
        pieces = " ".join(str(p) for p in captured_white)
        console.print(f"  [bold white]You captured:[/bold white] {pieces}")
    if captured_black:
        pieces = " ".join(str(p) for p in captured_black)
        console.print(f"  [bold magenta]Computer captured:[/bold magenta] {pieces}")
    if captured_white or captured_black:
        console.print()

def draw_history(move_log):
    if not move_log:
        return
    table = Table(
        title="Move History",
        box=box.SIMPLE,
        show_header=True,
        header_style="bold red",
        title_style="bold red"
    )
    table.add_column("#",     style="dim",     width=4)
    table.add_column("White", style="white",   width=8)
    table.add_column("Black", style="magenta", width=8)

    pairs = []
    for i in range(0, len(move_log), 2):
        white = move_log[i]
        black = move_log[i + 1] if i + 1 < len(move_log) else ""
        pairs.append((str(i // 2 + 1), white, black))

    for num, white, black in pairs[-8:]:
        table.add_row(num, white, black)

    console.print(table)

def pick_difficulty():
    console.print("\n  [bold red]Select Difficulty:[/bold red]")
    console.print("    [white]1.[/white] Easy   (AI thinks 1 move ahead)")
    console.print("    [white]2.[/white] Medium (AI thinks 2 moves ahead)")
    console.print("    [white]3.[/white] Hard   (AI thinks 3 moves ahead)\n")
    while True:
        choice = console.input("  [bold red]Choose 1, 2, or 3:[/bold red] ").strip()
        if choice == '1':
            return 1, "Easy"
        elif choice == '2':
            return 2, "Medium"
        elif choice == '3':
            return 3, "Hard"
        else:
            console.print("  [red]Please type 1, 2, or 3.[/red]")

def format_time(seconds):
    mins = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{mins:02d}:{secs:02d}"

def play():
    board    = Board()
    selected = None
    legal    = []
    history  = []
    depth, difficulty = pick_difficulty()
    book       = OpeningBook()
    move_count = 0
    clock      = {'white': 300.0, 'black': 300.0}
    last_time  = time.time()
    hints_left = 3

    console.print(Panel.fit(
        Text("♔  ChessAI  ♚", style="bold red", justify="center"),
        border_style="red"
    ))
    console.print(Panel.fit(
        Text.assemble(
            ("  Welcome to ChessAI\n", "bold white"),
            ("  You play as White  ♙  vs  Computer Black  ♟\n", "dim"),
            ("  Built from scratch in Python\n", "dim"),
            ("  Difficulty levels: Easy / Medium / Hard\n", "dim"),
        ),
        border_style="red"
    ))
    console.print("[dim]  Moves: [bold]e2 e4[/bold]  Castle: [bold]O-O[/bold] or [bold]O-O-O[/bold]  Undo: [bold]undo[/bold]  Save: [bold]save[/bold]  Load: [bold]load[/bold]  Hint: [bold]hint[/bold]  Export: [bold]export[/bold]  Quit: [bold]quit[/bold][/dim]\n")
    display_scores(console)

    move_log       = []
    captured_white = []
    captured_black = []

    while True:
        now       = time.time()
        elapsed   = now - last_time
        last_time = now
        clock[board.turn] -= elapsed

        # Timeout checks
        if clock['white'] <= 0:
            draw_board(board, legal, selected)
            console.print("\n  [bold red]⏰ Time's up! Black wins![/bold red]\n")
            record_result('loss')
            display_scores(console)
            filename = export_pgn(move_log, '0-1', difficulty)
            console.print(f"  [dim]Game saved to [bold]{filename}[/bold][/dim]\n")
            break
        if clock['black'] <= 0:
            draw_board(board, legal, selected)
            console.print("\n  [bold red]⏰ Time's up! White wins![/bold red]\n")
            record_result('win')
            display_scores(console)
            filename = export_pgn(move_log, '1-0', difficulty)
            console.print(f"  [dim]Game saved to [bold]{filename}[/bold][/dim]\n")
            break

        draw_board(board, legal, selected)
        draw_captured(captured_white, captured_black)
        draw_history(move_log)

        # Clocks
        w_color = "red" if clock['white'] < 30 else "white"
        b_color = "red" if clock['black'] < 30 else "magenta"
        console.print(
            f"  [bold {w_color}]⏱  You: {format_time(clock['white'])}[/bold {w_color}]"
            f"   [bold {b_color}]Computer: {format_time(clock['black'])}[/bold {b_color}]"
        )

        # Game over checks
        if board.status == 'checkmate':
            winner = 'Black' if board.turn == 'white' else 'White'
            console.print(f"\n  [bold red]Checkmate! {winner} wins! 🏆[/bold red]\n")
            pgn_result = '0-1' if winner == 'Black' else '1-0'
            result     = 'loss' if winner == 'Black' else 'win'
            record_result(result)
            display_scores(console)
            filename = export_pgn(move_log, pgn_result, difficulty)
            console.print(f"  [dim]Game saved to [bold]{filename}[/bold][/dim]\n")
            break
        if board.status == 'stalemate':
            console.print("\n  [bold yellow]Stalemate! It's a draw. 🤝[/bold yellow]\n")
            record_result('draw')
            display_scores(console)
            filename = export_pgn(move_log, '1/2-1/2', difficulty)
            console.print(f"  [dim]Game saved to [bold]{filename}[/bold][/dim]\n")
            break

        if board.is_in_check(board.turn):
            console.print(f"  [bold red]⚠️  {board.turn.title()} is in check![/bold red]")

        console.print(f"  [red]Turn:[/red] [bold]{board.turn.title()}[/bold]")
        user = console.input("  [bold red]Your move:[/bold red] ").strip().lower()

        if user in ('quit', 'exit', 'q'):
            console.print("\n  [red]Thanks for playing ChessAI! 👋[/red]\n")
            break

        if user == 'save':
            save_game(board, move_log, clock, captured_white, captured_black)
            console.print("  [green]Game saved! ✅[/green]\n")
            continue

        if user == 'load':
            result = load_game(board)
            if result:
                move_log, clock, captured_white, captured_black = result
                console.print("  [green]Game loaded! ✅[/green]\n")
            else:
                console.print("  [red]No saved game found.[/red]\n")
            continue

        if user == 'export':
            filename = export_pgn(move_log, '*', difficulty)
            console.print(f"  [green]Game exported to [bold]{filename}[/bold] ✅[/green]\n")
            continue

        if user == 'hint':
            if hints_left == 0:
                console.print("  [red]No hints left! You've used all 3. 🧠[/red]\n")
            else:
                console.print("  [dim]Thinking of a hint...[/dim]")
                hint = best_move(board, depth=depth, color='white')
                if hint:
                    fr_h, fc_h, tr_h, tc_h = hint
                    hints_left -= 1
                    console.print(
                        f"  [yellow]💡 Hint: try [bold]{format_move(fr_h, fc_h, tr_h, tc_h)}[/bold]"
                        f"  [dim]({hints_left} hint{'s' if hints_left != 1 else ''} remaining)[/dim][/yellow]\n"
                    )
                else:
                    console.print("  [red]No hint available.[/red]\n")
            continue

        # Castling
        if user in ('o-o', '0-0'):
            if board.can_castle_kingside('white'):
                history.append(copy.deepcopy(board))
                board.castle_kingside('white')
                move_log.append("O-O")
                console.print("  [green]You castled kingside! ♔[/green]")
                if board.status:
                    continue
                console.print("  [dim]Computer is thinking...[/dim]")
                ai = best_move(board, depth=depth)
                if ai:
                    history.append(copy.deepcopy(board))
                    board.move(*ai)
                    move_log.append(format_move(*ai))
                    console.print(f"  [magenta]Computer played {format_move(*ai)}[/magenta]\n")
            else:
                console.print("  [red]Can't castle kingside right now.[/red]\n")
            continue

        if user in ('o-o-o', '0-0-0'):
            if board.can_castle_queenside('white'):
                history.append(copy.deepcopy(board))
                board.castle_queenside('white')
                move_log.append("O-O-O")
                console.print("  [green]You castled queenside! ♔[/green]")
                if board.status:
                    continue
                console.print("  [dim]Computer is thinking...[/dim]")
                ai = best_move(board, depth=depth)
                if ai:
                    history.append(copy.deepcopy(board))
                    board.move(*ai)
                    move_log.append(format_move(*ai))
                    console.print(f"  [magenta]Computer played {format_move(*ai)}[/magenta]\n")
            else:
                console.print("  [red]Can't castle queenside right now.[/red]\n")
            continue

        if user == 'undo':
            if len(history) >= 2:
                board    = history[-2]
                history  = history[:-2]
                selected = None
                legal    = []
                console.print("  [yellow]Move undone.[/yellow]\n")
            else:
                console.print("  [red]Nothing to undo.[/red]\n")
            continue

        parsed = parse_move(user)
        if not parsed:
            console.print("  [red]Invalid format. Try: e2 e4[/red]\n")
            continue

        (fr, fc), (tr, tc) = parsed
        piece = board.get_piece(fr, fc)

        if not piece:
            console.print("  [red]No piece there.[/red]\n")
            continue
        if piece.color != 'white':
            console.print("  [red]That's not your piece.[/red]\n")
            continue

        legal = board.legal_moves('white')
        if (fr, fc, tr, tc) not in legal:
            console.print("  [red]Illegal move.[/red]\n")
            selected = (fr, fc)
            continue

        target = board.get_piece(tr, tc)
        if target:
            captured_white.append(target)

        history.append(copy.deepcopy(board))
        board.move(fr, fc, tr, tc)
        selected   = None
        legal      = []
        last_time  = time.time()
        move_count += 1
        move_log.append(format_move(fr, fc, tr, tc))
        console.print(f"  [green]You played {format_move(fr, fc, tr, tc)}[/green]")

        if board.status:
            continue

        # Opening book or AI
        book_move = book.get_move('black', move_count)
        ai        = None

        if book_move:
            coords      = book.parse_book_move(book_move)
            legal_black = board.legal_moves('black')
            if coords in [(m[0], m[1], m[2], m[3]) for m in legal_black]:
                ai = coords
                console.print("  [dim]Computer plays opening theory...[/dim]")

        if not ai:
            console.print("  [dim]Computer is thinking...[/dim]")
            ai = best_move(board, depth=depth)

        if ai:
            fr2, fc2, tr2, tc2 = ai
            target = board.get_piece(tr2, tc2)
            if target:
                captured_black.append(target)
            history.append(copy.deepcopy(board))
            board.move(*ai)
            move_count += 1
            move_log.append(format_move(*ai))
            console.print(f"  [magenta]Computer played {format_move(*ai)}[/magenta]\n")

if __name__ == "__main__":
    play()