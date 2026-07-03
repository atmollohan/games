PIECE_VALUES = {"P": 100, "N": 320, "B": 330, "R": 500, "Q": 900, "K": 20000}

PST = {
    "P": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    "N": [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50],
    ],
    "B": [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20],
    ],
    "R": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [0, 0, 0, 5, 5, 0, 0, 0],
    ],
    "Q": [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20],
    ],
    "K": [
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [20, 30, 10, 0, 0, 10, 30, 20],
    ],
}

INITIAL_BOARD = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
]

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

Board = list[list[str | None]]


def _clone_board(b: Board) -> Board:
    return [row[:] for row in b]


def _in_bounds(r: int, c: int) -> bool:
    return 0 <= r < 8 and 0 <= c < 8


def piece_color(p: str | None) -> str | None:
    if p is None:
        return None
    return "w" if p.isupper() else "b"


def piece_type(p: str) -> str:
    return p.upper()


# ---------------------------------------------------------------------------
# State container (pure, no globals inside helpers)
# ---------------------------------------------------------------------------


class GameState:
    __slots__ = (
        "board",
        "turn",
        "selected",
        "valid_moves",
        "game_over",
        "captured",
        "en_passant",
        "castling",
    )

    def __init__(self) -> None:
        self.board = _clone_board(INITIAL_BOARD)
        self.turn = "w"
        self.selected: tuple[int, int] | None = None
        self.valid_moves: list[tuple[int, int]] = []
        self.game_over = False
        self.captured: dict[str, list[str]] = {"w": [], "b": []}
        self.en_passant: tuple[int, int] | None = None
        self.castling: dict[str, bool] = {"K": True, "Q": True, "k": True, "q": True}

    def copy(self) -> "GameState":
        s = GameState.__new__(GameState)
        s.board = _clone_board(self.board)
        s.turn = self.turn
        s.selected = self.selected
        s.valid_moves = list(self.valid_moves)
        s.game_over = self.game_over
        s.captured = {"w": list(self.captured["w"]), "b": list(self.captured["b"])}
        s.en_passant = self.en_passant
        s.castling = dict(self.castling)
        return s


# ---------------------------------------------------------------------------
# Pure board helpers (take state explicitly)
# ---------------------------------------------------------------------------


def _find_king(board: Board, color: str) -> tuple[int, int] | None:
    k = "K" if color == "w" else "k"
    for r in range(8):
        for c in range(8):
            if board[r][c] == k:
                return (r, c)
    return None


def _pseudo_moves(
    board: Board,
    r: int,
    c: int,
    ptype: str,
    color: str,
    en_passant: tuple[int, int] | None,
    castling_flags: dict[str, bool],
) -> list[tuple[int, int]]:
    moves: list[tuple[int, int]] = []
    enemy = "b" if color == "w" else "w"
    d = -1 if color == "w" else 1

    def add(tr: int, tc: int) -> bool:
        if not _in_bounds(tr, tc):
            return False
        t = board[tr][tc]
        if t and piece_color(t) == color:
            return False
        moves.append((tr, tc))
        return t is None

    if ptype == "P":
        sr = 6 if color == "w" else 1
        if _in_bounds(r + d, c) and board[r + d][c] is None:
            moves.append((r + d, c))
            if r == sr and board[r + 2 * d][c] is None:
                moves.append((r + 2 * d, c))
        for dc in (-1, 1):
            tr, tc2 = r + d, c + dc
            if _in_bounds(tr, tc2):
                t = board[tr][tc2]
                if t and piece_color(t) == enemy:
                    moves.append((tr, tc2))
                if en_passant and (tr, tc2) == en_passant:
                    moves.append((tr, tc2))
    elif ptype == "N":
        for dr, dc in ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)):
            add(r + dr, c + dc)
    elif ptype == "B":
        for dr, dc in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
            for i in range(1, 8):
                if not add(r + dr * i, c + dc * i):
                    break
    elif ptype == "R":
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            for i in range(1, 8):
                if not add(r + dr * i, c + dc * i):
                    break
    elif ptype == "Q":
        for dr, dc in ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)):
            for i in range(1, 8):
                if not add(r + dr * i, c + dc * i):
                    break
    elif ptype == "K":
        for dr, dc in ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)):
            add(r + dr, c + dc)
        row = 7 if color == "w" else 0
        if r == row and c == 4:
            if (
                color == "w"
                and castling_flags["K"]
                and board[row][5] is None
                and board[row][6] is None
                and board[row][7] == "R"
            ):
                moves.append((row, 6))
            if (
                color == "w"
                and castling_flags["Q"]
                and board[row][1] is None
                and board[row][2] is None
                and board[row][3] is None
                and board[row][0] == "R"
            ):
                moves.append((row, 2))
            if (
                color == "b"
                and castling_flags["k"]
                and board[row][5] is None
                and board[row][6] is None
                and board[row][7] == "r"
            ):
                moves.append((row, 6))
            if (
                color == "b"
                and castling_flags["q"]
                and board[row][1] is None
                and board[row][2] is None
                and board[row][3] is None
                and board[row][0] == "r"
            ):
                moves.append((row, 2))
    return moves


def _is_under_attack(
    board: Board,
    r: int,
    c: int,
    by_color: str,
    en_passant: tuple[int, int] | None,
    castling_flags: dict[str, bool],
) -> bool:
    for rr in range(8):
        for cc in range(8):
            p = board[rr][cc]
            if p is None or piece_color(p) != by_color:
                continue
            pm = _pseudo_moves(board, rr, cc, piece_type(p), by_color, en_passant, castling_flags)
            if (r, c) in pm:
                return True
    return False


def _in_check(state: GameState, color: str) -> bool:
    k = _find_king(state.board, color)
    if k is None:
        return False
    enemy = "b" if color == "w" else "w"
    return _is_under_attack(state.board, k[0], k[1], enemy, state.en_passant, state.castling)


def _legal_moves_for(state: GameState, r: int, c: int) -> list[tuple[int, int]]:
    p = state.board[r][c]
    if p is None:
        return []
    color = piece_color(p)
    ptype = piece_type(p)
    pseudo = _pseudo_moves(state.board, r, c, ptype, color, state.en_passant, state.castling)
    legal: list[tuple[int, int]] = []
    for tr, tc in pseudo:
        test = state.copy()
        test.board[tr][tc] = test.board[r][c]
        test.board[r][c] = None
        if ptype == "P" and state.en_passant and (tr, tc) == state.en_passant:
            ep_r = state.en_passant[0] - (-1 if color == "w" else 1)
            test.board[ep_r][state.en_passant[1]] = None
        if ptype == "K" and abs(tc - c) == 2:
            row = 7 if color == "w" else 0
            if tc == 6:
                test.board[row][5] = test.board[row][7]
                test.board[row][7] = None
            if tc == 2:
                test.board[row][3] = test.board[row][0]
                test.board[row][0] = None
        if not _in_check(test, color):
            legal.append((tr, tc))
    return legal


def _get_all_legal_moves(state: GameState, color: str) -> list[dict]:
    all_moves: list[dict] = []
    for r in range(8):
        for c in range(8):
            p = state.board[r][c]
            if p and piece_color(p) == color:
                moves = _legal_moves_for(state, r, c)
                for tr, tc in moves:
                    all_moves.append({"from": (r, c), "to": (tr, tc)})
    return all_moves


# ---------------------------------------------------------------------------
# Evaluation + AI
# ---------------------------------------------------------------------------


def _evaluate(state: GameState, color: str) -> int:
    score = 0
    for r in range(8):
        for c in range(8):
            p = state.board[r][c]
            if p is None:
                continue
            ptype = piece_type(p)
            pc = piece_color(p)
            val = PIECE_VALUES.get(ptype, 0)
            pst = PST.get(ptype)
            if pst:
                idx = r if pc == "w" else 7 - r
                val += pst[idx][c]
            score += val if pc == color else -val
    return score


def _apply_move(state: GameState, move: dict) -> None:
    fr, fc = move["from"]
    tr, tc = move["to"]
    p = state.board[fr][fc]
    ptype = piece_type(p)
    color = piece_color(p)
    state.board[tr][tc] = p
    state.board[fr][fc] = None
    if ptype == "P" and state.en_passant and (tr, tc) == state.en_passant:
        ep_r = state.en_passant[0] - (-1 if color == "w" else 1)
        state.board[ep_r][state.en_passant[1]] = None
    if ptype == "K" and abs(tc - fc) == 2:
        row = 7 if color == "w" else 0
        if tc == 6:
            state.board[row][5] = state.board[row][7]
            state.board[row][7] = None
        if tc == 2:
            state.board[row][3] = state.board[row][0]
            state.board[row][0] = None
    if ptype == "P" and (tr == 0 or tr == 7):
        state.board[tr][tc] = "Q" if color == "w" else "q"


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
    current_color = color if is_maximizing else ("b" if color == "w" else "w")
    moves = _get_all_legal_moves(state, current_color)
    if not moves:
        return -99999.0 if is_maximizing else 99999.0
    if is_maximizing:
        max_eval = -1e9
        for m in moves:
            test = state.copy()
            _apply_move(test, m)
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
            _apply_move(test, m)
            e = _minimax(test, depth - 1, alpha, beta, True, color)
            min_eval = min(min_eval, e)
            beta = min(beta, e)
            if beta <= alpha:
                break
        return min_eval


def _find_best_ai_move(state: GameState) -> dict | None:
    moves = _get_all_legal_moves(state, "b")
    if not moves:
        return None
    best_move = moves[0]
    best_score = -1e9
    for m in moves:
        test = state.copy()
        _apply_move(test, m)
        score = _minimax(test, 2, -1e9, 1e9, False, "b")
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
    legal_moves: dict[str, list[list[int]]] = {}
    for r in range(8):
        for c in range(8):
            if state.board[r][c] and piece_color(state.board[r][c]) == state.turn:
                moves = _legal_moves_for(state, r, c)
                if moves:
                    legal_moves[f"{r}_{c}"] = [list(m) for m in moves]
    status = "SELECT A PIECE"
    opp_moves = _get_all_legal_moves(state, "b" if state.turn == "w" else "w")
    if state.game_over or not opp_moves:
        in_check_status = _in_check(state, state.turn)
        if in_check_status:
            winner = "BLACK" if state.turn == "w" else "WHITE"
            status = f"CHECKMATE! {winner} WINS!"
        else:
            status = "STALEMATE!"
    elif _in_check(state, state.turn):
        status = "CHECK!"
    return {
        "board": state.board,
        "turn": state.turn,
        "selected": list(state.selected) if state.selected else None,
        "validMoves": [list(m) for m in state.valid_moves],
        "gameOver": state.game_over or not opp_moves,
        "captured": state.captured,
        "enPassant": list(state.en_passant) if state.en_passant else None,
        "castling": state.castling,
        "legalMoves": legal_moves,
        "status": status,
    }


def init_game() -> dict:
    global _current
    _current = GameState()
    return _state_to_dict(_s())


def state() -> dict:
    return _state_to_dict(_s())


def handle_action(action: dict) -> dict:
    state = _s()
    if state.game_over:
        return {"error": "Game over"}
    fr, fc = action["from"]
    tr, tc = action["to"]
    p = state.board[fr][fc]
    if p is None or piece_color(p) != state.turn:
        return {"error": "Not your piece"}
    legal = _legal_moves_for(state, fr, fc)
    if (tr, tc) not in legal:
        return {"error": "Invalid move"}
    _apply_player_move(state, fr, fc, tr, tc)
    if not state.game_over:
        ai_move = _find_best_ai_move(state)
        if ai_move:
            fr2, fc2 = ai_move["from"]
            tr2, tc2 = ai_move["to"]
            _apply_player_move(state, fr2, fc2, tr2, tc2)
    return _state_to_dict(state)


def _apply_player_move(state: GameState, fr: int, fc: int, tr: int, tc: int) -> None:
    p = state.board[fr][fc]
    ptype = piece_type(p)
    color = piece_color(p)
    enemy = "b" if color == "w" else "w"
    captured_piece = state.board[tr][tc]
    if captured_piece:
        state.captured[enemy].append(captured_piece)
    ep_capture = None
    if ptype == "P" and abs(tr - fr) == 2:
        state.en_passant = ((fr + tr) // 2, fc)
    else:
        if ptype == "P" and state.en_passant and (tr, tc) == state.en_passant:
            ep_capture = (state.en_passant[0] - (-1 if color == "w" else 1), state.en_passant[1])
        state.en_passant = None
    if ptype == "K":
        state.castling["K" if color == "w" else "k"] = False
        state.castling["Q" if color == "w" else "q"] = False
    if ptype == "R":
        if fc == 7 and fr == (7 if color == "w" else 0):
            state.castling["K" if color == "w" else "k"] = False
        if fc == 0 and fr == (7 if color == "w" else 0):
            state.castling["Q" if color == "w" else "q"] = False
    if tr == 7 and tc == 7:
        state.castling["K"] = False
    if tr == 7 and tc == 0:
        state.castling["Q"] = False
    if tr == 0 and tc == 7:
        state.castling["k"] = False
    if tr == 0 and tc == 0:
        state.castling["q"] = False
    state.board[tr][tc] = p
    state.board[fr][fc] = None
    if ep_capture:
        state.board[ep_capture[0]][ep_capture[1]] = None
        state.captured[enemy].append("p" if color == "w" else "P")
    if ptype == "K" and abs(tc - fc) == 2:
        row = 7 if color == "w" else 0
        if tc == 6:
            state.board[row][5] = state.board[row][7]
            state.board[row][7] = None
        if tc == 2:
            state.board[row][3] = state.board[row][0]
            state.board[row][0] = None
    if ptype == "P" and (tr == 0 or tr == 7):
        state.board[tr][tc] = "Q" if color == "w" else "q"
    state.selected = None
    state.valid_moves = []
    state.turn = enemy
    opp_moves = _get_all_legal_moves(state, state.turn)
    if not opp_moves:
        state.game_over = True
