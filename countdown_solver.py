import operator
from functools import lru_cache
import time
from collections import Counter


"""
Brute-force solver for the Countdown numbers game.

Given a set of numbers and a target, this script tries to reach the target using arithmetic operations.
It uses recursion and memoization to efficiently search for solutions and keeps track of the closest result found.
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
    Pretty prints the sequence of operations.
    """
    for idx, op in enumerate(node_seq):
        (nums, oper) = op
        print(f"Step {idx+1}: {nums[0]} {oper} {nums[1]} = {ops[oper](nums[0], nums[1])}")

def countdown_solver(numbers: list, target: int):
    """
    Attempts to solve the Countdown numbers game.

    Parameters:
        numbers (list): List of available numbers.
        target (int): The target number to reach.

    Prints the solution or the closest result found, and the total number of recursive calls.
    """
    # Check trivial solution
    if target in numbers:
        print(f"Trivial solution found: {target} is in the numbers.")
        print("Total recursive calls: 0")
        return

    nodes_seq: list = []
    closest: int = min(numbers, key=lambda x: abs(x - target))

    numbers = sorted(numbers, reverse=True)  # Sort numbers in descending order

    start_time = time.time()
    node, flag = countdown_search(numbers, target, nodes_seq, closest)
    elapsed = time.time() - start_time

    if flag:
        print(f"\nSolution found, with operations:")
        print_node_sequence(node[2])
    else:
        print(f"\nClosest number found: {node[1]} with operations:")
        print_node_sequence(node[2])
    print(f"\nOperation calls: {operation_counter}")
    print(f"Search time: {elapsed:.3f} seconds")
    print(f"Cached values: {operate_node.cache_info().currsize}")
    print(f"Cache hits: {operate_node.cache_info().hits}")
    for op, count in cache_hit_counter.most_common(1):
        nums, operator_symbol = op
        print(f"{nums[0]} {operator_symbol} {nums[1]} → called {count} times")

def countdown_search(nums: list, target: int, nodes_seq: list, closest: int, calls: int = 0, flag: bool = False):
    """
    Recursively searches for a solution to reach the target number using the given numbers.

    Parameters:
        nums (list): Current list of numbers.
        target (int): Target number to reach.
        nodes_seq (list): Sequence of operations performed so far.
        closest (int): Closest number to the target found so far.
        flag (bool): Indicates if an exact solution was found.

    Returns:
        tuple: (best_node, found_flag)
    """

    closest_node = (None, closest, nodes_seq)

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
                    node = (operation, result, nodes_seq + [operation])
                    new_nums = [nums[k] for k in range(len(nums)) if k not in (i, j)] + [result]
                    new_nums = sorted(new_nums, reverse=True)

                    if result == target:
                        return node, True

                    elif abs(result - target) < abs(closest_node[1] - target):
                        closest_node = node

                    rec_node, rec_flag = countdown_search(
                        new_nums, target, node[2], closest_node[1], flag
                    )

                    if rec_flag:
                        return rec_node, True

                    elif rec_node and abs(rec_node[1] - target) < abs(closest_node[1] - target):
                        closest_node = rec_node

    return closest_node, False

@lru_cache(maxsize=None)
def operate_node(operation) -> int | None:
    """
    Executes an arithmetic operation on a pair of numbers.

    Parameters:
        operation (tuple): ((num1, num2), op) where op is a string key for the operation.

    Returns:
        int or None: Result if valid (positive integer), otherwise None.
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



