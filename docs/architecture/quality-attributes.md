# Quality Attributes and Evolution

## 1. Current Quality Profile

1. **Readability**
   - The code uses a single `Square` dataclass, named constants, and small helper functions.
   - The update loop is split into phases, which makes the simulation easier to trace.

2. **Stability**
   - Delta-time movement keeps motion consistent across different frame rates.
   - `clamp_speed` prevents squares from accelerating beyond their limit.

3. **Maintainability**
   - Shared logic is centralized in helpers such as `filter_nearby_squares` and `clamp_speed`.
   - Steering values are stored as module-level constants, so tuning is straightforward.

4. **Learnability**
   - The code stays close to beginner-friendly pygame patterns.
   - Each function has a small, visible job.

## 2. Architectural Risks

1. **Single-file growth risk**
   - If more systems are added, `main.py` could become crowded again.

2. **Pairwise scaling risk**
   - Neighbor scans still cost $O(n^2)$ per frame.

3. **Tuning flexibility risk**
   - Constants are easy to read, but they are still fixed at import time.

## 3. Recommended Evolution Path

1. **Split by responsibility when needed**
   - `models.py` for data structures.
   - `behaviors.py` for flee/chase rules.
   - `simulation.py` for the update pipeline.
   - `rendering.py` for drawing.
   - `config.py` for constants.

2. **Add test coverage for the helpers**
   - Test `compute_max_speed` across the size range.
   - Test `clamp_speed` with velocities above and below the limit.
   - Test `update_squares` for respawn and wall bounce behavior.

3. **Add reproducibility hooks**
   - Allow an optional random seed so experiments can be repeated.

4. **Prepare for larger populations**
   - Introduce a spatial grid or quadtree if the square count increases significantly.

## 4. Testing Strategy

Focus on high-value tests that match the current design:

1. **Unit tests**
   - `compute_max_speed` should produce smaller speed limits for larger squares.
   - `filter_nearby_squares` should respect both radius and size rules.
   - `clamp_speed` should cap the velocity vector correctly.

2. **Behavior tests**
   - `apply_flee_behavior` should push a square away from bigger neighbors.
   - `apply_chase_behavior` should move a square toward smaller neighbors.
   - `update_squares` should replace expired squares instead of dropping them.

3. **Integration checks**
   - The total number of squares should stay constant during runtime.
   - Squares should remain inside the screen after wall collisions.

## 5. Architecture Decision Record (Mini)

### ADR-001: Keep steering additive

- **Status**: Accepted
- **Decision**: Steering forces are added to current velocity.
- **Reason**: This preserves natural motion and avoids abrupt snapping.

### ADR-002: Reuse a shared neighbor filter

- **Status**: Accepted
- **Decision**: One helper handles nearby-square scanning.
- **Reason**: It removes duplication and makes the size rules easier to compare.

### ADR-003: Replace expired squares immediately

- **Status**: Accepted
- **Decision**: A square is reborn as soon as its lifespan ends.
- **Reason**: The visual density stays stable and the simulation keeps moving.
