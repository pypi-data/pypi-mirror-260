from typing import List, Self

from neuralplex.perceptron import Perceptron


class Layer:

    def __init__(self, perceptrons: List[Perceptron], deg: float = None):
        self.perceptrons = perceptrons
        self.deg = deg

        if not self.deg is None:
            for perceptron in self.perceptrons:
                if perceptron.deg is None:
                    perceptron.deg = self.deg

    def connect(self, layer: Self):
        for p1 in self.perceptrons:
            for p2 in layer.perceptrons:
                p1.connectRHS(p2)
