# MY_EXAM

## Exercise 0

Initialized exam notes file.

## Exercise 4

I added a `check_collision` function in `main.py`. Since the shapes in my program are squares and Pygame already has rectangle collision with `colliderect`, I used that instead of writing distance math. This feels simpler and matches how I draw the squares.

## Exercise 5

For eating, I checked each pair of squares after they move. If two squares collide and they are different sizes, I mark the smaller one as eaten. I respawn it instead of removing it, because the simulation should keep the same amount of squares and the eaten square should come back with its original size.

## Exercise 6

I changed the eating helper so the predator also grows after eating. I decided "proportional" means the predator gains half of the prey's size. I also capped the grown size at 80 pixels because otherwise one square could take over the whole screen too quickly. Since bigger squares are supposed to move slower in my program, I recalculate the predator's max speed after it grows.
After recalculating the predator's max speed, I clamp its current speed so it does not keep moving faster than its new allowed speed. I kept the implementation simple so the feature stays readable and does not take too much time away from the other exercises.

## Exercise 7

For trails, I added a list of old center positions to each square. Every frame I add the current center and keep only the last 30 positions, then I draw lines between those points. At first I thought wrapping could make a weird line across the whole screen, because the square jumps from one side to the other. To fix that, I clear the trail when a square wraps around an edge, so the trail starts fresh on the new side.
I also made the trail color a constant because it looked cleaner than leaving the random numbers inside the draw call.

## Exercise 8

For the speed test I made a simple `TEST_MODE_ON` global variable. If I turn it on, the program runs one test square instead of opening the normal game window. I gave the square velocity `(60, 80)`, because that makes its speed exactly 100 using Pythagoras. Then I update it for one second and compare how far it moved to the expected speed.

This is not a perfect test for the whole simulation. It does not test chasing, fleeing, eating, or wrapping all together. My assumption is that this exercise mostly wants proof that `position += velocity * delta_time` is working, so I tested that part directly. To make it more complete, I would probably separate the movement code more and write several tests for movement, wrapping, and behavior forces.
If I had more time, I would make the test suite stronger, but for now this covers the main speed calculation task.
I also moved the expected speed calculation before the update, because the test should compare against the velocity I started with, not anything that might change during the update later.
