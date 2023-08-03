from random import shuffle
import copy
from dataclasses import dataclass

from coup.player import Player
from coup.action import Card, Action

Cuid2 = str


class Game:
    def __init__(self, players: list[Player]) -> None:
        self.players = players
        self.current_player_idx = 0
        self.perfect_game_states: list["GameState"] = []

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

    def play(self):
        self.perfect_game_states.append(GameState.from_game_perfect(self))
        while self.is_over() is None:
            for i, player in enumerate(self.players):
                [print(player) for player in self.players]
                [print(s) for s in self.perfect_game_states]
                self.current_player_idx = i
                # self.player_game_states[player.id].append(
                #     GameState.for_player(self, player)
                # )

                action = player.ask_action(self.get_legal_actions(player))

                print("pre ")
                self.update_gamestate(action, self.current_player_idx)
                print("players coins", self.players[i].coins)

                # Ask to
                highest_action = Action.NOTHING
                for p in self.players:
                    if player == p:
                        continue

                    res = p.ask_action(self.get_legal_actions(p, action))
                    if res == Action.NOTHING:
                        continue

                    highest_action = res
                    break

                self.update_gamestate(highest_action, self.current_player_idx)

    def update_gamestate(self, action: Action, player_idx: int):
        state = copy.deepcopy(
            self.perfect_game_states[-1]
            if len(self.perfect_game_states)
            else GameState.from_game_perfect(self, action)
        )
        state.current_player = player_idx
        print(f"Updating state: p: {state.last_action} c: {action}")

        if state.last_action == Action.NOTHING:
            state.last_action = action
        # if state.last_action == Action.NOTHING and action == Action.INCOME:
        #     state.last_action = action
        # elif state.last_action == Action.NOTHING and action == Action.STEAL:
        #     state.last_action = action
        # elif state.last_action == Action.NOTHING and action == Action.TAX:
        #     ...

        if state.last_action == Action.INCOME and action == Action.NOTHING:
            self.players[player_idx].coins += 1
            state.last_action = action
            state.players[player_idx].coins += 1

        elif state.last_action == Action.TAX and action == Action.NOTHING:
            print(
                "taxing"
            )
            self.players[player_idx].coins += 3
            state.last_action = action
            state.players[player_idx].coins += 3

        elif state.last_action == Action.COUP and action == Action.NOTHING:
            other_player_idx = 0 if player_idx == 1 else 1
            self.players[other_player_idx].lose_influence()
            ...


        elif state.last_action == Action.STEAL and action == Action.BLOCK_STEAL:
            ...

        self.perfect_game_states.append(state)
        # return state

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


@dataclass
class PlayerState:
    hand: list[int]
    dead: list[int]
    coins: int

    @staticmethod
    def from_player_perfect(player: Player) -> "PlayerState":
        hand = list(map(lambda c: c.value, player.hand))
        while len(hand) > 2:
            hand.append(Card.EMPTY.value)

        dead = list(map(lambda c: c.value, player.dead))
        while len(dead) > 2:
            dead.append(Card.EMPTY.value)

        return PlayerState(hand=hand, dead=dead, coins=player.coins)

    @staticmethod
    def from_player_blind(player: Player) -> "PlayerState":
        hand = list(map(lambda _: Card.UNKNOWN.value, player.hand))
        while len(hand) > 2:
            hand.append(Card.EMPTY.value)

        dead = list(map(lambda _: Card.UNKNOWN.value, player.hand))
        while len(dead) > 2:
            dead.append(Card.EMPTY.value)

        return PlayerState(hand=hand, dead=dead, coins=player.coins)


@dataclass
class GameState:
    players: list[PlayerState]
    current_player: int
    last_action: Action

    @staticmethod
    def from_game_perfect(
        game: Game, last_action: Action = Action.NOTHING
    ) -> "GameState":
        player_states = []
        for player in game.players:
            player_states.append(PlayerState.from_player_perfect(player))

        return GameState(
            players=player_states,
            current_player=game.current_player_idx,
            last_action=last_action,
        )

    @staticmethod
    def for_player(game: Game, player: Player, last_action: Action) -> "GameState":
        player_states = []
        for p in game.players:
            if p == player:
                player_states.append(PlayerState.from_player_perfect(player))
            else:
                player_states.append(PlayerState.from_player_blind(player))

        return GameState(
            players=player_states,
            current_player=game.current_player_idx,
            last_action=last_action,
        )
