from random import shuffle

from player import Player
from game_state import Card, GameState, Action


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
            action = player.ask_action(self.get_legal_actions(player))
            # new_state = self.update(action)

            for p in self.players:
                if player == p:
                    continue

                res = p.ask_action(self.get_legal_actions(p, action))
                if res == Action.NOTHING:
                    continue

                ...

    def update(self, action: Action) -> GameState:
        ...

    def get_legal_actions(
        self, player: Player, prev_action: Action = Action.NOTHING
    ) -> list[Action]:
        # Player's turn
        if prev_action == Action.NOTHING:
            if player.coins >= 10:
                return [Action.COUP]

            actions = [
                Action.INCOME,
                Action.FORIGN_AID,
                Action.TAX,
                Action.STEAL,
                Action.EXCHANGE,
            ]

            if player.coins >= 7:
                actions.append(Action.COUP)
            if player.coins >= 3:
                actions.append(Action.ASSASSINATE)

            return actions
        
        # Response
        if prev_action == Action.INCOME:
            return [Action.NOTHING]
        elif prev_action == Action.COUP:
            return [Action.NOTHING]

        elif prev_action == Action.FORIGN_AID:
            return [Action.NOTHING, Action.BLOCK_FORIGN_AID]
        elif prev_action == Action.TAX:
            return [Action.NOTHING, Action.CHALLENGE_TAX]
        elif prev_action == Action.STEAL:
            return [Action.NOTHING, Action.BLOCK_STEAL, Action.CHALLENGE_STEAL]
        elif prev_action == Action.ASSASSINATE:
            return [
                Action.NOTHING,
                Action.BLOCK_ASSASSINATE,
                Action.CHALLENGE_ASSASSINATE,
            ]
        elif prev_action == Action.EXCHANGE:
            return [Action.NOTHING, Action.CHALLENGE_EXCHANGE]

        elif prev_action == Action.BLOCK_FORIGN_AID:
            return [Action.NOTHING, Action.CHALLENGE_BLOCK_FORIGN_AID]
        elif prev_action == Action.BLOCK_STEAL:
            return [Action.NOTHING, Action.CHALLENGE_BLOCK_STEAL]
        elif prev_action == Action.BLOCK_ASSASSINATE:
            return [Action.NOTHING, Action.CHALLENGE_BLOCK_ASSASSINATE]

        raise ValueError(f"{prev_action} does not have any valid responses")
