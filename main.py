"""Pygame simulation of moving squares with flee behavior.

Overview:
- Squares move inside a bounded window.
- Bigger nearby squares are treated as threats.
- Smaller squares adjust velocity to move away from threats.
- Movement uses delta time to keep speed stable across FPS.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import random
from typing import List

import pygame


SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
FPS: int = 60
SQUARE_COUNT: int = 20

MIN_SQUARE_SIZE: int = 10
MAX_SQUARE_SIZE: int = 40
GLOBAL_MAX_SPEED: float = 120.0  # pixels per second


@dataclass
class Square:
    """One square entity used by the simulation.

    Attributes:
        x: Horizontal position in pixels.
        y: Vertical position in pixels.
        vx: Horizontal velocity in pixels per second.
        vy: Vertical velocity in pixels per second.
        size: Side length in pixels.
        max_speed: Maximum allowed speed magnitude.
    """

    x: float
    y: float
    vx: float
    vy: float
    size: int
    max_speed: float


def distance_between(a: Square, b: Square) -> float:
    """Return Euclidean distance between two squares (center approximation)."""
    return math.hypot(b.x - a.x, b.y - a.y)


def compute_max_speed(size: int) -> float:
    """Bigger squares are slower."""
    size_range = MAX_SQUARE_SIZE - MIN_SQUARE_SIZE
    if size_range == 0:
        return GLOBAL_MAX_SPEED

    # Map size to [0, 1] so we can scale speed consistently.
    normalized = (size - MIN_SQUARE_SIZE) / size_range
    return GLOBAL_MAX_SPEED * (1.0 - 0.6 * normalized)


def create_squares(count: int) -> List[Square]:
    """Create the initial square list with random size, position, and velocity.

    Args:
        count: Number of squares to create.

    Returns:
        A list of randomized Square instances.
    """
    squares = []

    for _ in range(count):
        size = random.randint(MIN_SQUARE_SIZE, MAX_SQUARE_SIZE)
        max_speed = compute_max_speed(size)

        x = random.randint(0, SCREEN_WIDTH - size)
        y = random.randint(0, SCREEN_HEIGHT - size)

        vx = random.choice([-1, 1]) * random.uniform(40, max_speed)
        vy = random.choice([-1, 1]) * random.uniform(40, max_speed)

        square = Square(
            x=float(x),
            y=float(y),
            vx=float(vx),
            vy=float(vy),
            size=size,
            max_speed=max_speed,
        )
        squares.append(square)

    return squares


def find_bigger_nearby_squares(
    square: Square,
    squares: List[Square],
    flee_radius: float,
) -> List[Square]:
    """Find larger squares near the given square within the flee radius."""
    bigger_squares = []

    for other in squares:
        if other is square:
            continue
        if other.size <= square.size:
            continue
        if distance_between(square, other) <= flee_radius:
            bigger_squares.append(other)

    return bigger_squares


def apply_flee_behavior(
    square: Square,
    bigger_squares: List[Square],
    flee_strength: float,
) -> None:
    """Adjust square velocity away from detected threats.

    Strategy:
    - Build one combined "away" direction from all nearby bigger squares.
    - Normalize that direction.
    - Add scaled flee force to current velocity.
    - Clamp final speed to square.max_speed.
    """
    if not bigger_squares:
        return

    away_x = 0.0
    away_y = 0.0

    for other in bigger_squares:
        dx = other.x - square.x
        dy = other.y - square.y
        distance = math.hypot(dx, dy)

        if distance == 0:
            continue

        # Add a unit vector pointing away from each threat.
        away_x -= dx / distance
        away_y -= dy / distance

    length = math.hypot(away_x, away_y)
    if length == 0:
        return

    # Normalize combined flee direction before applying strength.
    away_x /= length
    away_y /= length

    square.vx += away_x * flee_strength
    square.vy += away_y * flee_strength

    speed = math.hypot(square.vx, square.vy)
    if speed > square.max_speed:
        # Keep motion stable by clamping to per-square max speed.
        scale = square.max_speed / speed
        square.vx *= scale
        square.vy *= scale


def handle_events() -> bool:
    """Process Pygame events.

    Returns:
        False when a quit event is received, otherwise True.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def update_squares(
    squares: List[Square],
    width: int,
    height: int,
    delta_time: float,
) -> None:
    """Update velocities and positions for one frame.

    Steps per square:
    1) Detect nearby bigger threats.
    2) Apply flee force to velocity.
    3) Integrate position with delta_time.
    4) Resolve wall collisions by clamping and inverting velocity.
    """
    flee_radius = 150.0
    flee_strength = 80.0

    for square in squares:
        bigger_squares = find_bigger_nearby_squares(square, squares, flee_radius)
        apply_flee_behavior(square, bigger_squares, flee_strength * delta_time)

        # Integrate velocity with delta_time (seconds per frame).
        square.x += square.vx * delta_time
        square.y += square.vy * delta_time

        if square.x <= 0:
            # Clamp position to wall, then reflect velocity.
            square.x = 0
            square.vx *= -1
        elif square.x + square.size >= width:
            square.x = width - square.size
            square.vx *= -1

        if square.y <= 0:
            square.y = 0
            square.vy *= -1
        elif square.y + square.size >= height:
            square.y = height - square.size
            square.vy *= -1


def draw_scene(screen: pygame.Surface, squares: List[Square]) -> None:
    """Render the scene: clear background and draw all squares."""
    screen.fill((0, 0, 0))

    for square in squares:
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (int(square.x), int(square.y), square.size, square.size),
        )


def run() -> None:
    """Initialize the app and run the main loop until quit."""
    pygame.init()
    try:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Moving Squares - Flee Behavior")
        clock = pygame.time.Clock()
        squares = create_squares(SQUARE_COUNT)

        running = True
        while running:
            running = handle_events()
            delta_time = clock.tick(FPS) / 1000.0

            update_squares(squares, SCREEN_WIDTH, SCREEN_HEIGHT, delta_time)
            draw_scene(screen, squares)
            pygame.display.flip()
    finally:
        pygame.quit()


if __name__ == "__main__":
    run()
