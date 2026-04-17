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
GLOBAL_MAX_SPEED: float = 120.0

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


def distance_between(a: Square, b: Square) -> float:
    return math.hypot(b.x - a.x, b.y - a.y)


def compute_max_speed(size: int) -> float:
    size_range = MAX_SQUARE_SIZE - MIN_SQUARE_SIZE
    if size_range == 0:
        return GLOBAL_MAX_SPEED

    normalized = (size - MIN_SQUARE_SIZE) / size_range
    return GLOBAL_MAX_SPEED * (1.0 - 0.6 * normalized)


def create_random_square() -> Square:
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
    )


def create_squares(count: int) -> List[Square]:
    return [create_random_square() for _ in range(count)]


def find_bigger_nearby_squares(
    square: Square,
    squares: List[Square],
    flee_radius: float,
) -> List[Square]:
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

        away_x -= dx / distance
        away_y -= dy / distance

    length = math.hypot(away_x, away_y)
    if length == 0:
        return

    away_x /= length
    away_y /= length

    square.vx += away_x * flee_strength
    square.vy += away_y * flee_strength

    speed = math.hypot(square.vx, square.vy)
    if speed > square.max_speed:
        scale = square.max_speed / speed
        square.vx *= scale
        square.vy *= scale


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
    flee_radius = 150.0
    flee_strength = 80.0
    updated_squares: List[Square] = []

    for square in squares:
        square.age += delta_time

        if square.age >= square.lifespan:
            updated_squares.append(create_random_square())
            continue

        bigger_squares = find_bigger_nearby_squares(square, squares, flee_radius)
        apply_flee_behavior(square, bigger_squares, flee_strength * delta_time)

        square.x += square.vx * delta_time
        square.y += square.vy * delta_time

        if square.x <= 0:
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

        updated_squares.append(square)

    return updated_squares


def draw_scene(screen: pygame.Surface, squares: List[Square]) -> None:
    screen.fill((0, 0, 0))

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
        pygame.display.set_caption("Moving Squares - Life Span + Rebirth")
        clock = pygame.time.Clock()
        squares = create_squares(SQUARE_COUNT)

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