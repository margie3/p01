import random

# Initialize variables for the game state
end = False
win = False
result = None

def flip(choice):
    global end, win, result
    # Randomly choose 'heads' or 'tails'
    result = random.choice(["heads", "tails"])
    end = True
    if choice == result:
        win = True
    else:
        win = False

def reset():
    global end, win, result
    end = False
    win = False
    result = None
