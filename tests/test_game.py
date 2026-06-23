from tic_tac_toe_ynov.game import GameState


def test_winner_detects_horizontal_line() -> None:
    game = GameState(board=["X", "X", "X", " ", " ", " ", " ", " ", " "])

    assert game.winner() == "X"


def test_draw_detects_full_board_without_winner() -> None:
    game = GameState(board=["X", "O", "X", "X", "O", "O", "O", "X", "X"])

    assert game.is_draw() is True


def test_play_switches_player_and_rejects_occupied_cell() -> None:
    game = GameState()

    game.play(0)

    assert game.board[0] == "X"
    assert game.current_player == "O"
