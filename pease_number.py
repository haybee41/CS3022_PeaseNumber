"""
Abiola Bamgbose
Pease Number Calculator
CS3022 Lab 06

Calculates Pease number from birthday using Fibonacci and Collatz sequences.
Uses pure functional programming - no loops, only recursion and memoization.
"""

from typing import Callable, TypeVar, Tuple, Dict, Optional

T = TypeVar('T')
U = TypeVar('U')

# ---- Closure Pattern ----
# Lookup tables live inside these closures

def make_fib_calculator():
    """Fibonacci with memoization via closure."""
    memo = {0: 0, 1: 1}
    
    def fib(n):
        if n in memo:
            return memo[n]
        memo[n] = fib(n - 1) + fib(n - 2)
        return memo[n]
    
    def show_memo():
        return dict(memo)
    
    return fib, show_memo

def make_collatz_calculator():
    """Collatz step counter with memoization via closure."""
    memo = {1: 0}
    
    def steps(n):
        if n in memo:
            return memo[n]
        next_n = n // 2 if n % 2 == 0 else 3 * n + 1
        memo[n] = 1 + steps(next_n)
        return memo[n]
    
    def show_memo():
        return dict(memo)
    
    return steps, show_memo

# ----1: Monadic Chaining ----

class Result:
    """
    Result monad - wraps a value or an error.
    Allows chaining computations with bind/map.
    """
    def __init__(self, val=None, err=None):
        self.val = val
        self.err = err
        self.ok = (err is None)
    
    @classmethod
    def good(cls, v):
        return cls(val=v)
    
    @classmethod
    def bad(cls, e):
        return cls(err=e)
    
    def bind(self, fn):
        """Chain another Result-returning function."""
        if not self.ok:
            return Result.bad(self.err)
        return fn(self.val)
    
    def map(self, fn):
        """Apply fn to value if ok."""
        if not self.ok:
            return Result.bad(self.err)
        return Result.good(fn(self.val))
    
    def __repr__(self):
        return f"Ok({self.val})" if self.ok else f"Err({self.err})"

# ----2: Convergence Detection ----

def make_convergence_checker(max_steps=10000, ceiling=10**15):
    """
    Returns function that checks if n reaches 1 in Collatz sequence.
    Detects loops and runaway growth.
    """
    def does_converge(n, visited=frozenset(), count=0):
        if n == 1:
            return True
        if n in visited or count > max_steps or n > ceiling or n < 1:
            return False
        nxt = n // 2 if n % 2 == 0 else 3 * n + 1
        return does_converge(nxt, visited | {n}, count + 1)
    
    return does_converge

# Set up the memoized functions
fib, get_fib_memo = make_fib_calculator()
collatz, get_collatz_memo = make_collatz_calculator()
converges = make_convergence_checker()

# ---- Core Computation ----

def check_birthday(mm, dd, yyyy):
    """Validate birthday inputs."""
    if mm < 1 or mm > 12:
        return Result.bad(f"Bad month: {mm}")
    if dd < 1 or dd > 31:
        return Result.bad(f"Bad day: {dd}")
    if yyyy < 1:
        return Result.bad(f"Bad year: {yyyy}")
    return Result.good((mm, dd, yyyy))

def get_fib_birthday(bday):
    """FBC = [Fib(month), Fib(day)]"""
    mm, dd, _ = bday
    return Result.good((fib(mm), fib(dd)))

def get_collatz_vals(fbc, year):
    """CFB = [Collatz(fbc[0]), Collatz(fbc[1]), Collatz(year)]"""
    f_mm, f_dd = fbc
    
    # Check convergence first
    if not converges(f_mm):
        return Result.bad(f"{f_mm} doesnt converge")
    if not converges(f_dd):
        return Result.bad(f"{f_dd} doesnt converge")
    if not converges(year):
        return Result.bad(f"{year} doesnt converge")
    
    c0 = collatz(f_mm)
    c1 = collatz(f_dd)
    c2 = collatz(year)
    return Result.good((c0, c1, c2))

def add_em_up(cfb):
    """Sum the three collatz values."""
    return cfb[0] + cfb[1] + cfb[2]

def calc_pease_monadic(mm, dd, yyyy):
    """
    Full calculation using monadic chaining.
    """
    return (
        check_birthday(mm, dd, yyyy)
        .bind(lambda bd: 
            get_fib_birthday(bd)
            .bind(lambda fbc: 
                get_collatz_vals(fbc, bd[2])
                .map(add_em_up)))
    )

def calc_pease(mm, dd, yyyy):
    """Simple wrapper - returns int or None."""
    res = calc_pease_monadic(mm, dd, yyyy)
    return res.val if res.ok else None

# ---- Display stuff ----

def show_steps(mm, dd, yyyy):
    """Build string showing all the math."""
    out = []
    out.append(f"\n{'='*55}")
    out.append(f"Pease Number for: {mm}/{dd}/{yyyy}")
    out.append(f"{'='*55}")
    
    out.append(f"\n1) Birthday = [{mm} {dd} {yyyy}]")
    
    f_mm = fib(mm)
    f_dd = fib(dd)
    out.append(f"\n2) Fib Birthday Constant")
    out.append(f"   Fib({mm}) = {f_mm}")
    out.append(f"   Fib({dd}) = {f_dd}")
    out.append(f"   FBC = [{f_mm} {f_dd}]")
    
    c0 = collatz(f_mm)
    c1 = collatz(f_dd)
    c2 = collatz(yyyy)
    out.append(f"\n3) Collatz Fibo-Birthday")
    out.append(f"   Collatz({f_mm}) = {c0} steps")
    out.append(f"   Collatz({f_dd}) = {c1} steps")
    out.append(f"   Collatz({yyyy}) = {c2} steps")
    out.append(f"   CFB = [{c0} {c1} {c2}]")
    
    pease = c0 + c1 + c2
    out.append(f"\n4) Pease = {c0} + {c1} + {c2} = {pease}")
    out.append(f"\n{'='*55}")
    out.append(f"Your Pease Number: {pease}")
    out.append(f"{'='*55}\n")
    
    return '\n'.join(out)

# ---- Input handling (recursive, no loops) ----

def get_int(prompt, valid_fn, err_msg):
    """Recursively get valid integer from user."""
    raw = input(prompt)
    if raw.lower() in ('q', 'quit', 'exit'):
        return None
    try:
        n = int(raw)
        if valid_fn(n):
            return n
        print(err_msg)
        return get_int(prompt, valid_fn, err_msg)
    except ValueError:
        print("Enter a number.")
        return get_int(prompt, valid_fn, err_msg)

def valid_mm(m):
    return 1 <= m <= 12

def valid_dd(d):
    return 1 <= d <= 31

def valid_yyyy(y):
    return y > 0

def run_loop():
    """Main interaction loop (recursive)."""
    print("\n" + "="*55)
    print("PEASE NUMBER CALCULATOR")
    print("Type 'q' to quit")
    print("="*55)
    
    mm = get_int("\nMonth (1-12): ", valid_mm, "Must be 1-12")
    if mm is None:
        print("\nBye!")
        return
    
    dd = get_int("Day (1-31): ", valid_dd, "Must be 1-31")
    if dd is None:
        print("\nBye!")
        return
    
    yyyy = get_int("Year: ", valid_yyyy, "Must be positive")
    if yyyy is None:
        print("\nBye!")
        return
    
    res = calc_pease_monadic(mm, dd, yyyy)
    if res.ok:
        print(show_steps(mm, dd, yyyy))
    else:
        print(f"\nError: {res.err}")
    
    run_loop()

# ---- Testing ----

def test_example():
    """Check against lab example: April 10, 1982 = 218"""
    print("\n" + "="*55)
    print("TEST: April 10, 1982")
    print("="*55)
    
    mm, dd, yyyy = 4, 10, 1982
    
    # Expected from lab doc
    exp_fbc = (3, 55)
    exp_cfb = (7, 112, 99)
    exp_pease = 218
    
    # Actual
    act_fbc = (fib(mm), fib(dd))
    act_cfb = (collatz(act_fbc[0]), collatz(act_fbc[1]), collatz(yyyy))
    act_pease = sum(act_cfb)
    
    print(f"\nFBC: expected {exp_fbc}, got {act_fbc} - {'PASS' if exp_fbc == act_fbc else 'FAIL'}")
    print(f"CFB: expected {exp_cfb}, got {act_cfb} - {'PASS' if exp_cfb == act_cfb else 'FAIL'}")
    print(f"Pease: expected {exp_pease}, got {act_pease} - {'PASS' if exp_pease == act_pease else 'FAIL'}")
    
    return exp_pease == act_pease

def show_extra_credits():
    """Demo the three EC features."""
    print("\n" + "="*55)
    print("EXTRA CREDIT DEMO")
    print("="*55)
    
    # 1: Monadic chaining
    print("\n-- EC1: Monadic Chaining --")
    good = calc_pease_monadic(4, 10, 1982)
    bad = calc_pease_monadic(13, 10, 1982)
    print(f"Valid input: {good}")
    print(f"Invalid month: {bad}")
    
    # 2: Convergence
    print("\n-- EC2: Convergence Detection --")
    nums = [1, 27, 55, 1982]
    def check_all(lst, i=0):
        if i >= len(lst):
            return
        n = lst[i]
        print(f"  {n}: {'converges' if converges(n) else 'diverges'}")
        check_all(lst, i + 1)
    check_all(nums)
    
    # 3: Closure pattern
    print("\n-- EC3: Closure Pattern --")
    fmemo = get_fib_memo()
    cmemo = get_collatz_memo()
    print(f"Fib cache size: {len(fmemo)}")
    print(f"Collatz cache size: {len(cmemo)}")
    print("="*55)

# ---- Main ----

def main():
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--test':
            test_example()
            show_extra_credits()
            return
        if sys.argv[1] == '--demo':
            show_extra_credits()
            return
    
    run_loop()

if __name__ == "__main__":
    main()
