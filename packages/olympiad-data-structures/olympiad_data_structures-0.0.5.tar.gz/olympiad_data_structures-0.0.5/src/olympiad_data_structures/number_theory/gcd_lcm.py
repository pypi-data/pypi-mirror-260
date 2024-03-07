def gcd(a: int, b: int) -> int:
    while a > 0:
        a, b = b % a, a
    return b


def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def get_greatest_common_divisor(a: int, b: int) -> int:
    return gcd(abs(a), abs(b))


def get_greatest_common_multiple(a: int, b: int) -> int:
    return lcm(abs(a), abs(b))


def extended_euclidean_algorithm(a: int, b: int) -> tuple[int, int, int]:
    """
    Extended Euclidean algorithm -- solution of diophantine equations. For example, ax + by = c, x and y are unknown
    :param a:
    :param b:
    :return: c, x, y (where c = greatest_common_divisor(a, b))
    """
    if b == 0:
        return a, 1, 0
    greatest_common_divisor, x, y = extended_euclidean_algorithm(b, a % b)
    x, y = y, x - (a // b) * y
    return greatest_common_divisor, x, y
