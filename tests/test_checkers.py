from games import checkers


def test_init_game():
    state = checkers.init_game()
    assert state["turn"] == "r"
    assert not state["gameOver"]
    assert state["redCount"] == 12
    assert state["blackCount"] == 12
    assert state["board"][0][1] == "b"
    assert state["board"][7][0] == "r"


def test_select_red_piece():
    state = checkers.init_game()
    state = checkers.handle_action({"type": "select", "pos": (5, 0)})
    assert state["selected"] == [5, 0]
    assert len(state["validMoves"]) > 0


def test_select_black_piece_wrong_turn():
    checkers.init_game()
    result = checkers.handle_action({"type": "select", "pos": (2, 1)})
    # Selecting black when it's red's turn should clear selection or error
    assert "error" not in result  # Just returns state with no selection


def test_red_moves_forward():
    state = checkers.init_game()
    state = checkers.handle_action({"type": "select", "pos": (5, 0)})
    assert len(state["validMoves"]) > 0
    dest = state["validMoves"][0]["to"]
    state = checkers.handle_action(
        {
            "type": "move",
            "from": [5, 0],
            "to": dest,
        }
    )
    assert state["board"][dest[0]][dest[1]] == "r"
    assert state["board"][5][0] is None


def test_game_over():
    state = checkers.init_game()
    assert not state["gameOver"]
