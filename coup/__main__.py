from coup.game import Game
from coup.player import Player

if __name__ == "__main__":
    p1 = Player()
    p2 = Player()
    game = Game([p1, p2])
    game.play()
