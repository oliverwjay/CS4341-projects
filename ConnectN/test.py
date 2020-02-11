import unittest
import agent
import alpha_beta_agent
import board


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



if __name__ == '__main__':
    unittest.main()
