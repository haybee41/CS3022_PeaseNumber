# Lab 06 - Pease Number Calculator
Abiola Bamgbose
CS3310 - NPS

## What it does

Takes a birthday (month, day, year) and calculates the Pease Number using:
1. Fibonacci sequence on month and day
2. Collatz sequence step counts
3. Sum of the three Collatz values

## How to run

Interactive mode:
```
python pease_number.py
```

Run tests (verifies April 10, 1982 = 218):
```
python pease_number.py --test
```

## Extra Credits

**EC1 - Monadic Chaining**: Lines 54-80, Result class with bind() and map() methods. Used in `calc_pease_monadic()` function around line 138.

**EC2 - Convergence Detection**: Lines 85-96, `make_convergence_checker()` returns a function that detects if a number converges to 1 or gets stuck in a loop.

**EC3 - Closure Pattern**: Lines 17-48, `make_fib_calculator()` and `make_collatz_calculator()` keep memo tables inside closures.

## Example

April 10, 1982:
- FBC = [Fib(4), Fib(10)] = [3, 55]
- CFB = [Collatz(3), Collatz(55), Collatz(1982)] = [7, 112, 99]
- Pease = 7 + 112 + 99 = 218

## References

- How to Program Fibonacci Sequence Recursively | Python for Math: https://www.youtube.com/watch?v=Qk0zUZW-U_M

- A Python Guide to the Fibonacci Sequence (Real Python): https://realpython.com/fibonacci-sequence-python/

- The Collatz Sequence in Python (Medium): https://medium.com/the-art-of-python/the-collatz-sequence-in-python-eb7e1f1b4f9e

- Memoization with Fibonacci and Collatz Sequences: https://chrishenson.net/posts/2020-06-03-memo.html
