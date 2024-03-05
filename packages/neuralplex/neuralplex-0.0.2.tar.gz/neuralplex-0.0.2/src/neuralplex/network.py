from typing import List
from neuralplex import Layer


class Network:

    def __init__(self, layers: List[Layer]):
        self.layers = layers
        self.input = layers[0]
        self.output = layers[len(layers) - 1]

        for i in range(0, len(layers) - 1):
            l1 = layers[i]
            l2 = layers[i + 1]
            l1.connect(l2)

    def train(self, inputs: List[float], outputs: List[float]):
        if len(self.input.perceptrons) != len(inputs):
            raise Exception(
                f'The length of the training values, {len(inputs)}, is not equal to the length of input perceptrons: {len(self.input.perceptrons)}')

        if len(self.output.perceptrons) != len(outputs):
            raise Exception(
                f'The length of the training values, {len(outputs)}, is not equal to the length of output perceptrons: {len(self.output.perceptrons)}')

        for i in range(0, len(inputs)):
            self.input.perceptrons[i].activate(inputs[i])

        for i in range(0, len(outputs)):
            o = outputs[i]
            p = self.output.perceptrons[i]
            p.propagate(p.q-o)

    def predict(self, inputs: List[float]):

        if len(self.input.perceptrons) != len(inputs):
            raise Exception(
                f'The length of the training values, {len(inputs)}, is not equal to the length of input perceptrons: {len(self.input.perceptrons)}')

        for i in range(0, len(inputs)):
            self.input.perceptrons[i].activate(inputs[i])

        return [perceptron.q for perceptron in self.output.perceptrons]
