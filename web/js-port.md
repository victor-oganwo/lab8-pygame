# JavaScript Port Plan

## Target

Port the Python Pygame simulation in `main.py` into a single standalone browser app at `web/index.html` using Vanilla JavaScript and HTML5 Canvas.

## Mapping

- `Square` becomes a JavaScript class with the same fields.
- Python lists become JavaScript arrays.
- Python `set[int]` logic becomes a JavaScript `Set` of square ids.
- `clock.tick(FPS)` becomes a `requestAnimationFrame()` loop with `deltaTime` measured from timestamps.
- `pygame.draw.lines` becomes Canvas line drawing with `beginPath()`, `moveTo()`, `lineTo()`, and `stroke()`.
- `pygame.draw.rect` becomes `fillRect()`.

## Implementation Notes

- Preserve the update order from Python: age, growth, flee, chase, movement, wrapping, trails, then collision respawn.
- Keep the same radius and strength constants.
- Keep the same size mix so the browser version starts with the same population balance.
- Expose a small speed test helper so the port can be checked against the Python motion logic.

## Validation

- Confirm the file opens directly in a browser without dependencies.
- Confirm squares move, wrap, grow, flee, and chase.
- Confirm trails are drawn from the center points.
- Confirm respawn still preserves the size mix after collisions and lifespan expiry.
