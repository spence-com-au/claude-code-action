"""Two-dimensional vectors."""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Vec2:
    x: float
    y: float

    def length(self) -> float:
        return math.hypot(self.x, self.y)

    def scaled(self, factor: float) -> "Vec2":
        return Vec2(self.x * factor, self.y * factor)
