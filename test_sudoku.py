import unittest

from sudoku import DIFFICULTIES, BOARD_SIZE, create_board, is_valid_move, load_board


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


class TestLoadBoard(unittest.TestCase):
    def test_loads_a_9x9_board_for_each_difficulty(self):
        for difficulty in DIFFICULTIES:
            with self.subTest(difficulty=difficulty):
                board = load_board(difficulty)

                self.assertEqual(len(board), BOARD_SIZE)
                self.assertTrue(all(len(row) == BOARD_SIZE for row in board))
                self.assertTrue(
                    all(0 <= value <= BOARD_SIZE for row in board for value in row)
                )
                self.assertTrue(any(value == 0 for row in board for value in row))

    def test_returns_a_copy_that_can_be_changed_independently(self):
        board = load_board("easy")
        original_value = board[0][0]
        board[0][0] = 0

        self.assertNotEqual(board[0][0], load_board("easy")[0][0])
        self.assertEqual(load_board("easy")[0][0], original_value)

    def test_rejects_unknown_difficulty(self):
        with self.assertRaises(ValueError):
            load_board("expert")


if __name__ == "__main__":
    unittest.main()
