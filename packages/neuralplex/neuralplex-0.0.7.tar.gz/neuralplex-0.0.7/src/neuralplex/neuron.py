import math
import statistics
from typing import Dict, List, Self
from scipy.stats import linregress


class Neuron:

    def __init__(self, m: float, b: float = 0, step: float = None, name=None):

        self.m = m
        self.b = b
        self.name = name
        self.step = step

        self.value = 0
        self.activation_count = 0

        self.neuronsRHS: List[Self] = []
        self.neuronsLHS: List[Self] = []

        self.activation: Dict[Self, float] = {}
        self.propagation: Dict[Self, float] = {}

    def connectRHS(self, neuronRHS: Self) -> None:
        if neuronRHS not in self.neuronsRHS:
            self.neuronsRHS.append(neuronRHS)

        if self not in neuronRHS.neuronsLHS:
            neuronRHS.connectLHS(self)

    def connectLHS(self, neuronLHS: Self) -> None:
        if neuronLHS not in self.neuronsLHS:
            self.neuronsLHS.append(neuronLHS)

        if self not in neuronLHS.neuronsRHS:
            neuronLHS.connectRHS(self)

    def disconnectRHS(self, neuronRHS: Self) -> None:
        if neuronRHS in self.neuronsRHS:
            self.neuronsRHS.remove(neuronRHS)

        if self in neuronRHS.neuronsLHS:
            neuronRHS.disconnectLHS(self)

        if len(self.neuronsRHS) == 0:
            for neuron in self.neuronsLHS:
                neuron.disconnectRHS(self)

    def disconnectLHS(self, neuronLHS: Self) -> None:
        if neuronLHS in self.neuronsLHS:
            self.neuronsLHS.remove(neuronLHS)

        if self in neuronLHS.neuronsRHS:
            neuronLHS.disconnectRHS(self)

        if len(self.neuronsLHS) == 0:
            for neuron in self.neuronsRHS:
                neuron.disconnectLHS(self)

    def activate(self, t: float, p: Self = None) -> None:

        if self.activation_count == 0:
            self.activation = {}

        self.activation.update({p: self.m * t})
        self.activation_count = self.activation_count + 1

        if len(self.neuronsLHS) == 0 or self.activation_count == len(self.neuronsLHS):
            self.value = sum(self.activation.values())
            for neuron in self.neuronsRHS:
                neuron.activate(self.value, self)
            self.activation_count = 0

    def propagate(self, error: float, p: Self = None) -> None:

        self.propagation.update({p: error})

        if len(self.neuronsRHS) == 0 or len(self.propagation) == len(self.neuronsRHS):

            error_total = sum(self.propagation.values())
            for error in self.propagation.values():
                self.m = self.m - (error * self.step)

            for p in self.neuronsLHS:
                p_activation_value = self.activation[p]

                if p_activation_value > 0 and error_total > 0 or p_activation_value < 0 and error_total < 0:
                    p.propagate(error_total, self)
                else:
                    p.propagate(math.copysign(1, error_total), self)

            self.propagation = {}
