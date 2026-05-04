# MY_EXAM

## Exercise 0

Initialized exam notes file.

## Exercise 4

I added a `check_collision` function in `main.py`. Since the shapes in my program are squares and Pygame already has rectangle collision with `colliderect`, I used that instead of writing distance math. This feels simpler and matches how I draw the squares.

## Exercise 5

For eating, I checked each pair of squares after they move. If two squares collide and they are different sizes, I mark the smaller one as eaten. I respawn it instead of removing it, because the simulation should keep the same amount of squares and the eaten square should come back with its original size.

## Exercise 6

I changed the eating helper so the predator also grows after eating. I decided "proportional" means the predator gains half of the prey's size. I also capped the grown size at 80 pixels because otherwise one square could take over the whole screen too quickly. Since bigger squares are supposed to move slower in my program, I recalculate the predator's max speed after it grows.
After recalculating the predator's max speed, I clamp its current speed so it does not keep moving faster than its new allowed speed. Im also not trying to do to much so i dont waste my time

## Exercise 7

For trails, I added a list of old center positions to each square. Every frame I add the current center and keep only the last 30 positions, then I draw lines between those points. At first I thought wrapping could make a weird line across the whole screen, because the square jumps from one side to the other. To fix that, I clear the trail when a square wraps around an edge, so the trail starts fresh on the new side.
I also made the trail color a constant because it looked cleaner than leaving the random numbers inside the draw call.
