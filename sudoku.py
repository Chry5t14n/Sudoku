"""Estrutura e exibição do tabuleiro de Sudoku."""

BOARD_SIZE = 9


def create_board() -> list[list[int]]:
    """Cria um tabuleiro 9x9 vazio, representado por zeros."""
    return [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


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
