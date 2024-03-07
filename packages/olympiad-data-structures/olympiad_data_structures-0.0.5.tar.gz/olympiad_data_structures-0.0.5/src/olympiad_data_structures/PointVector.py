import math


class PointVector:
    def __init__(self, *coordinates: float | int):
        self.coordinates: list[float | int] = list(coordinates)

    def __str__(self) -> str:
        return f"PointVector{self.coordinates}"

    def __repr__(self) -> str:
        return f"PointVector{self.coordinates}"

    def __len__(self) -> int:
        return len(self.coordinates)

    def __getitem__(self, index: int) -> float | int:
        return self.coordinates[index]

    def __add__(self, other: "PointVector") -> "PointVector":
        if len(self) != len(other):
            raise ValueError("Dimensions of vectors do not match")
        return PointVector(*(x + y for x, y in zip(self.coordinates, other.coordinates)))

    def __sub__(self, other: "PointVector") -> "PointVector":
        if len(self) != len(other):
            raise ValueError("Dimensions of vectors do not match")
        return PointVector(*(x - y for x, y in zip(self.coordinates, other.coordinates)))

    def __mul__(self, scalar: float | int) -> "PointVector":
        return PointVector(*(x * scalar for x in self.coordinates))

    def __rmul__(self, scalar: float | int) -> "PointVector":
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float | int) -> "PointVector":
        return PointVector(*(x / scalar for x in self.coordinates))

    def __eq__(self, other: "PointVector") -> bool:
        return self.coordinates == other.coordinates

    def __ne__(self, other: "PointVector") -> bool:
        return not self.__eq__(other)

    def __getattr__(self, name: str) -> float | int:
        if name in ('x', 'y', 'z'):
            index = ord(name) - ord('x')
            if index >= len(self.coordinates):
                raise AttributeError(f"Point has no attribute '{name}'")
            return self.coordinates[index]
        elif name == "coordinates":
            return self.__dict__["coordinates"]
        raise AttributeError(f"Point has no attribute '{name}'")

    def __setattr__(self, name: str, value: float | int) -> float | int:
        if name in ('x', 'y', 'z'):
            index = ord(name) - ord('x')
            if index >= len(self.coordinates):
                raise AttributeError(f"Point has no attribute '{name}'")
            self.coordinates[index] = value
            return self.coordinates[index]
        elif name == "coordinates":
            self.__dict__["coordinates"] = value
            return self.__dict__["coordinates"]
        raise AttributeError(f"Point has no attribute '{name}'")

    def magnitude(self) -> float:
        return math.sqrt(sum(x ** 2 for x in self.coordinates))

    def normalize(self) -> "PointVector":
        mag = self.magnitude()
        return PointVector(*(x / mag for x in self.coordinates))

    def dot_product(self, other: "PointVector") -> float | int:
        if len(self) != len(other):
            raise ValueError("Dimensions of vectors do not match")
        return sum(x * y for x, y in zip(self.coordinates, other.coordinates))

    def cross_product(self, other: "PointVector") -> "PointVector":
        if len(self) != 3 or len(other) != 3:
            raise ValueError("Cross product is defined only for 3-dimensional vectors")
        x = self.coordinates[1] * other.coordinates[2] - self.coordinates[2] * other.coordinates[1]
        y = self.coordinates[2] * other.coordinates[0] - self.coordinates[0] * other.coordinates[2]
        z = self.coordinates[0] * other.coordinates[1] - self.coordinates[1] * other.coordinates[0]
        return PointVector(x, y, z)
