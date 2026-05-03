# Light Refactoring Plan

## 1. Overview
This project is a small Pygame simulation where squares move around a window, bounce off walls, flee larger nearby squares, chase smaller nearby squares, and respawn after their lifespan ends.

The code already has a clear game-loop shape and a useful dataclass-based model, but most of the behavior still lives in one file. The main opportunities are to make the behavior settings easier to read, reduce repeated neighbor-scanning logic, and make the update flow a little easier to follow for a beginner.

## 2. Refactoring Goals
- Make the simulation rules easier to read and tune.
- Reduce duplicated logic in the neighbor-finding helpers.
- Keep the update loop simple and easy to trace.
- Preserve the current gameplay behavior as much as possible.
- Add concise inline comments in the final code so students can see what changed and why.

## 3. Step-by-Step Refactoring Plan

### Step 1: Pull behavior values into named constants
Move the flee radius, flee strength, chase radius, and chase strength out of `update_squares()` and into top-level constants near the other settings.

Why this helps: beginners can see the important tuning values in one place instead of hunting through the update function. It also makes later testing and adjustment easier because the behavior is no longer hidden inside the loop.

Inline comment requirement for the final code: add short comments next to the new constants explaining that they control how far squares look for others and how strongly they react.

Optional before/after idea:
```python
# before: numbers are hidden inside the update loop
# after: named constants describe the behavior
```

### Step 2: Add one shared neighbor-filter helper
Create a small helper that scans all squares once and returns nearby squares matching a rule, such as “bigger than me” or “smaller than me.” The helper can take a comparison condition or a tiny predicate function if that stays simple.

Why this helps: both `find_bigger_nearby_squares()` and `find_smaller_nearby_squares()` follow the same pattern. A shared helper removes duplicate looping logic and makes the difference between the two behaviors easier to spot.

Inline comment requirement for the final code: explain that the helper exists to avoid repeating the same scan logic twice and to keep neighbor rules easy to change.

Keep it beginner-friendly: do not over-abstract the helper. The point is to share one small loop, not to build a complex framework.

### Step 3: Simplify the update flow with clear phases
Reorganize `update_squares()` so the frame logic reads in a predictable order: age/respawn, detect neighbors, apply steering, move, then handle walls.

Why this helps: a clean phase order makes the simulation easier to reason about. Students can trace one square through a single frame without jumping around the function.

Inline comment requirement for the final code: add short comments marking the major phases, such as aging, behavior, movement, and boundary handling.

Suggested shape:
```python
# age and replace expired squares
# find nearby threats and targets
# apply flee and chase forces
# move the square
# bounce off walls
```

### Step 4: Reduce repeated speed-clamp logic
The flee and chase functions both end by clamping velocity to `square.max_speed`. Move that repeated clamping into one tiny helper if it stays readable, or at least make the current block visually consistent in both functions.

Why this helps: repeated math is easier to maintain when it lives in one place. It also reduces the chance that one steering rule gets updated while the other is forgotten.

Inline comment requirement for the final code: explain that clamping keeps squares from accelerating too much after steering forces are applied.

### Step 5: Improve naming where the meaning is still hidden
Check the names of local variables like `away_x`, `away_y`, `chase_x`, and `chase_y`. If any name can be made clearer without becoming long, rename it so the vector purpose is obvious.

Why this helps: clearer names reduce the amount of mental work needed to follow vector math. That is especially useful for first-year students who are still learning how direction vectors work.

Inline comment requirement for the final code: add short comments near the vector math explaining that the code is combining directions and then normalizing them.

### Step 6: Add a few focused beginner tests or manual checks to the report
Update the documentation or notes with a short checklist for checking the refactor: confirm bounce behavior still works, confirm fleeing still happens, and confirm respawn still replaces dead squares.

Why this helps: refactoring is safer when behavior is checked one small piece at a time. Beginners learn that clean-up should not change the program’s visible behavior.

Inline comment requirement for the final code: if you add any small debug comments during testing, keep them temporary and remove them after validation.

## 4. Final Output Requirements (Mandatory)
When this plan is executed, the output MUST:
- Contain only the refactored code.
- Include inline comments explaining what changed, why it improves the code, and the relevant programming concept.
- Keep the comments short, clear, and beginner-friendly.
- Preserve the current gameplay behavior unless a change is explicitly needed for readability.

## 5. Key Concepts for Students
- **Constants**: named values make code easier to tune and understand.
- **DRY**: do not repeat the same scan logic in two places if one helper can do the job.
- **Game loop phases**: breaking a frame into smaller steps makes debugging easier.
- **Vector normalization**: direction vectors are easier to use after they are scaled to length 1.
- **Speed clamping**: limits stop motion from becoming unrealistic or unstable.

## 6. Safety Notes
- Test after each small change instead of refactoring everything at once.
- Keep the square behavior the same unless the refactor clearly improves readability or correctness.
- Be careful with shared helpers: if they become too clever, the code becomes harder for beginners to follow.
- After moving constants or helpers, re-run the simulation to confirm that fleeing, chasing, bouncing, and respawning still work.
