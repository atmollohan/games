let chkState = null;
let chkSelected = null;
let chkValidMoves = [];

function pieceColor(p) {
  return p ? p.toLowerCase() : null;
}

function isKing(p) {
  return p && p === p.toUpperCase();
}

async function initCheckers() {
  const r = await fetch('/api/checkers/init', { method: 'POST' });
  chkState = await r.json();
  chkSelected = null;
  chkValidMoves = [];
  renderCheckers();
}

async function onChkClick(r, c) {
  if (!chkState || chkState.gameOver) return;
  if (chkSelected) {
    if (chkValidMoves.some(m => m.to[0] === r && m.to[1] === c)) {
      const res = await fetch('/api/checkers/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: 'move', from: chkSelected, to: [r, c] }),
      });
      chkState = await res.json();
      chkSelected = chkState.selected || null;
      chkValidMoves = chkState.validMoves || [];
      renderCheckers();
      return;
    }
    if (chkState.board[r][c] && pieceColor(chkState.board[r][c]) === chkState.turn) {
      const res = await fetch('/api/checkers/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: 'select', pos: [r, c] }),
      });
      chkState = await res.json();
      chkSelected = [r, c];
      chkValidMoves = chkState.validMoves || [];
      renderCheckers();
      return;
    }
    chkSelected = null;
    chkValidMoves = [];
    renderCheckers();
    return;
  }
  if (chkState.board[r][c] && pieceColor(chkState.board[r][c]) === chkState.turn) {
    const res = await fetch('/api/checkers/move', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: 'select', pos: [r, c] }),
    });
    chkState = await res.json();
    chkSelected = [r, c];
    chkValidMoves = chkState.validMoves || [];
    renderCheckers();
  }
}

function renderCheckers() {
  if (!chkState) return;
  const b = document.getElementById('checkers-board');
  b.innerHTML = '';
  for (let r = 0; r < 8; r++) {
    for (let c = 0; c < 8; c++) {
      const sq = document.createElement('div');
      sq.className = 'chk-square ' + ((r + c) % 2 === 0 ? 'light' : 'dark');
      sq.dataset.r = r;
      sq.dataset.c = c;
      if (chkState.board[r][c]) {
        const p = document.createElement('div');
        const pChar = chkState.board[r][c];
        p.className = 'chk-piece ' + (pieceColor(pChar) === 'r' ? 'red' : 'black');
        if (isKing(pChar)) p.classList.add('king');
        sq.appendChild(p);
      }
      if (chkSelected && chkSelected[0] === r && chkSelected[1] === c) sq.classList.add('selected');
      if (chkValidMoves.some(m => m.to[0] === r && m.to[1] === c)) {
        if (chkState.board[r][c]) sq.classList.add('valid-capture');
        else sq.classList.add('valid-move');
      }
      sq.addEventListener('click', () => onChkClick(r, c));
      b.appendChild(sq);
    }
  }
  document.getElementById('checkers-turn').textContent = chkState.turnLabel || '';
  const statusEl = document.getElementById('checkers-status');
  if (chkState.gameOver) {
    statusEl.textContent = (chkState.redCount === 0 ? 'BLACK' : 'RED') + ' WINS!';
  } else {
    statusEl.textContent = chkSelected ? 'SELECT DESTINATION' : 'SELECT A PIECE';
  }
  document.getElementById('checkers-count').textContent =
    'RED: ' + chkState.redCount + ' \u2022 BLACK: ' + chkState.blackCount;
}
