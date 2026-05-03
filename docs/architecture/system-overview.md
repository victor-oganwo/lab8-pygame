# System Overview

## 1. Context

The project is a small real-time pygame simulation. Squares move inside a bounded window,
react to nearby squares, bounce off walls, and respawn when their lifespan ends.

The current code is intentionally compact and lives in `main.py`, but it is still organized
into clear responsibilities so the behavior is easy to follow.

Main goals:

- Smaller squares flee larger nearby squares.
- Larger squares chase smaller nearby squares.
- Squares keep moving with frame-rate-independent motion.
- Squares bounce off screen edges instead of leaving the window.
- Expired squares are replaced so the simulation stays full.

## 2. Architectural Style

The project uses a lightweight procedural style with a data-centric model:

- `Square` stores the state for each entity.
- Helper functions read and update that state.
- `run()` owns the pygame lifecycle and frame timing.

This is a small game-loop architecture with explicit phases for input, update, and render.

## 3. Main Components

1. **Configuration**
   - Module-level constants define screen size, square count, behavior radii, steering strength, and lifespan ranges.

2. **Entity Model**
   - `Square` holds position, velocity, size, per-square speed cap, age, and lifespan.

3. **Creation Helpers**
   - `compute_max_speed`, `create_random_square`, and `create_squares` build valid starting state.

4. **Neighbor Filtering**
   - `filter_nearby_squares` centralizes the radius scan.
   - `find_bigger_nearby_squares` and `find_smaller_nearby_squares` reuse it with different size rules.

5. **Behavior Helpers**
   - `apply_flee_behavior` combines steering away from threats.
   - `apply_chase_behavior` combines steering toward targets.
   - `clamp_speed` keeps velocity inside each square's limit.

6. **Simulation Step**
   - `update_squares` handles aging, replacement, behavior, movement, and wall collisions in one pass.

7. **Presentation Layer**
   - `draw_scene` clears the screen and draws every square.

8. **Runtime Control**
   - `handle_events` checks for quit input.
   - `run` creates the window, drives the loop, and shuts pygame down safely.

## 4. Component Diagram

```mermaid
flowchart TD
    A[run()] --> B[handle_events()]
    A --> C[clock.tick(FPS)]
    A --> D[update_squares()]
    A --> E[draw_scene()]
    D --> F[filter_nearby_squares()]
    D --> G[apply_flee_behavior()]
    D --> H[apply_chase_behavior()]
    D --> I[clamp_speed()]
    D --> J[create_random_square()]
    E --> K[pygame.draw.rect]
```

## 5. Key Design Decisions

1. **Delta-time movement**
   - Motion and steering are multiplied by `delta_time`, so the simulation behaves consistently across frame rates.

2. **Speed limits per square**
   - Squares can receive multiple steering forces, but `clamp_speed` prevents runaway acceleration.

3. **Shared neighbor scan**
   - One helper handles distance checks, which reduces duplication and makes the size rules easier to read.

4. **Lifecycle rebirth**
   - Expired squares are replaced immediately with new random squares, which keeps the screen populated.

5. **Simple data model**
   - The simulation uses a dataclass instead of a heavier class hierarchy, which is easier for beginners to trace.
