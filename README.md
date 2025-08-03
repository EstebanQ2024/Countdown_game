This code provides:
- Generation of a random numbers game based on the British TV show "Countdown"
- Solution of the game based on brute force search with memoization
    - Some search performance metrics are provided
 
Sample output to terminal:

Number of large numbers selected: 1
Numbers selected: [100   3   6   1   9  10]
Target number: 796

Solution found, with operations:
Step 1: 10 - 6 = 4
Step 2: 9 - 1 = 8
Step 3: 100 * 8 = 800
Step 4: 800 - 4 = 796

Operation calls: 895254
Search time: 0.853 seconds
Cached values: 45159
Cache hits: 850095
6 * 3 → called 1474 times
