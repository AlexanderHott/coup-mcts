"""Monte Carlo Tree Search algorithm

https://www.harrycodes.com/blog/monte-carlo-tree-search
"""
import math
import copy
import random
import time
import logging

from coup.action import Action, Card
from coup.game import Game

EXPLORATION = math.sqrt(2)


class Node:
    def __init__(self, action: Action, parent: "Node | None" = None):
        self.action = action
        self.parent = parent
        self.N: int = 0  # number of times selected
        self.Q: int = 0  # number of child outcomes that are winning

        self.children: dict[Action, "Node"] = {}

    def add_children(self, children: list["Node"]):
        for child in children:
            self.children[child.action] = child

    def value(self, explore: float = EXPLORATION) -> float:
        """UCT value of node.

        https://en.wikipedia.org//wiki/Monte_Carlo_tree_search#Exploration_and_exploitation
        """
        if self.N == 0:
            return float("inf")

        return (self.Q / self.N) + explore * math.sqrt(
            math.log(self.parent.N if self.parent else 0) / self.N
        )

    def __str__(self) -> str:
        return f"""\
{self.__class__.__name__}(
    action={self.action},
    N={self.N}
    Q={self.Q}
)"""

    def __repr__(self) -> str:
        return f"""\
{self.__class__.__name__}(
    action={self.action},
    N={self.N}
    Q={self.Q}
)"""


class MCTS:
    def __init__(self, game: Game):
        self.root_game = copy.deepcopy(game)
        self.root = Node(Action.NOTHING)

    def select_node(self) -> tuple[Node, Game]:
        node = self.root
        game = copy.deepcopy(self.root_game)

        while len(node.children) != 0:
            children = node.children.values()
            max_val = max(children, key=lambda n: n.value()).value()
            max_nodes = [n for n in children if n.value() == max_val]

            node = random.choice(max_nodes)
            self.move(node.action)

            if node.N == 0:
                return node, game

        if self.expand(node, game):
            node = random.choice(list(node.children.values()))
            self.move(node.action)

        return node, game

    def expand(self, parent: Node, game: Game) -> bool:
        if game.is_over() is None:
            return False

        children = [Node(move, parent) for move in game.get_legal_actions()]
        parent.add_children(children)

        return True

    def roll_out(self, game: Game) -> int:
        while (winner := game.is_over()) is None:
            legal_actions = game.get_legal_actions()

            action = random.choice(legal_actions)
            logging.debug(f"Random action: {action}")
            game.handle_action(action)

            highest_action = Action.NOTHING
            for j in range(len(game.players)):
                if game.current_player_idx == j:
                    continue

                res = random.choice(game.get_legal_actions())
                if res == Action.NOTHING:
                    continue

                highest_action = res
                break

            game.handle_action(highest_action)

            # game.current_player_idx = game.other_player_idx

        return winner

    def back_propagate(self, node: Node | None, turn: int, outcome: int) -> None:
        reward = 0 if outcome == turn else 1

        while node is not None:
            node.N += 1
            node.Q += reward
            node = node.parent

            if outcome == 0:
                reward = 0
            else:
                reward = 1 - reward

    def search(self, time_limit: int) -> None:
        logging.debug(f"Searching for {time_limit}s")
        start = time.process_time()

        num_rollouts = 0
        for action in self.root_game.get_legal_actions():
            self.root.children[action] = Node(action, self.root)

        # while time.process_time() - start < time_limit:
        while num_rollouts < 100:
            node, game = self.select_node()
            logging.debug(f"{node=}\n{game=}")
            outcome = self.roll_out(game)
            self.back_propagate(node, game.other_player_idx, outcome)
            num_rollouts += 1

        run_time = time.process_time() - start
        logging.info(f"Runtime: {run_time}, {num_rollouts=}")

    def best_move(self) -> Action | None:
        if self.root_game.is_over() is not None:
            return None

        logging.debug(self.root)
        logging.debug(self.root.children)
        max_value = max(self.root.children.values(), key=lambda n: n.N).N
        max_nodes = [n for n in self.root.children.values() if n.N == max_value]

        best_child = random.choice(max_nodes)
        return best_child.action

    def handle_action(self, action: Action):
        self.root_game.handle_action(action)

        if action in self.root.children.keys():
            self.root = self.root.children[action]
        else:
            self.root = Node(Action.NOTHING, None)


    def _do_everything(self):

        for action in self.root_game.get_legal_actions():
            self.root.children[action] = Node(action, self.root)

        start = time.process_time()
        # while start + 5 > time.process_time():
        for _ in range(500):
            # Select
            node = self.root
            game = copy.deepcopy(self.root_game)
            # while there are still leaves
            while len(node.children) != 0:
                if game.is_over() is not None:
                    print("ahh")
                    ...
                # Select best uct leaf node, starting with the root
                children = node.children.values()
                max_val = max(children, key=lambda n: n.value()).value()
                max_nodes = [n for n in children if n.value() == max_val]
                if len(max_nodes) == 0:
                    print("aah")

                node = random.choice(max_nodes)
                game.handle_action(node.action)
            if (outcome := game.is_over()) is None:

                # Expand
                # add a child node to the selected node
                legal_actions = game.get_legal_actions()

                for action in legal_actions:
                    node.children[action] = Node(action, node)

                node = random.choice(list(node.children.values()))
                game.handle_action(node.action)

                # Simulate
                # simulate a game
                outcome = self.roll_out(game)

            # Back prop
            # backpropigate the values
            self.back_propagate(node, game.current_player_idx, outcome)


class MCTSPlayer:
    def __init__(self, mcts: MCTS | None = None):
        self.hand: list[Card] = []
        self.dead: list[Card] = []
        self.coins: int = 0
        self.mcts = mcts

    def ask_action(self, legal_actions: list[Action]) -> Action:
        if not self.mcts:
            raise ValueError("No mcts")

        self.mcts.search(1)

        best_move = self.mcts.best_move()
        if best_move is None:
            raise ValueError("Game over")
        return best_move

    def reset(self):
        self.hand = []
        self.dead = []
        self.coins = 2

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
