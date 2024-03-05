from typing import Dict, List, Self


class Perceptron:

    def __init__(self, coef: float, deg: float = None, name=None):
        self.coef = coef
        self.deg = deg
        self.name = name
        self.perceptronsRHS: List[Self] = []
        self.perceptronsLHS: List[Self] = []
        self.activations: List[float] = []
        self.propagation: Dict[float] = {}
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

    def activate(self, t: float):
        self.activations.append(self.coef * t**self.deg)
        # print(self.name, len(self.activations))
        if len(self.perceptronsLHS) == 0 or len(self.activations) == len(self.perceptronsLHS):
            self.q = sum(self.activations)
            for perceptron in self.perceptronsRHS:
                perceptron.activate(self.q)
            self.activations = []

    def propagate(self, t: float, p: Self = None):
        self.propagation.update({p: t})
        if len(self.perceptronsRHS) == 0 or len(self.propagation) == len(self.perceptronsRHS):
            if len(self.perceptronsRHS) > 5:
                perceptronRHS_max: Perceptron = max(
                    self.propagation, key=lambda x: abs(self.propagation.get(x)))
                self.disconnectRHS(perceptronRHS_max)
                print(self.name, self.propagation[perceptronRHS_max], len(
                    self.perceptronsRHS))
            d = sum(self.propagation.values())
            if d > 0:
                self.coef = self.coef - 1e-4
            else:
                self.coef = self.coef + 1e-4
            for perceptron in self.perceptronsLHS:
                perceptron.propagate(d, self)
            self.propagation = {}
