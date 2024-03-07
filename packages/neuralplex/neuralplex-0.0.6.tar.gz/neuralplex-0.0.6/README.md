# Neural-pleX

An object oriented neural network implementation.

## Installation
```bash
pip install neuralplex
```

## Instructions

### You can construct a neural network by specifying the Perceptrons for each layer and adding the Layers to the Network.
This Network's input Layer has 4 input Perceptrons and its output Layer has 1 output Perceptron. The hidden Layer has 8 Perceptrons.
```python
l1 = Layer(perceptrons=[Perceptron(m=random()) for i in range(0, 4)], step=STEP)

l2 = Layer(perceptrons=[Perceptron(m=random()) for i in range(0, 8)], step=STEP)

l3 = Layer(perceptrons=[Perceptron(m=random())], step=STEP)

n1 = Network(
    [
        l1,
        l2,
        l3,
    ]
)
```
## Test

The Test will train a model that estimates a decimal value given a binary nibble.

### Install package.
```bash
pip install neuralplex
```
### Clone the repository.
```bash
git clone https://github.com/faranalytics/neuralplex.git
```
### Change directory into the repository.
```bash
cd neuralplex
```
### Run the tests.
```bash
python -m unittest -v
```
#### Output
```bash
test_nibbles (tests.test.Test.test_nibbles) ... Training the model.
Training iteration: 0
Training iteration: 1000
Training iteration: 2000
Training iteration: 3000
Training iteration: 4000
Training iteration: 5000
Training iteration: 6000
Training iteration: 7000
Training iteration: 8000
Training iteration: 9000
1 input: [0, 0, 0, 1], truth: 1 prediction: [1.8160007977374275]
2 input: [0, 0, 1, 0], truth: 2 prediction: [2.768211299141504]
3 input: [0, 0, 1, 1], truth: 3 prediction: [4.584212096878932]
4 input: [0, 1, 0, 0], truth: 4 prediction: [3.772563194981495]
5 input: [0, 1, 0, 1], truth: 5 prediction: [5.588563992718923]
6 input: [0, 1, 1, 0], truth: 6 prediction: [6.540774494122998]
7 input: [0, 1, 1, 1], truth: 7 prediction: [8.356775291860426]
8 input: [1, 0, 0, 0], truth: 8 prediction: [6.784403350226391]
9 input: [1, 0, 0, 1], truth: 9 prediction: [8.600404147963818]
10 input: [1, 0, 1, 0], truth: 10 prediction: [9.552614649367897]
11 input: [1, 0, 1, 1], truth: 11 prediction: [11.368615447105324]
12 input: [1, 1, 0, 0], truth: 12 prediction: [10.556966545207885]
13 input: [1, 1, 0, 1], truth: 13 prediction: [12.372967342945314]
14 input: [1, 1, 1, 0], truth: 14 prediction: [13.32517784434939]
15 input: [1, 1, 1, 1], truth: 15 prediction: [15.141178642086818]
R2: 0.9599237139109126
ok

----------------------------------------------------------------------
Ran 1 test in 0.333s

OK
```