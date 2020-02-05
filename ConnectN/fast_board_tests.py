import unittest
from ConnectN.fast_board import FastBoard
from ConnectN.board import Board
import timeit


class FastBoardTests(unittest.TestCase):
    def time_outcome(self, w, h, n, moves=None):
        print(f"\nSize: {(w, h)} n: {n}")
        slow_board = Board([[0] * w for i in range(h)], w, h, n)
        if moves is not None:
            for move in moves:
                slow_board.add_token(move)
        fast_board = FastBoard(slow_board)
        print(f"    Nested list: {timeit.timeit(slow_board.get_outcome, number=10000)}")
        print(f"    Array manual: {timeit.timeit(fast_board.get_outcome, number=10000)}")
        print(f"    Array convolution: {timeit.timeit(fast_board.get_outcome_convolution, number=10000)}")

    def test_fast_outcome(self):
        w = 7
        h = 6
        n = 4
        slow_board = Board([[0] * w for i in range(h)], w, h, n)
        fast_board = FastBoard(slow_board)
        for i in range(10000):
            sol = fast_board.get_outcome_convolution()
        self.assertEqual(sol, None)

    def test_outcome_time(self):
        self.time_outcome(7, 6, 4)
        self.time_outcome(10, 8, 4)
        self.time_outcome(7, 6, 5)
        self.time_outcome(10, 8, 5)
        print("\n- Populated -")
        starting = [4,4,5,4,3,0,5,3,1,2,3,5,2]
        self.time_outcome(7, 6, 4, starting)
        self.time_outcome(10, 8, 4, starting)
        self.time_outcome(7, 6, 5, starting)
        self.time_outcome(10, 8, 5, starting)



if __name__ == '__main__':
    unittest.main()
