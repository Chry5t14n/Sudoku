"""Estrutura e exibição do tabuleiro de Sudoku."""

BOARD_SIZE = 9
BOX_SIZE = 3
DIFFICULTIES = ("easy", "medium", "hard")

_PUZZLES = {
    "easy": (
        (5, 3, 0, 0, 7, 0, 0, 0, 0),
        (6, 0, 0, 1, 9, 5, 0, 0, 0),
        (0, 9, 8, 0, 0, 0, 0, 6, 0),
        (8, 0, 0, 0, 6, 0, 0, 0, 3),
        (4, 0, 0, 8, 0, 3, 0, 0, 1),
        (7, 0, 0, 0, 2, 0, 0, 0, 6),
        (0, 6, 0, 0, 0, 0, 2, 8, 0),
        (0, 0, 0, 4, 1, 9, 0, 0, 5),
        (0, 0, 0, 0, 8, 0, 0, 7, 9),
    ),
    "medium": (
        (5, 3, 0, 0, 7, 0, 0, 0, 0),
        (6, 0, 0, 1, 0, 5, 0, 0, 0),
        (0, 9, 8, 0, 0, 0, 0, 6, 0),
        (8, 0, 0, 0, 6, 0, 0, 0, 0),
        (4, 0, 0, 8, 0, 3, 0, 0, 1),
        (7, 0, 0, 0, 2, 0, 0, 0, 0),
        (0, 6, 0, 0, 0, 0, 2, 8, 0),
        (0, 0, 0, 4, 1, 0, 0, 0, 5),
        (0, 0, 0, 0, 8, 0, 0, 7, 9),
    ),
    "hard": (
        (5, 0, 0, 0, 7, 0, 0, 0, 0),
        (6, 0, 0, 1, 0, 0, 0, 0, 0),
        (0, 9, 0, 0, 0, 0, 0, 6, 0),
        (8, 0, 0, 0, 6, 0, 0, 0, 0),
        (4, 0, 0, 0, 0, 3, 0, 0, 1),
        (7, 0, 0, 0, 2, 0, 0, 0, 0),
        (0, 6, 0, 0, 0, 0, 2, 0, 0),
        (0, 0, 0, 4, 0, 0, 0, 0, 5),
        (0, 0, 0, 0, 8, 0, 0, 7, 9),
    ),
}


def create_board() -> list[list[int]]:
    """Cria um tabuleiro 9x9 vazio, representado por zeros."""
    return [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def load_board(difficulty: str) -> list[list[int]]:
    """Carrega uma cópia do tabuleiro pré-pronto na dificuldade escolhida."""
    if difficulty not in DIFFICULTIES:
        raise ValueError(f"Dificuldade inválida: {difficulty}")

    return [list(row) for row in _PUZZLES[difficulty]]


def is_valid_move(board: list[list[int]], row: int, column: int, number: int) -> bool:
    """Verifica se um número pode ser inserido na posição indicada."""
    if not 0 <= row < BOARD_SIZE or not 0 <= column < BOARD_SIZE:
        return False
    if not 1 <= number <= BOARD_SIZE or board[row][column] != 0:
        return False

    if number in board[row]:
        return False

    if any(board[current_row][column] == number for current_row in range(BOARD_SIZE)):
        return False

    box_start_row = (row // BOX_SIZE) * BOX_SIZE
    box_start_column = (column // BOX_SIZE) * BOX_SIZE
    return all(
        board[current_row][current_column] != number
        for current_row in range(box_start_row, box_start_row + BOX_SIZE)
        for current_column in range(box_start_column, box_start_column + BOX_SIZE)
    )


def display_board(board: list[list[int]]) -> None:
    """Exibe o tabuleiro no terminal, usando '.' para casas vazias."""
    separator = "+-------+-------+-------+"

    for row_index, row in enumerate(board):
        if row_index % 3 == 0:
            print(separator)

        values = ["." if value == 0 else str(value) for value in row]
        print(
            f"| {' '.join(values[0:3])} "
            f"| {' '.join(values[3:6])} "
            f"| {' '.join(values[6:9])} |"
        )

    print(separator)


if __name__ == "__main__":
    display_board(create_board())
