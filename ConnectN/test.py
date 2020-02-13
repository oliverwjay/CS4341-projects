import unittest
from Group26 import alpha_beta_agent
import board
import time
import matplotlib.pyplot as plt


class MyTestCase(unittest.TestCase):

    def test_terminal_test(self):
        """
        Tests the terminal test function in alpha_beta_agent
        :return: void
        """

        fail_board = [[1, 2, 2, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]
                      ]

        pass_board = [[1, 2, 2, 1],
                      [1, 0, 0, 0],
                      [1, 0, 0, 0],
                      [0, 0, 0, 0]
                      ]

        tie_board = [[1, 2, 1, 2],
                     [1, 2, 1, 2],
                     [2, 1, 2, 1],
                     [2, 1, 2, 1]
                     ]

        ab_agent = alpha_beta_agent.AlphaBetaAgent("TestTerminalTestAgent", 3)

        fail_brd = board.Board(fail_board, 4, 4, 3)
        pass_brd = board.Board(pass_board, 4, 4, 3)
        tie_brd = board.Board(tie_board, 4, 4, 3)

        # Assert Statements
        # Tests if brd1 is not a terminal node
        self.assertEqual(ab_agent.terminal_test(fail_brd), False)
        # Tests if three in a row ends the game
        self.assertEqual(ab_agent.terminal_test(pass_brd), True)
        # Tests if a tie works
        self.assertEqual(ab_agent.terminal_test(tie_brd), True)

    def test_get_open_spaces(self):
        """
        Test the get open spaces in alpha beta agent
        :return: void
        """
        full_board = [[1, 2, 2, 1],
                      [1, 2, 1, 1],
                      [1, 2, 1, 1],
                      [1, 2, 1, 1]
                      ]

        check_board = [[1, 2, 2, 0],
                       [0, 2, 1, 0],
                       [0, 2, 0, 0],
                       [0, 0, 0, 0]
                       ]
        ab_agent = alpha_beta_agent.AlphaBetaAgent("TestGetOpenSpaces", 3)

        test_brd = board.Board(full_board, 4, 4, 3)
        check_brd = board.Board(check_board, 4, 4, 3)

        self.assertEqual(set(), ab_agent.get_open_spaces(test_brd))
        self.assertEqual({(0, 1), (1, 3), (2, 2), (3, 0)}, ab_agent.get_open_spaces(check_brd))

    def test_evaluate(self):
        """
        Tests the evaluate function in alpha beta agent
        :return: void
        """
        test_board = [[1, 2, 2, 2, 0],
                      [1, 1, 1, 2, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]
                      ]

        ab_agent = alpha_beta_agent.AlphaBetaAgent("TestEvaluate", 3)

        test_brd = board.Board(test_board, 5, 5, 4)
        # test_brd.is_any_line_poss()

        # print(ab_agent.evaluate(test_brd))

    def test_double_lookahead(self):
        """
        Tests scenario where opponent wins two moves out
        :return:
        """
        ab_agent = alpha_beta_agent.AlphaBetaAgent("Test Foresight", 2)

        test_board = [[0, 0, 2, 2, 0, 0, 0],
                      [0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0]
                      ]
        test_brd = board.Board(test_board, 7, 5, 4)

        move = ab_agent.go(test_brd)

        self.assertEqual(1, move)

    def test_move_speed(self):
        test_board = [[1, 2, 2, 2, 0],
                      [1, 1, 1, 2, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]
                      ]

        ab_agent = alpha_beta_agent.AlphaBetaAgent("TestEvaluate", 3)

        test_brd = board.Board(test_board, 5, 5, 4)

        st = time.time()
        ab_agent.go(test_brd)
        et = time.time() - st

        print(et)

    def time_outcome(self, brd, w, h, n, aba):
        """
        Times how long it takes to evaluate a given board 10000 times and prints the results
        :param w: Board width
        :param h: Board height
        :param n: Number in a row needed to win
        :param brd: the board
        :param aba: the alpha beta agent
        :return: None
        """
        print(f"\nSize: {(w, h)} n: {n}")
        # fast_brd = fast_board.FastBoard(brd)
        start = time.time()
        aba.go(brd)
        total = time.time() - start
        print(total)
        return total

    def test_outcome_time(self):
        arr = []
        for i in range(0, 8):
            ab_agent = alpha_beta_agent.AlphaBetaAgent("TestEvaluate", i)
            blank_board_6x7 = [[0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0]
                               ]

            semi_board_6x7 = [[1, 0, 2, 1, 1, 2, 0],
                              [2, 0, 1, 0, 2, 1, 0],
                              [1, 0, 1, 0, 1, 0, 0],
                              [0, 0, 2, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0]
                              ]

            filled_board_6x7 = [[1, 1, 2, 1, 1, 2, 1],
                                [2, 2, 1, 2, 2, 1, 2],
                                [1, 2, 1, 1, 1, 2, 1],
                                [1, 1, 2, 2, 2, 1, 2],
                                [2, 0, 2, 1, 1, 2, 1],
                                [1, 0, 2, 2, 2, 1, 2]
                                ]

            blank_board_10x8 = [[0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0]
                                ]

            semi_board_10x8 = [[1, 1, 2, 1, 1, 0, 2, 1],
                               [2, 1, 1, 2, 2, 0, 1, 2],
                               [1, 2, 0, 2, 1, 0, 2, 1],
                               [0, 2, 0, 2, 2, 0, 2, 1],
                               [0, 1, 0, 1, 2, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0]
                               ]

            filled_board_10x8 = [[1, 1, 2, 1, 1, 2, 2, 1],
                                 [2, 1, 1, 1, 2, 2, 1, 2],
                                 [1, 2, 2, 2, 1, 2, 1, 1],
                                 [2, 2, 1, 2, 2, 1, 2, 1],
                                 [1, 1, 2, 1, 2, 2, 2, 1],
                                 [2, 2, 1, 2, 2, 1, 1, 2],
                                 [1, 1, 2, 1, 1, 2, 2, 1],
                                 [2, 1, 1, 1, 2, 1, 1, 2],
                                 [1, 2, 2, 2, 1, 2, 2, 0],
                                 [1, 2, 1, 2, 1, 1, 2, 0],
                                 ]

            blank_brd_6x7_4 = board.Board(blank_board_6x7, 7, 6, 4)
            blank_brd_6x7_5 = board.Board(blank_board_6x7, 7, 6, 5)

            semi_brd_6x7_4 = board.Board(semi_board_6x7, 7, 6, 4)
            semi_brd_6x7_5 = board.Board(semi_board_6x7, 7, 6, 5)

            filled_brd_6x7_4 = board.Board(filled_board_6x7, 7, 6, 4)
            filled_brd_6x7_5 = board.Board(filled_board_6x7, 7, 6, 5)

            blank_brd_10x8_4 = board.Board(blank_board_10x8, 8, 10, 4)
            blank_brd_10x8_5 = board.Board(blank_board_10x8, 8, 10, 5)

            semi_brd_10x8_4 = board.Board(semi_board_10x8, 8, 10, 4)
            semi_brd_10x8_5 = board.Board(semi_board_10x8, 8, 10, 5)

            filled_brd_10x8_4 = board.Board(filled_board_10x8, 8, 10, 4)
            filled_brd_10x8_5 = board.Board(filled_board_10x8, 8, 10, 5)

            blank = self.time_outcome(blank_brd_6x7_4, 7, 6, 4, ab_agent)
            blank += self.time_outcome(blank_brd_6x7_5, 7, 6, 5, ab_agent)
            blank += self.time_outcome(blank_brd_10x8_4, 8, 10, 4, ab_agent)
            blank += self.time_outcome(blank_brd_10x8_5, 8, 10, 5, ab_agent)

            semi = self.time_outcome(semi_brd_6x7_4, 7, 6, 4, ab_agent)
            semi += self.time_outcome(semi_brd_6x7_5, 7, 6, 5, ab_agent)
            semi += self.time_outcome(semi_brd_10x8_4, 8, 10, 4, ab_agent)
            semi += self.time_outcome(semi_brd_10x8_5, 8, 10, 5, ab_agent)

            full = self.time_outcome(filled_brd_6x7_4, 7, 6, 4, ab_agent)
            full += self.time_outcome(filled_brd_6x7_5, 7, 6, 5, ab_agent)
            full += self.time_outcome(filled_brd_10x8_4, 8, 10, 4, ab_agent)
            full += self.time_outcome(filled_brd_10x8_5, 8, 10, 5, ab_agent)

            print("\n- Not-Populated Average Time-")
            blanks = blank / 4
            print(blanks)
            print("\n- Semi-Populated Average Time -")
            semis = semi / 4
            print(semis)
            print("\n- Highly Populated Average Time-")
            fulls = full / 4
            print(fulls)

            arr.append([blanks, semis, fulls])

        plt.plot(arr)
        plt.title("Time Per Move")
        plt.legend(('Empty Board', 'Partially Filled Board', 'Nearly Filled Board'))
        plt.ylabel("Time (seconds)")
        plt.xlabel("Max Depth")
        plt.show()

        # print(filled_brd_10x8_4.get_outcome())
        # print(filled_brd_6x7_4.get_outcome())
        # print(semi_brd_6x7_4.get_outcome())
        # print(semi_brd_10x8_4.get_outcome())


if __name__ == '__main__':
    unittest.main()
