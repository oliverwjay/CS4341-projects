Group 26 ConnectN

Requires modules numpy and scipy for matrix convolutions

Run different agents for different size boards:

# 7x6 Agent
THE_AGENT = AlphaBetaAgent("Group26", 6, auto_depth=True)

# 10x8 Agent
THE_AGENT = AlphaBetaAgent("Group26", 5, auto_depth=True)