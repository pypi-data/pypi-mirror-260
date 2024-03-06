def mod(a, b):
    remainder = a % b
    if remainder < 0:
        remainder += abs(b)
    return remainder

def mod_pow(base, exponent, modulus):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2

    return result