from coup.game import Game
from coup.player import CliPlayer, RandomPlayer, Player
from coup.mcts import MCTSPlayer, MCTS
import logging

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    p1: Player = RandomPlayer()
    p2: Player = RandomPlayer()
    game = Game([p1, p2])
    mcts = MCTS(game)
    # mcts.search(2)
    # logging.getLogger().setLevel(logging.DEBUG)

    mcts._do_everything()
    print(mcts.best_move())
    # random = False
    # if not random:
    #     p1 = CliPlayer()
    #     # p2 = CliPlayer()
    #     # p2 = RandomPlayer()
    #     p2 = MCTSPlayer()
    #     game = Game([p1, p2])
    #     p2.mcts = MCTS(game)
    #
    #     print(game.play())
    # else:
    #     p1 = RandomPlayer()
    #     p2 = RandomPlayer()
    #     p1_wins: list[bool] = []
    #     for _ in range(5000):
    #         p1.reset()
    #         p2.reset()
    #         game = Game([p1, p2])
    #         winner = game.play()
    #         p1_wins.append(winner == 0)
    #
    #     print(p1_wins.count(True) / len(p1_wins))
