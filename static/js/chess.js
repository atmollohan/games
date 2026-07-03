const CHESS_PIECES = {
  'K': '\u2654', 'Q': '\u2655', 'R': '\u2656', 'B': '\u2657',
  'N': '\u2658', 'P': '\u2659', 'k': '\u265A', 'q': '\u265B',
  'r': '\u265C', 'b': '\u265D', 'n': '\u265E', 'p': '\u265F',
};

let chessState = null;
let chessSelected = null;
let chessValidMoves = [];

function pieceColor(p) {
  return p ? (p === p.toUpperCase() ? 'w' : 'b') : null;
}

async function initChess() {
  const r = await fetch('/api/chess/init', { method: 'POST' });
  chessState = await r.json();
  chessSelected = null;
  chessValidMoves = [];
  renderChess();
}

async function onChessClick(r, c) {
  if (!chessState || chessState.gameOver) return;
  if (chessSelected) {
    if (chessValidMoves.some(m => m[0] === r && m[1] === c)) {
      const res = await fetch('/api/chess/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ from: chessSelected, to: [r, c] }),
      });
      chessState = await res.json();
      chessSelected = null;
      chessValidMoves = [];
      renderChess();
      return;
    }
    const p = chessState.board[r][c];
    if (p && pieceColor(p) === chessState.turn) {
      chessSelected = [r, c];
      chessValidMoves = chessState.legalMoves[`${r}_${c}`] || [];
      renderChess();
      return;
    }
    chessSelected = null;
    chessValidMoves = [];
    renderChess();
    return;
  }
  const p = chessState.board[r][c];
  if (p && pieceColor(p) === chessState.turn) {
    chessSelected = [r, c];
    chessValidMoves = chessState.legalMoves[`${r}_${c}`] || [];
    renderChess();
  }
}

function renderChess() {
  if (!chessState) return;
  const b = document.getElementById('chess-board');
  b.innerHTML = '';
  for (let r = 0; r < 8; r++) {
    for (let c = 0; c < 8; c++) {
      const sq = document.createElement('div');
      sq.className = 'chess-square ' + ((r + c) % 2 === 0 ? 'light' : 'dark');
      sq.dataset.r = r;
      sq.dataset.c = c;
      const piece = chessState.board[r][c];
      if (piece) sq.textContent = CHESS_PIECES[piece] || '';
      if (chessSelected && chessSelected[0] === r && chessSelected[1] === c) {
        sq.classList.add('selected', 'move-from');
      }
      if (chessValidMoves.some(m => m[0] === r && m[1] === c)) {
        if (chessState.board[r][c]) sq.classList.add('valid-capture');
        else sq.classList.add('valid-move');
      }
      sq.addEventListener('click', () => onChessClick(r, c));
      b.appendChild(sq);
    }
  }
  document.getElementById('chess-turn').textContent =
    chessState.turn === 'w' ? 'WHITE' : 'BLACK';
  document.getElementById('chess-status').textContent = chessState.status || '';
  const sv = (p) => ({ q: 9, r: 5, b: 3, n: 3, p: 1 })[p.toLowerCase()] || 0;
  const cw = (chessState.captured?.w || []).sort((a, b) => sv(b) - sv(a));
  const cb = (chessState.captured?.b || []).sort((a, b) => sv(b) - sv(a));
  document.getElementById('chess-captured-w').innerHTML =
    cw.map(p => '<span>' + (CHESS_PIECES[p] || p) + '</span>').join('');
  document.getElementById('chess-captured-b').innerHTML =
    cb.map(p => '<span>' + (CHESS_PIECES[p] || p) + '</span>').join('');
}
