from random import shuffle

from player import Player
from game_state import Card, GameState,Action


class Game:
    def __init__(self, players: list[Player]) -> None:
        self.players = players

        self.deck = [
            Card.AMBASSADOR,
            Card.AMBASSADOR,
            Card.AMBASSADOR,
            Card.ASSASSIN,
            Card.ASSASSIN,
            Card.ASSASSIN,
            Card.CAPTIAN,
            Card.CAPTIAN,
            Card.CAPTIAN,
            Card.CONTESSA,
            Card.CONTESSA,
            Card.CONTESSA,
            Card.DUKE,
            Card.DUKE,
            Card.DUKE,
        ]
        shuffle(self.deck)

        for player in self.players:
            player.hand.append(self.deck.pop())
            player.hand.append(self.deck.pop())

            player.coins = 2

    def is_over(self) -> Player | None:
        """Returns the winner if the game is over, None otherwise."""
        alive_players = list(filter(lambda p: len(p.hand) > 0, self.players))
        if len(alive_players) == 1:
            return alive_players[0]
        return None

    def get_perfect_state(self) -> GameState:
        ...

    def get_state(self, player: Player) -> GameState:
        ...

    def play(self):
        for player in self.players:
            action = player.ask_action()
            # new_state = self.update(action)

            for p in self.players:
                if player == p:
                    continue
                
                res = p.ask_response(action)
                if res == Action.NOTHING:
                    continue

                ...
            

    def update(self, action: Action) -> GameState:
        ...

