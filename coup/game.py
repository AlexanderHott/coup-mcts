from random import shuffle, randint
import logging

from coup.player import Player
from coup.action import Card, Action

# Cuid2 = str


class Game:
    def __init__(self, players: list[Player]) -> None:
        self.players = players
        self.current_player_idx = 0
        self.prev_action = Action.NOTHING

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

    def __repr__(self) -> str:
        return f"""\
{self.__class__.__name__}(
    current_player_idx={self.current_player_idx},
    prev_action={self.prev_action},
    players={self.players}
)"""

    @property
    def other_player_idx(self) -> int:
        return 0 if self.current_player_idx == 1 else 1

    def is_over(self) -> int | None:
        """Returns the index of the winner if the game is over, None otherwise."""
        alive_players = list(filter(lambda p: len(p.hand) > 0, self.players))
        logging.debug(f"{alive_players=}\ncount: {len(alive_players)}")
        if len(alive_players) == 1:
            return self.players.index(alive_players[0])
        return None

    def play(self) -> int:
        while (winner := self.is_over()) is None:
            for i, player in enumerate(self.players):
                if (winner := self.is_over()) is not None:
                    return winner
                logging.info(f"\nPlayer {i + 1}'s turn\n")
                [logging.debug(player) for player in self.players]
                self.current_player_idx = i

                action = player.ask_action(self.get_legal_actions())
                self.handle_action(action)

                # Ask to block
                highest_action = Action.NOTHING
                for j, p in enumerate(self.players):
                    if i == j:
                        continue

                    res = p.ask_action(self.get_legal_actions())
                    if res == Action.NOTHING:
                        continue

                    highest_action = res
                    break

                self.handle_action(highest_action)

        return winner

    def handle_action(self, action: Action):
        logging.debug(
            f"[+] Updating state [{self.current_player_idx}]: {self.prev_action=} {action=}"
        )
        if self.prev_action == Action.NOTHING:
            ...

        if self.prev_action == Action.INCOME and action == Action.NOTHING:
            self.players[self.current_player_idx].coins += 1
            self.current_player_idx = self.other_player_idx

        elif self.prev_action == Action.TAX and action == Action.NOTHING:
            self.players[self.current_player_idx].coins += 3
            self.current_player_idx = self.other_player_idx

        elif self.prev_action == Action.TAX and action == Action.CHALLENGE_TAX:
            logging.debug("challengin tax")
            player = self.players[self.current_player_idx]
            if Card.DUKE in player.hand:
                logging.debug("challenge failed")
                player.hand.remove(Card.DUKE)
                self.deck.append(Card.DUKE)
                shuffle(self.deck)
                player.hand.append(self.deck.pop())

                other_player = self.players[self.other_player_idx]
                other_player.dead.append(
                    other_player.hand.pop(
                        randint(0, len(self.players[self.other_player_idx].hand) - 1)
                    )
                )

                player.coins += 3
            else:
                logging.debug("challenge succeeded")
                # TODO: player choose card to lose influence
                player.dead.append(player.hand.pop(randint(0, len(player.hand) - 1)))
            self.current_player_idx = self.other_player_idx

        elif self.prev_action == Action.COUP and action == Action.NOTHING:
            self.players[self.current_player_idx].coins -= 7
            other_player = self.players[self.other_player_idx]
            other_player.dead.append(
                other_player.hand.pop(
                    randint(0, len(self.players[self.other_player_idx].hand) - 1)
                )
            )

        self.prev_action = action

    def get_legal_actions(self) -> list[Action]:
        player = self.players[self.current_player_idx]
        # Player's turn
        if (
            self.prev_action == Action.NOTHING
            or self.prev_action == Action.CHALLENGE_TAX
        ):
            if player.coins >= 10:
                return [Action.COUP]

            # actions = [
            #     Action.INCOME,
            #     Action.FORIGN_AID,
            #     Action.TAX,
            #     Action.STEAL,
            #     Action.EXCHANGE,
            # ]
            # TODO: Add back all actions
            actions = [
                Action.INCOME,
                Action.TAX,
            ]

            if player.coins >= 7:
                actions.append(Action.COUP)

            # TODO: Add back all actions
            # if player.coins >= 3:
            #     actions.append(Action.ASSASSINATE)

            return actions

        # Response
        if self.prev_action == Action.INCOME:
            return [Action.NOTHING]
        elif self.prev_action == Action.COUP:
            return [Action.NOTHING]

        elif self.prev_action == Action.FORIGN_AID:
            return [Action.NOTHING, Action.BLOCK_FORIGN_AID]
        elif self.prev_action == Action.TAX:
            return [Action.NOTHING, Action.CHALLENGE_TAX]
        elif self.prev_action == Action.STEAL:
            return [Action.NOTHING, Action.BLOCK_STEAL, Action.CHALLENGE_STEAL]
        elif self.prev_action == Action.ASSASSINATE:
            return [
                Action.NOTHING,
                Action.BLOCK_ASSASSINATE,
                Action.CHALLENGE_ASSASSINATE,
            ]
        elif self.prev_action == Action.EXCHANGE:
            return [Action.NOTHING, Action.CHALLENGE_EXCHANGE]

        elif self.prev_action == Action.BLOCK_FORIGN_AID:
            return [Action.NOTHING, Action.CHALLENGE_BLOCK_FORIGN_AID]
        elif self.prev_action == Action.BLOCK_STEAL:
            return [Action.NOTHING, Action.CHALLENGE_BLOCK_STEAL]
        elif self.prev_action == Action.BLOCK_ASSASSINATE:
            return [Action.NOTHING, Action.CHALLENGE_BLOCK_ASSASSINATE]

        # elif self.prev_action == Action.CHALLENGE_TAX:
        #     return [Action.NOTHING]

        raise ValueError(f"{self.prev_action} does not have any valid responses")
