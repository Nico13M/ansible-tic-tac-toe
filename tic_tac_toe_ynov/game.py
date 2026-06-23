from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


WINNING_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


@dataclass
class GameState:
    board: list[str] = field(default_factory=lambda: [" " for _ in range(9)])
    current_player: str = "X"

    def play(self, position: int) -> None:
        if position < 0 or position > 8:
            raise ValueError("position must be between 0 and 8")
        if self.board[position] != " ":
            raise ValueError("cell is already occupied")
        self.board[position] = self.current_player
        self.current_player = "O" if self.current_player == "X" else "X"

    def winner(self) -> str | None:
        for a, b, c in WINNING_LINES:
            if self.board[a] != " " and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def is_draw(self) -> bool:
        return self.winner() is None and all(cell != " " for cell in self.board)

    def available_moves(self) -> Iterable[int]:
        return [index for index, cell in enumerate(self.board) if cell == " "]
