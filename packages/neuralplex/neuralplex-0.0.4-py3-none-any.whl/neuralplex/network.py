from typing import List
from neuralplex import Layer


class Network:

    def __init__(self, layers: List[Layer]):
        self.layers = layers
        self.input_layer = layers[0]
        self.output_layer = layers[len(layers) - 1]

        for i in range(0, len(layers) - 1):
            l1 = layers[i]
            l2 = layers[i + 1]
            l1.connect(l2)

    def train(self, X_train: List[float], y_train: List[float]) -> None:
        if len(self.input_layer.perceptrons) != len(X_train):
            raise Exception(
                f"The length of the training values, {len(X_train)}, is not equal to the length of input perceptrons: {len(self.input_layer.perceptrons)}"
            )

        if len(self.output_layer.perceptrons) != len(y_train):
            raise Exception(
                f"The length of the training values, {len(y_train)}, is not equal to the length of output perceptrons: {len(self.output_layer.perceptrons)}"
            )

        for i in range(0, len(X_train)):
            self.input_layer.perceptrons[i].activate(X_train[i])

        for i in range(0, len(y_train)):
            y_train = y_train[i]
            perceptron = self.output_layer.perceptrons[i]
            perceptron.propagate(perceptron.value - y_train, None)

    def predict(self, inputs: List[float]) -> List[float]:

        if len(self.input_layer.perceptrons) != len(inputs):
            raise Exception(
                f"The length of the training values, {len(inputs)}, is not equal to the length of input perceptrons: {len(self.input.perceptrons)}"
            )

        for i in range(0, len(inputs)):
            self.input_layer.perceptrons[i].activate(inputs[i])

        return [perceptron.value for perceptron in self.output_layer.perceptrons]
