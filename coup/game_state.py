from enum import Enum
from dataclasses import dataclass
from player import Player


class Action(Enum):
    NOTHING = 0
    INCOME = 1
    FORIGN_AID = 2
    TAX = 3
    STEAL = 4
    ASSASSINATE = 5
    EXCHANGE = 6
    COUP = 7

    BLOCK_FORIGN_AID = 8
    BLOCK_STEAL = 9
    BLOCK_ASSASSINATE = 10

    CHALLENGE_TAX = 11
    CHALLENGE_STEAL = 12
    CHALLENGE_ASSASSINATE = 13
    CHALLENGE_EXCHANGE = 14

    CHALLENGE_BLOCK_FORIGN_AID = 15
    CHALLENGE_BLOCK_STEAL = 16
    CHALLENGE_BLOCK_ASSASSINATE = 17

class Card(Enum):
    EMPTY = 0
    UNKNOWN = 1
    DUKE = 2
    CAPTIAN = 3
    ASSASSIN = 4
    CONTESSA = 5
    AMBASSADOR = 6

@dataclass
class GameState:
    players: list[Player]
    active_player: Player
    revealed_deck: list[Card]


