# Neural-pleX

An object oriented neural network implementation.

## Introduction

**Neural-pleX** is an intuitive object oriented neural network implementation. The Neural-pleX API consists of Network, Layer, and Neuron constructors. The networks can be easily [visualized](#visualize-a-neural-plex-network) using a visualization library. <img src="Neural-pleX_float.png" style="width:40%" align="right">

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
    - [Create a 3 Layer Neural Network](#create-a-3-layer-neural-network)
- [Examples](#examples)
    - [Visualize a Neural-pleX Network](#visualize-a-neural-plex-network)
- [Test](#test)

## Installation
```bash
pip install neuralplex
```

## Usage

### Create a 3 Layer Neural Network

This implementation demonstrates each component of the API.  A Network is constructed that has a 4 Neuron input Layer and a 1 Neuron output Layer. The hidden Layer has 8 Neurons.  The Network will undergo one iteration of training.

#### Import the Network, Layer, and Neuron modules.
```python
from neuralplex import Network, Layer, Neuron
```

#### Construct a neural network by specifying the Neurons for each Layer and adding the Layers to a Network.
```python
l1 = Layer(neurons=[Neuron(m=random()) for i in range(0, 4)], step=STEP)
l2 = Layer(neurons=[Neuron(m=random()) for i in range(0, 8)], step=STEP)
l3 = Layer(neurons=[Neuron(m=random())], step=STEP)
n1 = Network([l1, l2, l3])
```

#### Implement one iteration of training.
```python
n1.train([1,1,1,1], [15])
```

#### Generate and print a prediction.
```python
prediction = n1.predict([1,1,1,1])
print(prediction)
```

## Examples
### Visualize a Neural-pleX Network

In this example you will use [D3](https://d3js.org/) and [D3Blocks](https://d3blocks.github.io/d3blocks/pages/html/index.html) in order to visualize a neural network.

#### Create a network.
```python
n = Network([Layer(neurons=[Neuron(m=random(), name=f'l{layer}-p{i}') for i in range(1, size+1)], step=STEP) for layer, size in zip([1,2,3], [4, 8, 1])])
```

#### Use D3 and D3Blocks in order to create a visualization of the Network.
```python
records = []
for layer in n.layers:
    for p1 in layer.neurons:
        for p2 in p1.neuronsRHS:
            records.append({'source':p1.name, 'target':p2.name, 'weight':p1.m})

df = pd.DataFrame(records) 
df['weight'] = df['weight'] * 42

d3 = D3Blocks()
d3.d3graph(df, charge=1e4*3, filepath=None)

for index, source, target, weight in df.to_records():
    if source.startswith('l1'):
        color = '#00274C'
    else:
        color = 'grey'
    d3.D3graph.node_properties[source]['color'] = color
    d3.D3graph.node_properties[source]['size'] = weight

d3.D3graph.node_properties['l3-p1']['color'] = '#FFCB05'
d3.D3graph.show(filepath='./Neural-pleX.html')
```

##### The blue nodes comprise the inputs, the grey nodes comprise the hidden layer, and the yellow node is the output.  The size of the Neuron is proportional to its coefficient.

Before Taining             |  After Training
:-------------------------:|:-------------------------:
![](Neural-pleX_before_training.png)  |  ![](Neural-pleX_after_training.png)

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