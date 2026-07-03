let tttState = null;

async function initTictactoe() {
  const r = await fetch('/api/tictactoe/init', { method: 'POST' });
  tttState = await r.json();
  updateTictactoeBoard();
}

async function playTictactoe(idx) {
  if (!tttState || tttState.gameOver) return;
  if (tttState.board[idx]) return;
  const res = await fetch('/api/tictactoe/action', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ index: idx }),
  });
  tttState = await res.json();
  updateTictactoeBoard();
}

function updateTictactoeBoard() {
  if (!tttState) return;
  const cells = document.querySelectorAll('#board-tictactoe .cell');
  cells.forEach((c, i) => {
    c.textContent = tttState.board[i] || '';
    c.style.color = tttState.board[i] === 'X' ? '#ff6b6b' : '#4ecdc4';
  });
  document.getElementById('status-tictactoe').textContent = tttState.status || '';
}
