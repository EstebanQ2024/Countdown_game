import numpy as np

""" This script allows to play the British TV show Countdown for the number game.
It generates a random set of large integers and a target number, and then tries to find a solution
to reach the target number using the integers.
"""

def generate_numbers(n_large):
    """Generates a set of 6 mixed large and small numbers."""
    large = [25, 50, 75, 100]
    small = list(range(1, 11))
    small = 2*small  # Duplicate small numbers (each number can be used twice)
    
    n_small = 6 - n_large
    
    selected_large = np.random.choice(large, n_large, replace=False)
    selected_small = np.random.choice(small, n_small, replace=False)
    return np.concatenate((selected_large, selected_small))

n_large = np.random.randint(1, 5) # Randomly choose how many large numbers to include (1 to 4)
print(f"\nNumber of large numbers selected: {n_large}")

numbers = generate_numbers(n_large)
target = np.random.randint(100, 1000)  # Random target number between 100 and 999

print(f"Numbers drawn: {numbers}")
print(f"Target number: {target}")

# Search for a solution
from countdown_solver import countdown_solver
countdown_solver(numbers.tolist(), target)