# MY_EXAM

## Exercise 0

Initialized exam notes file.

## Exercise 4

I added a `check_collision` function in `main.py`. Since the shapes in my program are squares and Pygame already has rectangle collision with `colliderect`, I used that instead of writing distance math. This feels simpler and matches how I draw the squares.

## Exercise 5

For eating, I checked each pair of squares after they move. If two squares collide and they are different sizes, I mark the smaller one as eaten. I respawn it instead of removing it, because the simulation should keep the same amount of squares and the eaten square should come back with its original size.

## Exercise 6

I changed the eating helper so the predator also grows after eating. I decided "proportional" means the predator gains half of the prey's size. I also capped the grown size at 80 pixels because otherwise one square could take over the whole screen too quickly. Since bigger squares are supposed to move slower in my program, I recalculate the predator's max speed after it grows.
