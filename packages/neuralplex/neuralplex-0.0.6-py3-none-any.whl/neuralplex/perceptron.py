import math
import statistics
from typing import Dict, List, Self
from scipy.stats import linregress


class Perceptron:

    def __init__(self, m: float, b: float = 0, step: float = None, name=None):

        self.m = m
        self.b = b
        self.name = name
        self.step = step

        self.value = 0
        self.activation_count = 0

        self.perceptronsRHS: List[Self] = []
        self.perceptronsLHS: List[Self] = []

        self.activation: Dict[Self, float] = {}
        self.propagation: Dict[Self, float] = {}

    def connectRHS(self, perceptronRHS: Self) -> None:
        if perceptronRHS not in self.perceptronsRHS:
            self.perceptronsRHS.append(perceptronRHS)

        if self not in perceptronRHS.perceptronsLHS:
            perceptronRHS.connectLHS(self)

    def connectLHS(self, perceptronLHS: Self) -> None:
        if perceptronLHS not in self.perceptronsLHS:
            self.perceptronsLHS.append(perceptronLHS)

        if self not in perceptronLHS.perceptronsRHS:
            perceptronLHS.connectRHS(self)

    def disconnectRHS(self, perceptronRHS: Self) -> None:
        if perceptronRHS in self.perceptronsRHS:
            self.perceptronsRHS.remove(perceptronRHS)

        if self in perceptronRHS.perceptronsLHS:
            perceptronRHS.disconnectLHS(self)

        if len(self.perceptronsRHS) == 0:
            for perceptron in self.perceptronsLHS:
                perceptron.disconnectRHS(self)

    def disconnectLHS(self, perceptronLHS: Self) -> None:
        if perceptronLHS in self.perceptronsLHS:
            self.perceptronsLHS.remove(perceptronLHS)

        if self in perceptronLHS.perceptronsRHS:
            perceptronLHS.disconnectRHS(self)

        if len(self.perceptronsLHS) == 0:
            for perceptron in self.perceptronsRHS:
                perceptron.disconnectLHS(self)

    def activate(self, t: float, p: Self = None) -> None:

        if self.activation_count == 0:
            self.activation = {}

        self.activation.update({p: self.m * t})
        self.activation_count = self.activation_count + 1

        if len(self.perceptronsLHS) == 0 or self.activation_count == len(self.perceptronsLHS):
            self.value = sum(self.activation.values())
            for perceptron in self.perceptronsRHS:
                perceptron.activate(self.value, self)
            self.activation_count = 0

    def propagate(self, error: float, p: Self = None) -> None:

        self.propagation.update({p: error})

        if len(self.perceptronsRHS) == 0 or len(self.propagation) == len(self.perceptronsRHS):

            error_total = sum(self.propagation.values())
            for error in self.propagation.values():
                self.m = self.m - (error * self.step)

            for p in self.perceptronsLHS:
                p_activation_value = self.activation[p]

                if p_activation_value > 0 and error_total > 0 or p_activation_value < 0 and error_total < 0:
                    p.propagate(error_total, self)
                else:
                    p.propagate(math.copysign(1, error_total), self)

            self.propagation = {}
