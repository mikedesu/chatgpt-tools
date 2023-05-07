import random

# Create a list of possible items
items = ["sword", "shield", "potion", "key", "map"]

# Create a list of possible monsters
monsters = ["dragon", "troll", "ogre", "giant spider", "gargoyle"]

# Create a list of possible locations
locations = ["dungeon", "cave", "forest", "tower", "castle"]

# Create a list of possible actions
actions = ["fight", "run", "hide", "search", "bribe"]

# Create a list of possible outcomes
outcomes = ["victory", "defeat", "escape", "treasure", "trap"]

# Set the initial score to 0
score = 0

# Set the initial health to 10
health = 10

# Set the initial location
location = random.choice(locations)

# Set the initial monster
monster = random.choice(monsters)

# Set the initial item
item = random.choice(items)

# Print the initial game state
print("You are in a " + location + " and you encounter a " + monster + "!")
print("You have a " + item + " and " + str(health) + " health.")

# Start the game loop
while health > 0:
    # Ask the player what action to take
    action = input("What do you want to do? ")
    
    # Check if the action is valid
    if action in actions:
        # Generate a random outcome
        outcome = random.choice(outcomes)
        
        # Check if the outcome is positive
        if outcome == "victory" or outcome == "treasure" or outcome == "escape":
            # Increase the score
            score += 1
            
            # Print a success message
            print("You " + action + " and you " + outcome + "!")
            
            # Generate a new monster
            monster = random.choice(monsters)
            
            # Generate a new item
            item = random.choice(items)
            
            # Print the new game state
            print("You are in a " + location + " and you encounter a " + monster + "!")
            print("You have a " + item + " and " + str(health) + " health.")
        else:
            # Decrease the health
            health -= 1
            
            # Print a failure message
            print("You " + action + " and you " + outcome + "!")
            
            # Print the new game state
            print("You are in a " + location + " and you encounter a " + monster + "!")
            print("You have a " + item + " and " + str(health) + " health.")
    else:
        # Print an error message
        print("That is not a valid action!")

# Print the final score
print("Game Over! Your score is " + str(score) + ".")
