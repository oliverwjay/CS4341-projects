import unittest
import timeit
import fast_board
import board
import matplotlib.pyplot as plt


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
        slow_board_time = timeit.timeit(slow_board.get_outcome, number=10000)
        # print(f"    Array manual: {timeit.timeit(fast_board.get_outcome, number=10000)}")
        print(f"    Array convolution: {timeit.timeit(fast_brd.get_outcome_convolution, number=10000)}")
        fast_board_time = timeit.timeit(fast_brd.get_outcome_convolution, number=10000)

        return slow_board_time, fast_board_time

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
        time_result11 = self.time_outcome(7, 6, 4)
        time_result12 = self.time_outcome(10, 8, 4)
        time_result13 = self.time_outcome(7, 6, 5)
        time_result14 = self.time_outcome(10, 8, 5)
        time_result_int = ((time_result11[0] + time_result12[0] + time_result13[0] + time_result14[0]) / 4)
        time_result_int1 = ((time_result11[1] + time_result12[1] + time_result13[1] + time_result14[1]) / 4)
        time_result1 = (time_result_int, time_result_int1)
        print(time_result1)
        print("\n- Semi-Populated -")
        starting = [3, 3, 3, 3, 3, 2, 5, 6, 5, 5, 3, 2, 2]
        time_result21 = self.time_outcome(7, 6, 4, starting)
        time_result22 = self.time_outcome(10, 8, 4, starting)
        time_result23 = self.time_outcome(7, 6, 5, starting)
        time_result24 = self.time_outcome(10, 8, 5, starting)
        time_result_int = ((time_result21[0] + time_result22[0] + time_result23[0] + time_result24[0]) / 4)
        time_result_int1 = ((time_result21[1] + time_result22[1] + time_result23[1] + time_result24[1]) / 4)
        time_result2 = (time_result_int, time_result_int1)

        print("\n- Highly Populated -")
        starting = [3, 3, 3, 3, 3, 2, 5, 6, 5, 5, 3, 2, 2, 5, 6, 2, 2, 0, 6, 6, 5, 1, 6, 4, 0, 0, 0, 0, 0]
        time_result31 = self.time_outcome(7, 6, 4, starting)
        time_result32 = self.time_outcome(10, 8, 4, starting)
        time_result33 = self.time_outcome(7, 6, 5, starting)
        time_result34 = self.time_outcome(10, 8, 5, starting)
        time_result_int = ((time_result31[0] + time_result32[0] + time_result33[0] + time_result34[0]) / 4)
        time_result_int1 = ((time_result31[1] + time_result32[1] + time_result33[1] + time_result34[1]) / 4)
        time_result3 = (time_result_int, time_result_int1)

        # slow_thyme = [time_result1[0], time_result2[0], time_result3[0]]
        # fast_thyme = [time_result1[1], time_result2[1], time_result3[1]]

        plt.plot([time_result1, time_result2, time_result3])
        plt.ylabel("Time (seconds)")
        plt.show()


if __name__ == '__main__':
    unittest.main()
