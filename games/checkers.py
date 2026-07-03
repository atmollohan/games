Board = list[list[str | None]]

INITIAL_BOARD: Board = [
    [None, "b", None, "b", None, "b", None, "b"],
    ["b", None, "b", None, "b", None, "b", None],
    [None, "b", None, "b", None, "b", None, "b"],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ["r", None, "r", None, "r", None, "r", None],
    [None, "r", None, "r", None, "r", None, "r"],
    ["r", None, "r", None, "r", None, "r", None],
]


def _clone_board(b: Board) -> Board:
    return [row[:] for row in b]


def _in_bounds(r: int, c: int) -> bool:
    return 0 <= r < 8 and 0 <= c < 8


def piece_color(p: str | None) -> str | None:
    if p is None:
        return None
    return p.lower()


def is_king(p: str | None) -> bool:
    return bool(p and p == p.upper())


# ---------------------------------------------------------------------------
# State container
# ---------------------------------------------------------------------------


class GameState:
    __slots__ = (
        "board",
        "turn",
        "selected",
        "valid_moves",
        "game_over",
        "red_count",
        "black_count",
        "must_jump",
    )

    def __init__(self) -> None:
        self.board = _clone_board(INITIAL_BOARD)
        self.turn = "r"
        self.selected: tuple[int, int] | None = None
        self.valid_moves: list[dict] = []
        self.game_over = False
        self.red_count = 12
        self.black_count = 12
        self.must_jump = False

    def copy(self) -> "GameState":
        s = GameState.__new__(GameState)
        s.board = _clone_board(self.board)
        s.turn = self.turn
        s.selected = self.selected
        s.valid_moves = [dict(m) for m in self.valid_moves]
        s.game_over = self.game_over
        s.red_count = self.red_count
        s.black_count = self.black_count
        s.must_jump = self.must_jump
        return s


# ---------------------------------------------------------------------------
# Move generation
# ---------------------------------------------------------------------------


def _get_moves(board: Board, r: int, c: int, must_jump: bool) -> list[dict]:
    p = board[r][c]
    if p is None:
        return []
    color = piece_color(p)
    king = is_king(p)
    dirs = [-1, 1] if king else [-1 if color == "r" else 1]
    moves: list[dict] = []
    jumps: list[dict] = []
    for dr in dirs:
        for dc in (-1, 1):
            tr, tc = r + dr, c + dc
            if not _in_bounds(tr, tc):
                continue
            if board[tr][tc] is None:
                if not must_jump:
                    moves.append({"to": (tr, tc), "jump": None})
            elif piece_color(board[tr][tc]) != color:
                jr, jc = r + 2 * dr, c + 2 * dc
                if _in_bounds(jr, jc) and board[jr][jc] is None:
                    jumps.append({"to": (jr, jc), "jump": (tr, tc)})
    if jumps:
        return jumps
    return moves


def _get_all_moves(board: Board, color: str, must_jump: bool) -> list[dict]:
    all_moves: list[dict] = []
    for r in range(8):
        for c in range(8):
            if board[r][c] and piece_color(board[r][c]) == color:
                moves = _get_moves(board, r, c, must_jump)
                for m in moves:
                    all_moves.append({"from": (r, c), **m})
    return all_moves


def _has_jumps(board: Board, color: str) -> bool:
    for r in range(8):
        for c in range(8):
            if board[r][c] and piece_color(board[r][c]) == color:
                if any(m.get("jump") for m in _get_moves(board, r, c, False)):
                    return True
    return False


# ---------------------------------------------------------------------------
# Evaluation + AI
# ---------------------------------------------------------------------------


def _evaluate(state: GameState, color: str) -> float:
    score = 0.0
    for r in range(8):
        for c in range(8):
            p = state.board[r][c]
            if p is None:
                continue
            pc = piece_color(p)
            king = is_king(p)
            val = 3.0 if king else 1.0
            pos = (7 - r) if pc == "r" else r
            score += (val + pos * 0.1) if pc == color else -(val + pos * 0.1)
    return score


def _apply_move(board: Board, move: dict) -> None:
    fr, fc = move["from"]
    tr, tc = move["to"]
    p = board[fr][fc]
    color = piece_color(p)
    board[tr][tc] = p
    board[fr][fc] = None
    if move.get("jump"):
        jr, jc = move["jump"]
        board[jr][jc] = None
    king_row = 0 if color == "r" else 7
    if tr == king_row and not is_king(p):
        board[tr][tc] = color.upper()


def _minimax(
    state: GameState,
    depth: int,
    alpha: float,
    beta: float,
    is_maximizing: bool,
    color: str,
) -> float:
    if depth == 0:
        return _evaluate(state, color)
    current_color = color if is_maximizing else ("b" if color == "r" else "r")
    jumps_exist = _has_jumps(state.board, current_color)
    moves = _get_all_moves(state.board, current_color, jumps_exist)
    if not moves:
        return -999.0 if is_maximizing else 999.0
    if is_maximizing:
        max_eval = -1e9
        for m in moves:
            test = state.copy()
            _apply_move(test.board, m)
            e = _minimax(test, depth - 1, alpha, beta, False, color)
            max_eval = max(max_eval, e)
            alpha = max(alpha, e)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = 1e9
        for m in moves:
            test = state.copy()
            _apply_move(test.board, m)
            e = _minimax(test, depth - 1, alpha, beta, True, color)
            min_eval = min(min_eval, e)
            beta = min(beta, e)
            if beta <= alpha:
                break
        return min_eval


def _find_best_ai_move(state: GameState) -> dict | None:
    jumps_exist = _has_jumps(state.board, "b")
    moves = _get_all_moves(state.board, "b", jumps_exist)
    if not moves:
        return None
    best_move = moves[0]
    best_score = -1e9
    for m in moves:
        test = state.copy()
        _apply_move(test.board, m)
        score = _minimax(test, 4, -1e9, 1e9, False, "b")
        if score > best_score:
            best_score = score
            best_move = m
    return best_move


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

_current: GameState | None = None


def _s() -> GameState:
    global _current
    if _current is None:
        _current = GameState()
    return _current


def _state_to_dict(state: GameState) -> dict:
    return {
        "board": state.board,
        "turn": state.turn,
        "selected": list(state.selected) if state.selected else None,
        "validMoves": [
            {"to": list(m["to"]), "jump": list(m["jump"]) if m.get("jump") else None}
            for m in state.valid_moves
        ],
        "gameOver": state.game_over,
        "redCount": state.red_count,
        "blackCount": state.black_count,
        "status": "SELECT A PIECE",
        "turnLabel": "RED'S TURN" if state.turn == "r" else "BLACK'S TURN",
    }


def init_game() -> dict:
    global _current
    _current = GameState()
    return _state_to_dict(_s())


def state() -> dict:
    return _state_to_dict(_s())


def handle_action(action: dict) -> dict:
    st = _s()
    if st.game_over:
        return {"error": "Game over"}
    action_type = action.get("type", "select")
    if action_type == "select":
        r, c = action["pos"]
        return _handle_select(st, r, c)
    elif action_type == "move":
        fr, fc = action["from"]
        tr, tc = action["to"]
        return _handle_move(st, fr, fc, tr, tc)
    return {"error": "Unknown action type"}


def _handle_select(state: GameState, r: int, c: int) -> dict:
    p = state.board[r][c]
    if p and piece_color(p) == state.turn:
        jumps_exist = _has_jumps(state.board, state.turn)
        moves = _get_moves(state.board, r, c, jumps_exist)
        state.selected = (r, c)
        state.valid_moves = moves
        return _state_to_dict(state)
    state.selected = None
    state.valid_moves = []
    return _state_to_dict(state)


def _handle_move(state: GameState, fr: int, fc: int, tr: int, tc: int) -> dict:
    if state.selected is None or state.selected != (fr, fc):
        return {"error": "No piece selected at that position"}
    move = next((m for m in state.valid_moves if m["to"] == (tr, tc)), None)
    if move is None:
        return {"error": "Invalid destination"}
    _apply_player_move(state, fr, fc, tr, tc, move)
    if not state.game_over and state.turn == "b":
        ai_move = _find_best_ai_move(state)
        if ai_move:
            fr2, fc2 = ai_move["from"]
            tr2, tc2 = ai_move["to"]
            _apply_player_move(state, fr2, fc2, tr2, tc2, ai_move)
    return _state_to_dict(state)


def _apply_player_move(state: GameState, fr: int, fc: int, tr: int, tc: int, move: dict) -> None:
    p = state.board[fr][fc]
    color = piece_color(p)
    state.board[tr][tc] = p
    state.board[fr][fc] = None
    if move.get("jump"):
        jr, jc = move["jump"]
        state.board[jr][jc] = None
        if color == "r":
            state.black_count -= 1
        else:
            state.red_count -= 1
    king_row = 0 if color == "r" else 7
    if tr == king_row and not is_king(p):
        state.board[tr][tc] = color.upper()
    state.selected = None
    state.valid_moves = []
    if state.black_count == 0 or state.red_count == 0:
        state.game_over = True
        return
    if move.get("jump"):
        chain_moves = _get_moves(state.board, tr, tc, True)
        if any(m.get("jump") for m in chain_moves):
            state.selected = (tr, tc)
            state.valid_moves = chain_moves
            return
    state.turn = "b" if color == "r" else "r"
    opp_moves = _get_all_moves(state.board, state.turn, False)
    if not opp_moves:
        state.game_over = True
