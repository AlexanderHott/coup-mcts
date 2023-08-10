from typing import Protocol
import logging
from random import choice

from coup.action import Card, Action

from cuid2 import cuid_wrapper

id_generator = cuid_wrapper()


class Player(Protocol):
    def ask_action(self, legal_actions: list[Action]) -> Action:
        ...

    def lose_influence(self):
        ...

    def reset(self):
        ...

    def __str__(self) -> str:
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


class RandomPlayer:
    def __init__(self, hand: list[Card] | None = None, coins: int = 2):
        if hand is None:
            self.hand = []
        else:
            self.hand = hand

        self.dead = [Card.EMPTY, Card.EMPTY]
        self.coins = coins
        self.id = id_generator()

    def reset(self):
        self.hand = []
        self.dead = [Card.EMPTY, Card.EMPTY]
        self.coins = 2

    def ask_action(self, legal_actions: list[Action]) -> Action:
        return choice(legal_actions)

    def lose_influence(self):
        alive_cards = list(filter(lambda c: c != Card.EMPTY, self.hand))
        selection = choice(alive_cards)

        self.hand.remove(selection)
        self.hand.append(Card.EMPTY)
        self.dead.remove(Card.EMPTY)
        self.dead.append(selection)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(hand={self.hand}, coins={self.coins})"


class CliPlayer:
    def __init__(self, hand: list[Card] | None = None, coins: int = 2):
        if hand is None:
            self.hand = []
        else:
            self.hand = hand

        self.dead = [Card.EMPTY, Card.EMPTY]
        self.coins = coins
        self.id = id_generator()

    def reset(self):
        self.hand = []
        self.dead = [Card.EMPTY, Card.EMPTY]
        self.coins = 2

    def ask_action(self, legal_actions: list[Action]) -> Action:
        if len(legal_actions) == 1:
            return legal_actions[0]

        for i in range(len(legal_actions)):
            logging.info(f"{i}: {legal_actions[i].name}")

        selection = int(input("Select action index: "))
        return legal_actions[selection]

    def lose_influence(self):
        alive_cards = list(filter(lambda c: c != Card.EMPTY, self.hand))
        if len(alive_cards) == 1:
            self.hand.remove(alive_cards[0])
            self.hand.append(Card.EMPTY)
            self.dead.remove(Card.EMPTY)
            self.dead.append(alive_cards[0])
            return

        for i in range(len(alive_cards)):
            logging.info(f"{i}: {alive_cards[i].name}")

        selection = int(input("Select card index (to lose): "))

        self.dead.append(alive_cards[selection])
        self.dead.remove(Card.EMPTY)
        self.hand.pop(selection)
        self.hand.append(Card.EMPTY)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(hand={self.hand}, coins={self.coins})"
