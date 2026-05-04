# MY_EXAM

## Exercise 0

Initialized exam notes file.

## Exercise 1

I changed the square creation so the program starts with a fixed mix of sizes: 5 squares of size 25, 10 squares of size 10, and 30 squares of size 4. I used a list of tuples so each group is easy to read and change.

## Exercise 2

I changed the respawn logic so a square keeps the same size when it dies and respawns. This helps preserve the size mix instead of creating a completely random size each time.

## Exercise 3

I replaced wall bouncing with screen wrapping. When a square leaves one side of the screen, it appears on the opposite side. I kept the velocity unchanged because the requirement says the speed should stay the same.

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

## Exercise 9

For animated growth, I changed eating so the predator does not instantly jump to the bigger size. Instead, it stores a `target_size` and a `growth_rate`, then each update moves the current size toward the target. I used `GROWTH_SPEED = 0.5` because the assignment said 500 ms, and that made the idea easy to connect to the code.

This version is intentionally simple. It does not do fancy easing or special visual effects, and if a square eats again while already growing it just updates the target size and keeps going. I think that is good enough for this exam because the main idea is visible: growth happens over time instead of all at once.

## Exercise 10

For the boids screen wrapping, I used the same basic idea as the square wrapping from earlier. If a boid goes past the left side, it appears on the right, and the same thing happens for top and bottom. I did not change the velocity because the spec says the speed should stay unchanged. I also made wrap the default wall behavior so I can see this feature right away when running the boids file.

## Exercise 11

For random steer, I changed the boid's angle by a small random amount instead of directly adding random numbers to `vx` and `vy`. I think this is better because the boid keeps about the same speed, but the direction wiggles a little bit and looks more natural. I used the `spread` value as the maximum left or right turn amount.

## Exercise 12

For separation, I loop through the nearby boids and make a vector pointing away from each one. I divide by distance so a really close boid pushes harder than one that is only barely inside the separation range. Then in `update`, I add that steering vector to the velocity when separation is turned on. I turned separation on by default so I can actually see the behavior when the program starts.

## Exercise 13

For alignment, I look at nearby boids and add up their velocity vectors. Then I divide by how many neighbors I found to get the average direction/speed. The steering value is the average velocity minus my current velocity, so the boid slowly turns toward what the local group is doing instead of instantly copying them.
I also filled in the speed clamp because separation and alignment can keep adding to the velocity. This felt like a bug fix, not extra polish, because otherwise the boids could get faster than the config limits.

## Exercise 14

For cohesion, I average the positions of nearby boids to find the local center of the group. Then I subtract my boid's current position from that center point, which gives a vector pointing toward the group. This should help keep the boids from spreading out forever, especially when it works together with separation and alignment.

## Exercise 15

For a S.A.C. flocking test, I would measure whether nearby boids start moving in a more similar direction after separation, alignment, and cohesion run for a little while. The easiest number for me to track is heading agreement: compare each boid's direction to the average direction of the group. If the score goes up, that suggests the boids are starting to flock instead of all going random ways.

This is not the only thing flocking means. A better test could also check that boids do not overlap too much and that they stay close enough to count as a group. For this exam, I think heading agreement is a clear first metric because alignment is one of the main rules and it is easy to print and understand.

## Exercise 16

I implemented the S.A.C. test using a small controlled group of boids with different starting directions. The test runs the boids for 60 frames and compares the heading agreement before and after. It passes if the ending heading agreement is higher. I know this does not prove every visual part of flocking, but it gives me a simple check that the combined rules are pushing the group toward shared movement.
