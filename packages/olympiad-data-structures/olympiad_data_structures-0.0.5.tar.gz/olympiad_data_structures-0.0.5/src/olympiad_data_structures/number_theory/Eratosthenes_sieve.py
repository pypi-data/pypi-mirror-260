import typing
from bitarray import bitarray


class EratosthenesSieve:
    def __init__(self) -> None:
        self.n = 0
        self.prime = bitarray()

    def build(self, n: int) -> None:
        self.n = n
        self.prime = self.build_and_get_sieve_in_array(n)

    def is_prime(self, num: int) -> bool:
        return bool(self.prime[num])

    @staticmethod
    def build_and_get_sieve_in_array(n: int,
                                     get_prime_and_multiple: typing.Callable[[int, int], None] = lambda x, y: None,
                                     process_prime: typing.Callable[[int], None] = lambda x: None
                                     ) -> bitarray:
        prime: bitarray = bitarray(n)
        prime.setall(True)
        prime[0] = prime[1] = False
        for i in range(2, n):
            if prime[i]:
                process_prime(i)
                for j in range(2 * i, n, i):
                    prime[j] = False
                    get_prime_and_multiple(i, j)
        return prime

    @staticmethod
    def is_prime_sqrt_method(n: int) -> bool:
        if n < 2:
            return False
        sq = int(n ** 0.5)
        for i in range(2, sq + 1):
            if n % i == 0:
                return False
        return True
