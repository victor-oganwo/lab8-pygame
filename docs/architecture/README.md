# Architecture Documents

This folder documents the current `main.py` implementation of the pygame square simulation.
The goal is to explain how the code is organized, how one frame moves through the system,
and what tradeoffs matter if the project grows.

## Document Map

1. [System Overview](system-overview.md) - what the program contains and how the parts fit together.
2. [Runtime Behavior](runtime-behavior.md) - what happens during a single frame update.
3. [Quality Attributes and Evolution](quality-attributes.md) - readability, scaling risks, and next-step ideas.

## What This Set Covers

- One Python file with a small `Square` data model.
- Delta-time movement and steering behaviors.
- Neighbor queries that decide when squares flee or chase.
- Wall bouncing and lifespan-based respawning.

## How to Use These Docs

- Start with [System Overview](system-overview.md) to understand the structure.
- Read [Runtime Behavior](runtime-behavior.md) to follow the frame loop step by step.
- Finish with [Quality Attributes and Evolution](quality-attributes.md) to see what would change if the project expands.

## Intended Audience

- Students learning how a pygame loop is structured.
- Reviewers checking whether the current code is easy to maintain.
- Future contributors planning new behaviors, tests, or performance improvements.
