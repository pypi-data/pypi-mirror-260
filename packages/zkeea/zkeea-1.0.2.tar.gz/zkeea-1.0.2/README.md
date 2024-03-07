# zkeea
Implementation of Extended Euclidean Algorithm, which is to calculate two integers' greatest common divisor and its linear combination from the two integers at the same time.

## Dependencies
- [numpy](https://numpy.org/)
- [numpy](https://github.com/numpy/numpy)

## Installation
```shell
pip install zkeea
```

## Usage
```python
import zkeea
a, x1, y1 = zkeea.extended_euclidean_algorithm(123, 456)
print(f"gcd of 123 and 456 is {a} = {x1} * 123 + {y1} * 456")
```
