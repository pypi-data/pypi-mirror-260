from typing import List, Self

from neuralplex.perceptron import Perceptron


class Layer:

    def __init__(self, perceptrons: List[Perceptron], step: float = None):
        self.perceptrons = perceptrons
        self.step = step

        if not self.step is None:
            for perceptron in self.perceptrons:
                if perceptron.step is None:
                    perceptron.step = self.step

    def connect(self, layer: Self) -> None:
        for p1 in self.perceptrons:
            for p2 in layer.perceptrons:
                p1.connectRHS(p2)
