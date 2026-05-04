"""Pygame simulation of moving squares with flee behavior.

Overview:
- Squares move inside a bounded window.
- Bigger nearby squares are treated as threats.
- Bigger square should chase smaller ones, while smaller squares try to flee from bigger ones.
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
SQUARE_MIX: list[tuple[int, int]] = [
    (5, 25),
    (10, 10),
    (30, 4),
]

# Behavior constants: control how far squares detect neighbors and how strongly they react.
FLEE_RADIUS: float = 150.0
FLEE_STRENGTH: float = 80.0
CHASE_RADIUS: float = 200.0
CHASE_STRENGTH: float = 60.0

MIN_SQUARE_SIZE: int = 4
MAX_SQUARE_SIZE: int = 40
MAX_GROWN_SIZE: int = 80
GLOBAL_MAX_SPEED: float = 120.0
TRAILS_LENGTH: int = 30
TRAIL_COLOR: tuple[int, int, int] = (130, 130, 130)

MIN_LIFESPAN: float = 30.0
MAX_LIFESPAN: float = 180.0


@dataclass
class Square:
    x: float
    y: float
    vx: float
    vy: float
    size: int
    max_speed: float
    age: float
    lifespan: float
    trail: list[tuple[float, float]]


def distance_between(a: Square, b: Square) -> float:
    return math.hypot(b.x - a.x, b.y - a.y)


def check_collision(a: Square, b: Square) -> bool:
    # I used pygame.Rect here because my squares are already rectangles on screen.
    rect_a = pygame.Rect(int(a.x), int(a.y), a.size, a.size)
    rect_b = pygame.Rect(int(b.x), int(b.y), b.size, b.size)
    return rect_a.colliderect(rect_b)


def handle_eating(squares: List[Square]) -> set[int]:
    eaten_ids: set[int] = set()

    for index, square in enumerate(squares):
        for other in squares[index + 1:]:
            if square.size == other.size:
                continue
            if not check_collision(square, other):
                continue

            # The smaller square loses the collision and gets respawned.
            smaller = square if square.size < other.size else other
            bigger = other if smaller is square else square
            eaten_ids.add(id(smaller))

            # I made growth half the prey size so it is visible but not too fast.
            bigger.size = min(MAX_GROWN_SIZE, bigger.size + max(1, smaller.size // 2))
            bigger.max_speed = compute_max_speed(bigger.size)
            clamp_speed(bigger)

    return eaten_ids


def compute_max_speed(size: int) -> float:
    size_range = MAX_GROWN_SIZE - MIN_SQUARE_SIZE
    if size_range == 0:
        return GLOBAL_MAX_SPEED

    normalized = max(0.0, min(1.0, (size - MIN_SQUARE_SIZE) / size_range))
    return GLOBAL_MAX_SPEED * (1.0 - 0.6 * normalized)


def create_random_square(size: int | None = None) -> Square:
    if size is None:
        size = random.randint(MIN_SQUARE_SIZE, MAX_SQUARE_SIZE)

    max_speed = compute_max_speed(size)

    x = random.randint(0, SCREEN_WIDTH - size)
    y = random.randint(0, SCREEN_HEIGHT - size)

    vx = random.choice([-1, 1]) * random.uniform(40, max_speed)
    vy = random.choice([-1, 1]) * random.uniform(40, max_speed)

    lifespan = random.uniform(MIN_LIFESPAN, MAX_LIFESPAN)

    return Square(
        x=float(x),
        y=float(y),
        vx=float(vx),
        vy=float(vy),
        size=size,
        max_speed=max_speed,
        age=0.0,
        lifespan=lifespan,
        trail=[],
    )


def create_squares() -> List[Square]:
    squares: List[Square] = []

    for count, size in SQUARE_MIX:
        for _ in range(count):
            squares.append(create_random_square(size))

    return squares


def filter_nearby_squares(
    square: Square,
    squares: List[Square],
    radius: float,
    size_compare,
) -> List[Square]:
    """Helper to reduce duplicate neighbor-scanning logic.

    Returns nearby squares that match the size_compare rule (a function that takes
    other.size and square.size and returns True if the square matches the filter).
    """
    nearby = []
    for other in squares:
        if other is square:
            continue
        if not size_compare(other.size, square.size):
            continue
        if distance_between(square, other) <= radius:
            nearby.append(other)
    return nearby


def find_bigger_nearby_squares(
    square: Square,
    squares: List[Square],
    flee_radius: float,
) -> List[Square]:
    # Use shared helper with a rule: 'bigger than current square'.
    return filter_nearby_squares(
        square,
        squares,
        flee_radius,
        lambda other_size, square_size: other_size > square_size,
    )


def find_smaller_nearby_squares(
    square: Square,
    squares: List[Square],
    chase_radius: float,
) -> List[Square]:
    # Use shared helper with a rule: 'smaller than current square'.
    return filter_nearby_squares(
        square,
        squares,
        chase_radius,
        lambda other_size, square_size: other_size < square_size,
    )


def apply_flee_behavior(
    square: Square,
    bigger_squares: List[Square],
    flee_strength: float,
) -> None:
    if not bigger_squares:
        return

    # Combine directions away from all threats, then normalize to unit vector.
    away_x = 0.0
    away_y = 0.0

    for other in bigger_squares:
        dx = other.x - square.x
        dy = other.y - square.y
        distance = math.hypot(dx, dy)

        if distance == 0:
            continue
        # Subtract direction toward threat to get direction away from it.
        away_x -= dx / distance
        away_y -= dy / distance

    length = math.hypot(away_x, away_y)
    if length == 0:
        return

    # Normalize: scale vector to unit length so strength applies consistently.
    away_x /= length
    away_y /= length

    square.vx += away_x * flee_strength
    square.vy += away_y * flee_strength

    clamp_speed(square)


def clamp_speed(square: Square) -> None:
    """Helper to enforce speed limit after steering forces are applied.

    Prevents squares from accelerating too much and ensures consistent max speed across all squares.
    """
    speed = math.hypot(square.vx, square.vy)
    if speed > square.max_speed:
        scale = square.max_speed / speed
        square.vx *= scale
        square.vy *= scale


def record_trail_point(square: Square) -> None:
    # I store the center point so the trail follows the square and not just its corner.
    center = (square.x + square.size / 2, square.y + square.size / 2)
    square.trail.append(center)

    if len(square.trail) > TRAILS_LENGTH:
        square.trail.pop(0)


def apply_chase_behavior(
    square: Square,
    smaller_squares: List[Square],
    chase_strength: float,
) -> None:
    if not smaller_squares:
        return

    # Combine directions toward all targets, then normalize to unit vector.
    toward_x = 0.0
    toward_y = 0.0
    square_center_x = square.x + square.size / 2
    square_center_y = square.y + square.size / 2

    for other in smaller_squares:
        other_center_x = other.x + other.size / 2
        other_center_y = other.y + other.size / 2

        dx = other_center_x - square_center_x
        dy = other_center_y - square_center_y
        distance = math.hypot(dx, dy)

        if distance == 0:
            continue
        # Add direction toward target (normalized by distance).
        toward_x += dx / distance
        toward_y += dy / distance

    length = math.hypot(toward_x, toward_y)
    if length == 0:
        return

    # Normalize: scale vector to unit length so strength applies consistently.
    toward_x /= length
    toward_y /= length

    square.vx += toward_x * chase_strength
    square.vy += toward_y * chase_strength

    clamp_speed(square)


def handle_events() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def update_squares(
    squares: List[Square],
    width: int,
    height: int,
    delta_time: float,
) -> List[Square]:
    """Update all squares through one frame cycle: age, behavior, movement, and collision.

    Behavior constants (FLEE_RADIUS, CHASE_RADIUS, etc.) are defined at module level
    so they are easy to tune without editing this function.
    """
    updated_squares: List[Square] = []

    for square in squares:
        # Phase 1: Age and check for lifespan expiration.
        square.age += delta_time
        if square.age >= square.lifespan:
            updated_squares.append(create_random_square(square.size))
            continue

        # Phase 2: Detect neighbors and apply steering behaviors.
        bigger_squares = find_bigger_nearby_squares(square, squares, FLEE_RADIUS)
        apply_flee_behavior(square, bigger_squares, FLEE_STRENGTH * delta_time)

        smaller_squares = find_smaller_nearby_squares(square, squares, CHASE_RADIUS)
        apply_chase_behavior(square, smaller_squares, CHASE_STRENGTH * delta_time)

        # Phase 3: Integrate position based on velocity and frame time.
        square.x += square.vx * delta_time
        square.y += square.vy * delta_time

        # Phase 4: Wrap around screen edges without changing velocity.
        wrapped = False
        if square.x + square.size < 0:
            square.x = width
            wrapped = True
        elif square.x > width:
            square.x = -square.size
            wrapped = True

        if square.y + square.size < 0:
            square.y = height
            wrapped = True
        elif square.y > height:
            square.y = -square.size
            wrapped = True

        if wrapped:
            # Clearing this avoids one long trail line across the screen after wrapping.
            square.trail.clear()

        record_trail_point(square)

        updated_squares.append(square)

    eaten_ids = handle_eating(updated_squares)
    if not eaten_ids:
        return updated_squares

    # I respawn eaten squares with their same size so the starting mix stays balanced.
    return [
        create_random_square(square.size) if id(square) in eaten_ids else square
        for square in updated_squares
    ]


def draw_scene(screen: pygame.Surface, squares: List[Square]) -> None:
    screen.fill((0, 0, 0))

    for square in squares:
        if len(square.trail) < 2:
            continue

        points = [(int(x), int(y)) for x, y in square.trail]
        pygame.draw.lines(screen, TRAIL_COLOR, False, points, 2)

    for square in squares:
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (int(square.x), int(square.y), square.size, square.size),
        )


def run() -> None:
    pygame.init()
    try:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Moving Squares - Mixed Sizes + Wrapping")
        clock = pygame.time.Clock()
        squares = create_squares()

        running = True
        while running:
            running = handle_events()
            delta_time = clock.tick(FPS) / 1000.0

            squares = update_squares(
                squares,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                delta_time,
            )
            draw_scene(screen, squares)
            pygame.display.flip()
    finally:
        pygame.quit()


if __name__ == "__main__":
    run()
