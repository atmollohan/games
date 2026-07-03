import random

WIN_LINES = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]


def _check_win(board: list[str | None], player: str) -> bool:
    return any(all(board[i] == player for i in line) for line in WIN_LINES)


def _empty_cells(board: list[str | None]) -> list[int]:
    return [i for i, v in enumerate(board) if v is None]


def _find_best_move(board: list[str | None]) -> int | None:
    # Win if possible
    for line in WIN_LINES:
        vals = [board[i] for i in line]
        if vals.count("O") == 2 and any(v is None for v in vals):
            candidates = [i for i in line if board[i] is None]
            if candidates:
                return candidates[0]
    # Block if needed
    for line in WIN_LINES:
        vals = [board[i] for i in line]
        if vals.count("X") == 2 and any(v is None for v in vals):
            candidates = [i for i in line if board[i] is None]
            if candidates:
                return candidates[0]
    # Center
    if board[4] is None:
        return 4
    # Random corner or edge
    empties = _empty_cells(board)
    return random.choice(empties) if empties else None


_current_board: list[str | None] = [None] * 9
_current_game_over = False


def init_game() -> dict:
    global _current_board, _current_game_over
    _current_board = [None] * 9
    _current_game_over = False
    return _state()


def _state() -> dict:
    return {
        "board": list(_current_board),
        "gameOver": _current_game_over,
        "status": "YOUR TURN (X)"
        if not _current_game_over
        else (
            "YOU WIN!"
            if _check_win(_current_board, "X")
            else ("AI WINS!" if _check_win(_current_board, "O") else "TIE!")
        ),
    }


def state() -> dict:
    return _state()


def handle_action(action: dict) -> dict:
    global _current_board, _current_game_over
    if _current_game_over:
        return {"error": "Game over"}
    idx = action["index"]
    if _current_board[idx] is not None:
        return {"error": "Cell taken"}
    _current_board[idx] = "X"
    if _check_win(_current_board, "X"):
        _current_game_over = True
        return _state()
    if not _empty_cells(_current_board):
        _current_game_over = True
        return _state()
    ai_idx = _find_best_move(_current_board)
    if ai_idx is not None:
        _current_board[ai_idx] = "O"
        if _check_win(_current_board, "O"):
            _current_game_over = True
    if not _empty_cells(_current_board) and not _current_game_over:
        _current_game_over = True
    return _state()
