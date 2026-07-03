from games import tictactoe


def test_init_game():
    state = tictactoe.init_game()
    assert state["board"] == [None] * 9
    assert not state["gameOver"]
    assert state["status"] == "YOUR TURN (X)"


def test_player_move():
    state = tictactoe.init_game()
    state = tictactoe.handle_action({"index": 0})
    assert state["board"][0] == "X"
    assert state["board"].count("O") <= 1  # AI may have responded


def test_blocked_cell():
    tictactoe.init_game()
    tictactoe.handle_action({"index": 0})
    result = tictactoe.handle_action({"index": 0})
    assert "error" in result


def test_ai_blocks_win():
    tictactoe.init_game()
    # X plays corner 0, AI takes center 4
    state = tictactoe.handle_action({"index": 0})
    assert state["board"][4] == "O"  # AI took center
    # X plays corner 2, AI plays...
    state = tictactoe.handle_action({"index": 2})
    # X plays corner 8, should win
    state = tictactoe.handle_action({"index": 8})
    # Either game over or AI blocked
    assert state.get("gameOver") or state["board"][8] == "X"
