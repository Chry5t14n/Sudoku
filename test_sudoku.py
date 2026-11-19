import unittest

from sudoku import BOARD_SIZE, create_board, is_valid_move


class TestCreateBoard(unittest.TestCase):
    def test_returns_empty_9x9_matrix(self):
        board = create_board()

        self.assertEqual(len(board), BOARD_SIZE)
        self.assertTrue(all(len(row) == BOARD_SIZE for row in board))
        self.assertTrue(all(value == 0 for row in board for value in row))

    def test_rows_are_independent(self):
        board = create_board()
        board[0][0] = 5

        self.assertEqual(board[0][0], 5)
        self.assertEqual(board[1][0], 0)


class TestIsValidMove(unittest.TestCase):
    def test_accepts_number_without_conflicts(self):
        board = create_board()

        self.assertTrue(is_valid_move(board, 0, 0, 5))

    def test_rejects_number_repeated_in_row(self):
        board = create_board()
        board[0][4] = 5

        self.assertFalse(is_valid_move(board, 0, 0, 5))

    def test_rejects_number_repeated_in_column(self):
        board = create_board()
        board[4][0] = 5

        self.assertFalse(is_valid_move(board, 0, 0, 5))

    def test_rejects_number_repeated_in_box(self):
        board = create_board()
        board[1][1] = 5

        self.assertFalse(is_valid_move(board, 0, 0, 5))

    def test_rejects_invalid_number_or_occupied_position(self):
        board = create_board()
        board[0][0] = 5

        self.assertFalse(is_valid_move(board, 0, 1, 0))
        self.assertFalse(is_valid_move(board, 0, 0, 5))


if __name__ == "__main__":
    unittest.main()
