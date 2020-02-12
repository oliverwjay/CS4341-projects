import unittest
import timeit
import fast_board
import board


class FastBoardTests(unittest.TestCase):
    def time_outcome(self, w, h, n, moves=None):
        """
        Times how long it takes to evaluate a given board 10000 times and prints the results
        :param w: Board width
        :param h: Board height
        :param n: Number in a row needed to win
        :param moves: List of moves for sample board
        :return: None
        """
        print(f"\nSize: {(w, h)} n: {n}")
        slow_board = board.Board([[0] * w for i in range(h)], w, h, n)
        if moves is not None:
            for move in moves:
                slow_board.add_token(move)
        fast_brd = fast_board.FastBoard(slow_board)
        print(f"    Nested list: {timeit.timeit(slow_board.get_outcome, number=10000)}")
        # print(f"    Array manual: {timeit.timeit(fast_board.get_outcome, number=10000)}")
        print(f"    Array convolution: {timeit.timeit(fast_brd.get_outcome_convolution, number=10000)}")

    def test_fast_outcome(self):
        """
        Checks fast_board will evaluate the winner
        :return:
        """
        w = 7
        h = 6
        n = 4
        slow_board = board.Board([[0] * w for i in range(h)], w, h, n)
        moves = [3, 2, 3, 2, 3, 1, 3, 2, 5, 6, 5, 5, 1, 3, 2, 2]
        for move in moves:
            slow_board.add_token(move)

        fast_brd = fast_board.FastBoard(slow_board)
        sol = fast_brd.get_outcome_convolution()
        print(sol)
        self.assertTrue(sol > 60)

    def test_outcome_time(self):
        self.time_outcome(7, 6, 4)
        self.time_outcome(10, 8, 4)
        self.time_outcome(7, 6, 5)
        self.time_outcome(10, 8, 5)
        print("\n- Semi-Populated -")
        starting = [3, 3, 3, 3, 3, 2, 5, 6, 5, 5, 3, 2, 2]
        self.time_outcome(7, 6, 4, starting)
        self.time_outcome(10, 8, 4, starting)
        self.time_outcome(7, 6, 5, starting)
        self.time_outcome(10, 8, 5, starting)
        print("\n- Highly Populated -")
        starting = [3, 3, 3, 3, 3, 2, 5, 6, 5, 5, 3, 2, 2, 5, 6, 2, 2, 0, 6, 6, 5, 1, 6, 4, 0, 0, 0, 0, 0]
        self.time_outcome(7, 6, 4, starting)
        self.time_outcome(10, 8, 4, starting)
        self.time_outcome(7, 6, 5, starting)
        self.time_outcome(10, 8, 5, starting)


if __name__ == '__main__':
    unittest.main()
