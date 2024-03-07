from src.olympiad_data_structures import number_theory
import time
from functools import reduce


def main():
    n = 10**7
    sieve = number_theory.EratosthenesSieve()
    t1 = time.time()
    sieve.build(n)
    t2 = time.time()
    print(t2 - t1)
    k = int(input())
    print(sieve.is_prime(k), sieve.is_prime_sqrt_method(k))

    n = 10**5
    factorizer = number_theory.Factorizer()
    factorizer.build(n)
    k = int(input())
    factorization = factorizer.factorize(k)
    print("multiplication(", factorization, ") =", reduce(lambda x, y: x * y, factorization, 1))

    return 0


if __name__ == "__main__":
    main()
