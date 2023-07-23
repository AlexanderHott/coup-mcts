from game_state import Card, Action


class Player:
    def __init__(self, hand: list[Card] | None = None, coins: int = 2):
        if hand is None:
            self.hand = []
        else:
            self.hand = hand

        self.face_up = []
        self.coins = coins

    def ask_action(self, legal_actions: list[Action]) -> Action:
        if len(legal_actions) == 1:
            return legal_actions[0]

        print(legal_actions)
        i = int(input("Select action index"))
        return legal_actions[i]
