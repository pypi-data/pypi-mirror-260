import math
from typing import Dict, List, Self


class Perceptron:

    def __init__(self, coef: float, deg: float = None, name=None):

        self.coef = coef
        self.deg = deg
        self.name = name

        self.perceptronsRHS: List[Self] = []
        self.perceptronsLHS: List[Self] = []

        self.activation: Dict[Self, float] = {}
        self.propagation: Dict[Self, float] = {}

        self.q = 0

    def connectRHS(self, perceptronRHS: Self):
        if perceptronRHS not in self.perceptronsRHS:
            self.perceptronsRHS.append(perceptronRHS)

        if self not in perceptronRHS.perceptronsLHS:
            perceptronRHS.connectLHS(self)

    def connectLHS(self, perceptronLHS: Self):
        if perceptronLHS not in self.perceptronsLHS:
            self.perceptronsLHS.append(perceptronLHS)

        if self not in perceptronLHS.perceptronsRHS:
            perceptronLHS.connectRHS(self)

    def disconnectRHS(self, perceptronRHS: Self):
        if perceptronRHS in self.perceptronsRHS:
            self.perceptronsRHS.remove(perceptronRHS)

        if self in perceptronRHS.perceptronsLHS:
            perceptronRHS.disconnectLHS(self)

        if len(self.perceptronsRHS) == 0:
            for perceptron in self.perceptronsLHS:
                perceptron.disconnectRHS(self)

    def disconnectLHS(self, perceptronLHS: Self):
        if perceptronLHS in self.perceptronsLHS:
            self.perceptronsLHS.remove(perceptronLHS)

        if self in perceptronLHS.perceptronsRHS:
            perceptronLHS.disconnectRHS(self)

        if len(self.perceptronsLHS) == 0:
            for perceptron in self.perceptronsRHS:
                perceptron.disconnectLHS(self)

    def activate(self, t: float, p: Self = None):
        self.activation.update({p: self.coef * t**self.deg})
        if len(self.perceptronsLHS) == 0 or len(self.activation) == len(self.perceptronsLHS):
            self.q = sum(self.activation.values())
            for perceptron in self.perceptronsRHS:
                perceptron.activate(self.q, self)
            self.activation = {}

    def propagate(self, t: float, p: Self = None):
        self.propagation.update({p: t})
        if len(self.perceptronsRHS) == 0 or len(self.propagation) == len(self.perceptronsRHS):
            for error in self.propagation.values():
                self.coef = self.coef - (error * 1e-7)
            for p in self.perceptronsLHS:
                if p.q > 0 and error > 0 or p.q < 0 and error < 0:
                    p.propagate(error, self)
                else:
                    p.propagate(math.copysign(1, error), self)
            self.propagation = {}
