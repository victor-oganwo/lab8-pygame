## Feature: fleeing behavior

Goal:
Make smaller squares flee from bigger nearby squares.

Idea:
For each square, I check nearby squares.
If another square is bigger, I treat it as a threat.
I compute the direction from the small square to the bigger one, then reverse that direction to get a flee vector.

Design choice:
I combine flee direction with the square’s current movement instead of replacing movement completely.
This keeps some randomness and makes the motion look more natural.

Time-based animation:
I use delta_time so movement is based on pixels per second rather than pixels per frame.

Questions:
Should the square flee from only the nearest bigger square, or from all nearby bigger squares combined?
Should flee strength depend on distance?