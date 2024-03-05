import math

import numpy as np

a = -0.131293
b = -0.386233


def rot(x: float) -> np.ndarray:
    return np.array([[math.cos(x), -math.sin(x)], [math.sin(x), math.cos(x)]])


def to_theta(m):
    v = m[:2, :2] @ np.array([1, 0])
    print(v)
    return np.arctan2(v[1], v[0])


print(rot(a))
print(to_theta(rot(a)))
