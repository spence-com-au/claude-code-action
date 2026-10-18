"""Speed limiting for moving bodies."""

from geometry import Vec2


def limit_speed(velocity: Vec2, max_speed: float) -> Vec2:
    """Scale `velocity` down so that its speed is at most `max_speed`."""
    speed = velocity.magnitude()
    if speed <= max_speed:
        return velocity
    return velocity.scaled(max_speed / speed)
