import time
from random import random, randint
import json
import pickle
import numbers
import math
from sklearn.metrics import r2_score
from neuralplex import Network, Layer, Perceptron

EPOCHS = int(1e6 / 2)

l1 = Layer(
    perceptrons=[
        Perceptron(coef=random(), name="in-0"),
        Perceptron(coef=random(), name="in-1"),
        Perceptron(coef=random(), name="in-2"),
        Perceptron(coef=random(), name="in-3"),
    ],
    deg=1,
)

# l2a = Layer(
#     perceptrons=[Perceptron(coef=random()*1e2) for i in range(0, 10)], deg=2
# )

l2b = Layer(perceptrons=[Perceptron(coef=random() * 1e2) for i in range(0, 100)], deg=2)

l3 = Layer(perceptrons=[Perceptron(coef=random(), name="out-0")], deg=1)

n1 = Network([l1, l2b, l3])

for i in range(0, EPOCHS):

    rn = randint(1, 15)

    b = [int(n) for n in bin(rn)[2:]]

    while len(b) < 4:
        b = [0] + b

    n1.train(b, [rn])

    pn = n1.predict(b)

    print(f"{i} input: {json.dumps(b)}, truth: {rn} prediction: {json.dumps(pn)}")

    if math.isnan(pn[0]):
        break

    # time.sleep(1)

# Not trying to generalize here...  Just seeing if it can converge onto truth.
y_true = []
y_pred = []
for i in range(1, 16):

    b = [int(n) for n in bin(i)[2:]]

    while len(b) < 4:
        b = [0] + b

    pn = n1.predict(b)

    y_true.append(i)
    y_pred.append(pn[0])

    print(f"{i} input: {json.dumps(b)}, truth: {i} prediction: {json.dumps(pn)}")

R2 = r2_score(y_true, y_pred)

print(R2)

if R2 >= 0.7:
    with open("model.pkl", "wb") as f:
        pickle.dump(n1, f)
