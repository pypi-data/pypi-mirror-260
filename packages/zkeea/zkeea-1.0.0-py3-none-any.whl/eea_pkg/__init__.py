import numpy

def extended_euclidean_algorithm(a, b):
    x1, y1, x2, y2 = 1, 0, 0, 1

    while b:
        q = a // b
        a, b = b, numpy.mod(a,b)
        x1, x2 = x2, x1 - q * x2
        y1, y2 = y2, y1 - q * y2

    return a, x1, y1

def euclidean_algorithm(a, b):
    while b:
        a, b = b, a % b
    return a
