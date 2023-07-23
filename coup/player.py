from game_state import Card, Action


class Player:
    def __init__(self, hand: list[Card], face_up: list[Card], coins: int):
        self.hand = hand
        self.face_up = face_up
        self.coins = coins

    def get_valid_actions(self) -> list[Action]:
        if self.coins >= 10:
            return [Action.COUP]

        actions = [
            Action.INCOME,
            Action.FORIGN_AID,
            Action.TAX,
            Action.STEAL,
            Action.EXCHANGE,
        ]

        if self.coins >= 7:
            actions.append(Action.COUP)
        if self.coins >= 3:
            actions.append(Action.ASSASSINATE)

        return actions

    def get_valid_response(self, action: Action) -> list[Action]:
        if action == Action.INCOME:
            return [Action.NOTHING]
        elif action == Action.COUP:
            return [Action.NOTHING]

        elif action == Action.FORIGN_AID:
            return [Action.NOTHING, Action.BLOCK_FORIGN_AID]
        elif action == Action.TAX:
            return [Action.NOTHING, Action.CHALLENGE_TAX]
        elif action == Action.STEAL:
            return [Action.NOTHING, Action.BLOCK_STEAL, Action.CHALLENGE_STEAL]
        elif action == Action.ASSASSINATE:
            return [
                Action.NOTHING,
                Action.BLOCK_ASSASSINATE,
                Action.CHALLENGE_ASSASSINATE,
            ]
        elif action == Action.EXCHANGE:
            return [Action.NOTHING, Action.CHALLENGE_EXCHANGE]

        elif action == Action.BLOCK_FORIGN_AID:
            return [Action.NOTHING, Action.CHALLENGE_BLOCK_FORIGN_AID]
        elif action == Action.BLOCK_STEAL:
            return [Action.NOTHING, Action.CHALLENGE_BLOCK_STEAL]
        elif action == Action.BLOCK_ASSASSINATE:
            return [Action.NOTHING, Action.CHALLENGE_BLOCK_ASSASSINATE]

        raise ValueError(f"{action} does not have any valid responses")

    def ask_action(self) -> Action:
        valid_actions = self.get_valid_actions()
        print(valid_actions)
        i = int(input("Select action index"))
        return valid_actions[i]

    def ask_response(self, action: Action) -> Action:
        valid_responses = self.get_valid_response(action)
        
        if len(valid_responses) == 1:
            return valid_responses[0]

        print(valid_responses)
        i = int(input("Select action index"))
        return valid_responses[i]
