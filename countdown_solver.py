
import operator
from functools import lru_cache
import time
from collections import Counter
from typing import Optional


"""
Brute-force solver for the Countdown numbers game.

Given a set of numbers and a target, this script tries to reach the target using arithmetic operations (+, -, *, /).
It uses recursion and memoization to efficiently search for solutions and keeps track of the closest result found.

Algorithm stops once any solution is found, the search is exhausted, or the maximum number of calls is reached.
If no exact solution is found, it returns the closest number achieved and the sequence of operations.

Output includes:
- The sequence of operations leading to the solution or closest result
- Search statistics: number of operation calls, cache size, cache hits, and most frequent operation
"""

# Supported operations
ops = {
    '*': operator.mul,
    '+': operator.add,
    '-': operator.sub,
    '/': operator.truediv
}

MAX_CALLS = 3_000_000  # Limit the number of operation calls to prevent infinite recursion
operation_counter = 0
cache_hit_counter = Counter()

def print_node_sequence(node_seq):
    """
    Pretty prints the sequence of operations performed to reach the target or closest result.

    Parameters:
        node_seq (list): List of operation tuples (nums, oper) in the order performed.
    """
    for idx, op in enumerate(node_seq):
        nums, oper = op
        result = ops[oper](nums[0], nums[1])
        print(f"Step {idx+1}: {int(nums[0])} {oper} {int(nums[1])} = {int(result)}")

def countdown_solver(numbers: list, target: int):
    """
    Attempts to solve the Countdown numbers game for a given set of numbers and target.

    Parameters:
        numbers (list): List of available numbers.
        target (int): The target number to reach.

    Prints:
        - The solution or the closest result found
        - The sequence of operations
        - Search statistics (operation calls, cache size, cache hits, most frequent operation)
    """
    # Check trivial solution
    if target in numbers:
        print(f"Trivial solution found: {target} is in the numbers.")
        print("Total recursive calls: 0")
        return

    nodes_seq: list = []
    closest: int = min(numbers, key=lambda x: abs(x - target))
    closest_node = {'operation': None, 'result': closest, 'sequence': nodes_seq}


    numbers = sorted(numbers, reverse=True)  # Sort numbers in descending order

    start_time = time.time()
    node, flag = countdown_search(numbers, target, nodes_seq, closest_node)
    elapsed = time.time() - start_time

    if flag:
        print(f"\nSolution found, with operations:")
        print_node_sequence(node['sequence'])
    else:
        print(f"\nClosest number found: {node['result']} with operations:")
        print_node_sequence(node['sequence'])
    print(f"\nOperation calls: {operation_counter}")
    print(f"Search time: {elapsed:.3f} seconds")
    print(f"Cached operations: {operate_node.cache_info().currsize}")
    print(f"Cache hits: {operate_node.cache_info().hits}")
    for op, count in cache_hit_counter.most_common(1):
        nums, operator_symbol = op
        print(f"{nums[0]} {operator_symbol} {nums[1]} → called {count} times")

def countdown_search(nums: list, target: int, nodes_seq: list, closest_node, flag: bool = False):
    """
    Recursively searches for a solution to the Countdown numbers game.

    Parameters:
        nums (list): Current list of numbers available for operations.
        target (int): Target number to reach.
        nodes_seq (list): Sequence of operations performed so far.
        closest (int): Closest number to the target found so far.
        flag (bool): Indicates if an exact solution was found (used for recursion).

    Returns:
        tuple: (best_node, found_flag)
            best_node (dict): Dictionary with keys 'operation', 'result', 'sequence'.
            found_flag (bool): True if exact solution found, False otherwise.
    """
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            pair = (nums[i], nums[j])
            for op in ops:
                
                global operation_counter
                if operation_counter > MAX_CALLS:  # Limit the number of recursive calls
                    return closest_node, False
                operation_counter += 1
                
                operation = (pair, op)
                result = operate_node(operation)
                
                global cache_hit_counter
                cache_hit_counter[operation] += 1

                if result is not None:
                    node = {
                        'operation': operation,
                        'result': result,
                        'sequence': nodes_seq + [operation]
                    }
                    if result == target:
                        return node, True

                    elif abs(result - target) < abs(closest_node['result'] - target):
                        closest_node = node

                    # Create new numbers list excluding the used pair and including the result
                    new_nums = [nums[k] for k in range(len(nums)) if k not in (i, j)] + [result]
                    new_nums = sorted(new_nums, reverse=True)

                    # Recursive call to search with the new numbers from this node
                    # Pass the closest node to keep track of the best found solution
                    rec_node, rec_flag = countdown_search(
                        new_nums, target, node['sequence'], closest_node, flag=flag
                    )

                    if rec_flag:
                        return rec_node, True

                    elif rec_node and abs(rec_node['result'] - target) < abs(closest_node['result'] - target):
                        closest_node = rec_node

    return closest_node, False

@lru_cache(maxsize=None)
def operate_node(operation) -> Optional[int]:
    """
    Executes an arithmetic operation on a pair of numbers.

    Parameters:
        operation (tuple): ((num1, num2), op) where op is a string key for the operation.
            num1, num2 (int): Operands
            op (str): Operation symbol ('+', '-', '*', '/')

    Returns:
        int or None: Result if valid (positive integer), otherwise None.
            Only returns positive integer results (no negatives, zero, or fractions).
    """

    pair, op = operation
    result = ops[op](pair[0], pair[1])

    if isinstance(result, float):
        if result.is_integer() and result > 0:
            return int(result)
    elif isinstance(result, int) and result > 0:
        return result
    return None

if __name__ == "__main__":
    numbers = [100, 25, 1, 4, 2, 5]
    target = 950
    countdown_solver(numbers, target)



