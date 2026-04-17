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


## Feature: life span and rebirth

Idea:
Each square should live for a random amount of time.
I added two attributes: age and lifespan.
At every update, age increases by delta_time.
When age becomes greater than or equal to lifespan, the square dies and is replaced by a newly created square.

Design choice:
I used a helper function create_random_square() so the same logic works for both initial creation and rebirth.
I changed update_squares() so it returns a new list of squares, which makes replacing dead squares easier and safer.