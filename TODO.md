## New Task TODO: Fleeing Behavior

- [ ] Define data needed per square
  - [ ] Confirm each square has: position, velocity, size.
  - [ ] Decide whether max speed is fixed or can vary by square.

- [ ] Define threat detection rule
  - [ ] Pick a detection radius (in pixels).
  - [ ] Filter nearby squares to only those bigger than the current square.
  - [ ] Ignore self when scanning neighbors.

- [ ] Choose flee strategy (decision point)
  - [ ] Option A: flee from nearest bigger square only.
  - [ ] Option B: combine vectors from all bigger nearby squares.
  - [ ] Document why you chose A or B.

- [ ] Compute flee direction safely
  - [ ] Build vector from current square to threat.
  - [ ] Reverse vector to get flee direction.
  - [ ] Handle zero-distance case to avoid divide-by-zero.
  - [ ] Normalize direction before scaling by strength.

- [ ] Define flee strength behavior
  - [ ] Decide if strength is constant or distance-based.
  - [ ] If distance-based, choose a falloff rule (e.g., inverse distance).
  - [ ] Clamp final flee force to avoid sudden jumps.

- [ ] Blend flee with existing movement
  - [ ] Combine flee vector with current velocity (do not fully replace).
  - [ ] Keep some randomness as described in report.
  - [ ] Clamp final speed to max speed.

- [ ] Apply time-based motion
  - [ ] Multiply movement by delta_time.
  - [ ] Verify behavior stays similar across different FPS values.

- [ ] Keep wall collision compatible
  - [ ] Ensure bounce logic still works after flee force is added.
  - [ ] Prevent squares from getting stuck at boundaries.

- [ ] Add lightweight debugging
  - [ ] Temporary print/log of number of threats detected.
  - [ ] Optional: draw debug lines from small square to threat source.

- [ ] Test cases to run
  - [ ] Case 1: isolated square (no threat) keeps normal movement.
  - [ ] Case 2: one larger nearby square causes visible flee response.
  - [ ] Case 3: multiple larger squares behaves according to chosen strategy.
  - [ ] Case 4: equal-size squares should not trigger fleeing.

- [ ] Final cleanup
  - [ ] Remove temporary debug visuals/logs.
  - [ ] Update REPORT with your chosen strategy and observations.
