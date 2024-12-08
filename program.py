import curses
import random
import time

# Initialize the curses screen
stdscr = curses.initscr()
curses.curs_set(0)  # Hide the cursor
sh, sw = stdscr.getmaxyx()  # Get screen height and width
w = curses.newwin(sh, sw, 0, 0)  # Create a new window
w.keypad(1)
w.timeout(100)  # Set the timeout to 100 milliseconds for the game loop

# Game variables
player_car = 'A'  # Your car character
car_x = sw // 2  # Starting position of your car (horizontally centered)
car_y = sh - 2  # Your car is at the bottom of the screen
road_width = 5  # Number of "lanes" on the road
score = 0
speed = 1  # Speed of the incoming cars

# List for other cars
other_cars = []

# Function to create a new incoming car at the top of the screen
def create_car():
    lane_width = sw // road_width
    x = random.randint(0, road_width - 1) * lane_width  # Random position in one of the lanes
    y = 0  # Start at the top of the screen
    return [x, y]

# Main game loop
while True:
    w.clear()  # Clear the screen
    w.addstr(0, 2, f'Score: {score}', curses.A_BOLD)  # Display score
    
    # Handle user input to move the car
    key = w.getch()
    if key == ord('q'):  # Quit the game if 'q' is pressed
        break
    elif key == curses.KEY_LEFT and car_x > 0:
        car_x -= sw // road_width  # Move left
    elif key == curses.KEY_RIGHT and car_x < sw - (sw // road_width):
        car_x += sw // road_width  # Move right

    # Move other cars and check for collisions
    for other_car in other_cars:
        x, y = other_car
        if y < sh - 1:  # Move the car down
            other_car[1] += speed
        else:  # Remove the car when it reaches the bottom
            other_cars.remove(other_car)
            score += 1  # Increase the score when the car successfully avoids an incoming car

        # Check if the player's car collides with an incoming car
        if x == car_x and y == car_y:
            w.clear()
            w.addstr(sh // 2, sw // 2 - 6, "Game Over!", curses.A_BOLD)
            w.refresh()
            time.sleep(2)
            break
        
        if x < sw and y < sh:  # Only draw the car if it's within bounds
            w.addstr(y, x, 'X')  # Represent other cars with 'X'

    # Randomly add new cars to the game at the top of the screen
    if random.randint(1, 20) == 1:
        other_cars.append(create_car())

    # Draw the player's car
    if car_x < sw and car_y < sh:
        w.addstr(car_y, car_x, player_car)

    # Refresh the screen
    w.refresh()

    # Control the game speed
    time.sleep(0.005)

# Close the curses window properly
curses.endwin()
