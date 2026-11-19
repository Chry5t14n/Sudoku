import unittest

from sudoku import BOARD_SIZE, create_board


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


if __name__ == "__main__":
    unittest.main()
