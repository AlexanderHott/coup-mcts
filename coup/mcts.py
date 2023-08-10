"""Monte Carlo Tree Search algorithm

https://www.harrycodes.com/blog/monte-carlo-tree-search
"""
import math
import copy
import random

from coup.action import Action
from coup.game import Game

EXPLORATION = math.sqrt(2)


class Node:
    def __init__(self, action: Action, parent: "Node" | None = None):
        self.action = action
        self.parent = parent
        self.N: int = 0  # number of times selected
        self.Q: int = 0  # number of child outcomes that are winning

        self.children: dict[Action, "Node"] = {}

    def add_children(self, children: list["Node"]):
        for child in children:
            self.children[child.action] = child

    def value(self, explore: float = EXPLORATION) -> float:
        if self.N == 0:
            return 0

        return (self.Q / self.N) + explore * math.sqrt(
            math.log(self.parent.N if self.parent else 0) / self.N
        )


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
            game.handle_action(node.action)

            if node.N == 0:
                return node, game

        if self.expand(node, game):
            node = random.choice(list(node.children.values()))
            game.handle_action(node.action)

        return node, game

    def expand(self, parent: Node, game: Game) -> bool:
        if game.is_over():
            return False

        children = [Node(move, parent) for move in game.get_legal_actions()]
        parent.add_children(children)

        return True

    def roll_out(self, game: Game) -> int:
        while not (winner := game.is_over()):
            game.handle_action(random.choice(game.get_legal_actions()))

        return winner

    def back_propagate(self, node: Node | None, turn: int, outcome: int) -> None:
        reward = 0 if outcome == turn else 1

        while node is not None:
            node.N += 1
            node.Q += reward
            node = node.parent

            if outcome == 0:
                ...
