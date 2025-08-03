Randomly generates a numbers game based on the British TV show "Countdown".

Then solves the game using brute force search with memoization

Sample output:
```
Number of large numbers selected: 3
Numbers selected: [ 25  50 100   9   4   2]
Target number: 358

Solution found, with operations:
Step 1: 100 + 50 = 150
Step 2: 150 + 25 = 175
Step 3: 175 + 4 = 179
Step 4: 179 * 2 = 358

Operation calls: 37135
Search time: 0.038 seconds
Cached values: 9249
Cache hits: 27886
25 * 9 → called 76 times
```
