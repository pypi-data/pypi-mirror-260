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

def sieve_of_eratosthenes(n):
    primes = [True] * (n + 1)
    primes[0] = primes[1] = False
    for i in range(2, int(n**0.5) + 1):
        if primes[i]:
            for j in range(i * i, n + 1, i):
                primes[j] = False
    return [x for x in range(n + 1) if primes[x]]

def euclidean_division(a, b):
    quotient, remainder = divmod(a, b)
    if remainder < 0:
        remainder += abs(b)
        quotient += 1
    return quotient, remainder
