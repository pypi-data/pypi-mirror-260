from .Eratosthenes_sieve import EratosthenesSieve


class Factorizer:
    def __init__(self) -> None:
        self.n = 0
        self.minimal_prime_divisors = []

    def build(self, n: int) -> None:
        self.n = n
        self.minimal_prime_divisors = [-1] * n
        EratosthenesSieve.build_and_get_sieve_in_array(n, self._add_min_divisor, self._process_prime)

    def _add_min_divisor(self, i: int, j: int) -> None:
        if self.minimal_prime_divisors[j] == -1:
            self.minimal_prime_divisors[j] = i

    def _process_prime(self, i: int) -> None:
        self.minimal_prime_divisors[i] = i

    def get_minimal_prime_divisor(self, n: int) -> int:
        return self.minimal_prime_divisors[n]

    def factorize(self, n: int, repetitions: bool = True) -> list[int]:
        prime_factors: list[int] = []
        while n > 1:
            count = 0
            minimal_prime_divisor = self.get_minimal_prime_divisor(n)
            while n % minimal_prime_divisor == 0:
                n //= minimal_prime_divisor
                count += 1
            prime_factors += [minimal_prime_divisor] * ((count - 1) * repetitions + 1)
        return prime_factors
