from coup.game import Game
from coup.player import CliPlayer, RandomPlayer
import logging

if __name__ == "__main__":
    # p1 = CliPlayer()
    # p2 = CliPlayer()
    logging.getLogger().setLevel(logging.DEBUG)
    p1_wins: list[bool] = []
    # game = Game([p1, p2])
    # print(game.play())
    p1 = RandomPlayer()
    p2 = RandomPlayer()
    for _ in range(5000):
        p1.reset()
        p2.reset()
        game = Game([p1, p2])
        winner = game.play()
        p1_wins.append(winner == p1)

    print(p1_wins.count(True) / len(p1_wins))
