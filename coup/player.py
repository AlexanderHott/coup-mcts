from typing import Protocol
import logging
import random

from coup.action import Card, Action

from cuid2 import cuid_wrapper

id_generator = cuid_wrapper()


class Player(Protocol):
    def ask_action(self, legal_actions: list[Action]) -> Action:
        ...

    def reset(self):
        ...

    @property
    def hand(self) -> list[Card]:
        ...

    @hand.setter
    def hand(self, cards: list[Card]):
        ...

    @property
    def dead(self) -> list[Card]:
        ...

    @dead.setter
    def dead(self, cards: list[Card]):
        ...

    @property
    def coins(self) -> int:
        ...

    @coins.setter
    def coins(self, amount: int):
        ...

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(coins={self.coins}, hand={self.hand}, dead={self.dead})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(coins={self.coins}, hand={self.hand}, dead={self.dead})"


class RandomPlayer:
    def __init__(self, hand: list[Card] | None = None, coins: int = 2):
        if hand is None:
            self.hand = []
        else:
            self.hand = hand

        self.dead = []
        self.coins = coins
        self.id = id_generator()

    def reset(self):
        self.hand = []
        self.dead = []
        self.coins = 2

    def ask_action(self, legal_actions: list[Action]) -> Action:
        action = random.choice(legal_actions)
        logging.debug(f"Random action: {action}")
        return action

    def __str__(self) -> str:
        return f"""\
{self.__class__.__name__}(
    coins={self.coins},
    hand={self.hand},
    dead={self.dead}
)"""

    def __repr__(self) -> str:
        return f"""\
{self.__class__.__name__}(
    coins={self.coins},
    hand={self.hand},
    dead={self.dead}
)"""


class CliPlayer:
    def __init__(self, hand: list[Card] | None = None, coins: int = 2):
        if hand is None:
            self.hand = []
        else:
            self.hand = hand

        self.dead = []
        self.coins = coins
        self.id = id_generator()

    def reset(self):
        self.hand = []
        self.dead = []
        self.coins = 2

    def ask_action(self, legal_actions: list[Action]) -> Action:
        if len(legal_actions) == 1:
            return legal_actions[0]

        for i in range(len(legal_actions)):
            logging.info(f"{i}: {legal_actions[i].name}")

        selection = int(input("Select action index: "))
        return legal_actions[selection]

    def __str__(self) -> str:
        return f"""\
{self.__class__.__name__}(
    coins={self.coins},
    hand={self.hand},
    dead={self.dead}
)"""

    def __repr__(self) -> str:
        return f"""\
{self.__class__.__name__}(
    coins={self.coins},
    hand={self.hand},
    dead={self.dead}
)"""
