"""Estrutura e exibição do tabuleiro de Sudoku."""

from random import Random

BOARD_SIZE = 9
BOX_SIZE = 3
DIFFICULTIES = ("easy", "medium", "hard")
_CLUES_BY_DIFFICULTY = {
    "easy": 40,
    "medium": 32,
    "hard": 24,
}

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


def generate_board(difficulty: str, rng: Random | None = None) -> list[list[int]]:
    """Gera um tabuleiro aleatório com solução válida na dificuldade escolhida."""
    if difficulty not in DIFFICULTIES:
        raise ValueError(f"Dificuldade inválida: {difficulty}")

    random_source = rng if rng is not None else Random()
    board = create_board()

    def fill_board() -> bool:
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                if board[row][column] != 0:
                    continue

                numbers = list(range(1, BOARD_SIZE + 1))
                random_source.shuffle(numbers)
                for number in numbers:
                    if is_valid_move(board, row, column, number):
                        board[row][column] = number
                        if fill_board():
                            return True
                        board[row][column] = 0
                return False
        return True

    if not fill_board():
        raise RuntimeError("Não foi possível gerar uma solução de Sudoku.")

    positions = [
        (row, column)
        for row in range(BOARD_SIZE)
        for column in range(BOARD_SIZE)
    ]
    random_source.shuffle(positions)
    cells_to_remove = BOARD_SIZE * BOARD_SIZE - _CLUES_BY_DIFFICULTY[difficulty]
    for row, column in positions[:cells_to_remove]:
        board[row][column] = 0

    return board


def load_board(difficulty: str) -> list[list[int]]:
    """Carrega uma cópia do tabuleiro pré-pronto na dificuldade escolhida."""
    if difficulty not in DIFFICULTIES:
        raise ValueError(f"Dificuldade inválida: {difficulty}")

    return [list(row) for row in _PUZZLES[difficulty]]


def get_fixed_cells(board: list[list[int]]) -> set[tuple[int, int]]:
    """Retorna as posições preenchidas pelo tabuleiro inicial."""
    return {
        (row, column)
        for row in range(BOARD_SIZE)
        for column in range(BOARD_SIZE)
        if board[row][column] != 0
    }


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


def is_winning_board(board: list[list[int]]) -> bool:
    """Verifica se o tabuleiro está completo e sem conflitos."""
    expected_values = set(range(1, BOARD_SIZE + 1))

    if any(
        len(row) != BOARD_SIZE or any(value not in expected_values for value in row)
        for row in board
    ) or len(board) != BOARD_SIZE:
        return False

    if any(set(row) != expected_values for row in board):
        return False

    if any(
        {board[row][column] for row in range(BOARD_SIZE)} != expected_values
        for column in range(BOARD_SIZE)
    ):
        return False

    return all(
        {
            board[row][column]
            for row in range(box_start_row, box_start_row + BOX_SIZE)
            for column in range(box_start_column, box_start_column + BOX_SIZE)
        }
        == expected_values
        for box_start_row in range(0, BOARD_SIZE, BOX_SIZE)
        for box_start_column in range(0, BOARD_SIZE, BOX_SIZE)
    )


def apply_move(
    board: list[list[int]],
    fixed_cells: set[tuple[int, int]],
    row: int,
    column: int,
    number: int,
) -> bool:
    """Aplica uma jogada válida, sem alterar posições fixas."""
    if (row, column) in fixed_cells or not is_valid_move(board, row, column, number):
        return False

    board[row][column] = number
    return True


def read_move(input_fn=input) -> tuple[int, int, int] | None:
    """Lê uma jogada em formato de usuário: linha, coluna e número."""
    raw_move = input_fn("Digite linha, coluna e número (ou 'sair'): ").strip()
    if raw_move.lower() == "sair":
        return None

    values = raw_move.split()
    if len(values) != 3:
        raise ValueError("Informe exatamente três números.")

    try:
        row, column, number = (int(value) for value in values)
    except ValueError as error:
        raise ValueError("Linha, coluna e número devem ser inteiros.") from error

    if not all(1 <= value <= BOARD_SIZE for value in (row, column, number)):
        raise ValueError("Linha, coluna e número devem estar entre 1 e 9.")

    return row - 1, column - 1, number


def display_board(board: list[list[int]], output_fn=print) -> None:
    """Exibe o tabuleiro no terminal, usando '.' para casas vazias."""
    separator = "+-------+-------+-------+"

    for row_index, row in enumerate(board):
        if row_index % 3 == 0:
            output_fn(separator)

        values = ["." if value == 0 else str(value) for value in row]
        output_fn(
            f"| {' '.join(values[0:3])} "
            f"| {' '.join(values[3:6])} "
            f"| {' '.join(values[6:9])} |"
        )

    output_fn(separator)


def play_game(board: list[list[int]], input_fn=input, output_fn=print) -> None:
    """Executa o loop de interação do jogador no terminal."""
    fixed_cells = get_fixed_cells(board)

    while True:
        display_board(board, output_fn)
        try:
            move = read_move(input_fn)
        except EOFError:
            output_fn("Jogo encerrado.")
            return
        except ValueError as error:
            output_fn(f"Entrada inválida: {error}")
            continue

        if move is None:
            output_fn("Jogo encerrado.")
            return

        row, column, number = move
        if (row, column) in fixed_cells:
            output_fn("Essa posição é fixa e não pode ser alterada.")
        elif apply_move(board, fixed_cells, row, column, number):
            output_fn("Jogada aplicada.")
            if is_winning_board(board):
                output_fn("Parabéns! Você completou o Sudoku!")
                return
        else:
            output_fn("Jogada inválida.")


if __name__ == "__main__":
    play_game(load_board("easy"))
