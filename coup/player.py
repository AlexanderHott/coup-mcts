from coup.action import Card, Action

from cuid2 import cuid_wrapper

id_generator = cuid_wrapper()


class Player:
    def __init__(self, hand: list[Card] | None = None, coins: int = 2):
        if hand is None:
            self.hand = []
        else:
            self.hand = hand

        self.dead = [Card.EMPTY, Card.EMPTY]
        self.coins = coins
        self.id = id_generator()

    def ask_action(self, legal_actions: list[Action]) -> Action:
        if len(legal_actions) == 1:
            return legal_actions[0]

        for i in range(len(legal_actions)):
            print(f"{i}: {legal_actions[i].name}")

        selection = int(input("Select action index: "))
        return legal_actions[selection]

    def lose_influence(self):
        if len(self.hand) == 1:
            return self.hand[0]

        for i in range(len(self.hand)):
            print(f"{i}: {self.hand[i].name}")

        selection = int(input("Select card index (to lose): "))

        self.dead.append(self.hand[selection])
        self.dead.remove(Card.EMPTY)
        self.hand.pop(selection)
        self.hand.append(Card.EMPTY)
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(hand={self.hand}, coins={self.coins})"
