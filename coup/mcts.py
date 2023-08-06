from coup.action import Action
from coup.game import GameState
import math
import copy
import random

EXPLORATION = math.sqrt(2)


class Node:
    def __init__(self, action: Action, parent: "Node"):
        self.action = action
        self.parent = parent
        self.N = 0  # number of times selected
        self.Q = 0  # number of child outcomes that are winning

        self.children: dict[Action, "Node"] = {}

    def add_children(self, children: list["Node"]):
        for child in children:
            self.children[child.action] = child

    def value(self, explore: float = EXPLORATION) -> float:
        if self.N == 0:
            return 0

        return (self.Q / self.N) + explore * math.sqrt(math.log(self.parent.N) / self.N)


class MCTS:
    def __init__(self, state: GameState):
        self.root_state = copy.deepcopy(state)
        self.root = Node()

    def select_node(self) -> tuple[Node, GameState]:
        node = self.root
        state = copy.deepcopy(self.root_state)

        while len(node.children) != 0:
            children = node.children.values()
            max_val = max(children, key=lambda n: n.value()).value()
            max_nodes = [n for n in children if n.value() == max_val]

            node = random.choice(max_nodes)
            state.move(node.move)
