# ISE315 HW2 - Change Making (Greedy strategies)
# My goal here is: implement 3 different greedy ideas and compare them on the same inputs.

import sys

# I use sys for 2 reasons:
# 1) sys.argv lets me read the coin set + target value from the terminal (command line).
# 2) sys.exit() lets me stop the program with a clear message when the input is wrong.
# If I don't import sys, I lose those two tools and the program becomes harder to run as requested.

def parse_coin_list(coin_text):
    # I convert something like "25,10,5,1" into [25, 10, 5, 1]
    # I also remove spaces because students (including me) always type spaces randomly.
    cleaned = coin_text.replace(" ", "")
    if cleaned == "":
        return []

    parts = cleaned.split(",")
    coin_vals = []
    for p in parts:
        if p == "":
            continue
        coin_vals.append(int(p))

    # I sort descending because strategy 1 naturally wants largest first.
    # Keeping them in a consistent order also makes debugging easier for me.
    coin_vals = sorted(coin_vals, reverse=True)
    return coin_vals


def read_input_from_file(file_path):
    # I support file input because the homework allows "command line OR a file".
    # File format (simple):
    # line1: coins (example: 25,10,5,1)
    # line2: V (example: 41)
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f.readlines() if ln.strip() != ""]

    if len(lines) < 2:
        # I exit because continuing would just cause confusing errors later.
        print("Input file needs at least 2 non-empty lines: coins on line1, V on line2.")
        sys.exit(1)

    coins = parse_coin_list(lines[0])
    target_v = int(lines[1])
    return coins, target_v


def greedy_largest_first(coin_set, target_value):
    # Strategy 1:
    # Always take the largest coin that still fits in the remaining value.
    remaining = target_value
    picked = []

    # I loop until remaining becomes 0 because that means exact change is reached.
    while remaining > 0:
        took_something = False

        # I scan coins from largest to smallest (coin_set is already sorted desc).
        for c in coin_set:
            if c <= remaining:
                picked.append(c)
                remaining -= c
                took_something = True
                # I break because greedy means I commit to the first (largest) fit.
                break

        if not took_something:
            # If we can't take any coin, it means exact sum is impossible.
            # (This can happen when coin set doesn't include 1, for example.)
            return None

    return picked


def greedy_closest_to_half(coin_set, target_value):
    # Strategy 2:
    # At each step I pick the coin closest to (remaining / 2).
    # Why? Because it's trying to "balance" the remaining amount instead of going all-in on large coins.
    remaining = target_value
    picked = []

    while remaining > 0:
        half_point = remaining / 2.0

        best_coin = None
        best_distance = None

        # I only consider coins that can actually fit.
        for c in coin_set:
            if c <= remaining:
                dist = abs(c - half_point)

                # I pick the smallest distance to half.
                # Tie-break: if same distance, I pick the larger coin to reduce number of coins a bit.
                if best_distance is None or dist < best_distance or (dist == best_distance and c > best_coin):
                    best_distance = dist
                    best_coin = c

        if best_coin is None:
            return None

        picked.append(best_coin)
        remaining -= best_coin

    return picked


def score_remainder_quality(coin_set, remainder_amount):
    # This helper is for Strategy 3.
    # The idea: I want the remainder to be "friendly" for the next step.
    # Homework says: remainder should be divisible by the largest possible denomination.
    #
    # So I compute:
    #   best_divisor = max coin d in coin_set such that remainder_amount % d == 0
    # If none divides it (except maybe 1), then score becomes small.
    best_divisor = 0
    for d in coin_set:
        if d == 0:
            continue
        if remainder_amount % d == 0:
            if d > best_divisor:
                best_divisor = d
    return best_divisor


def greedy_max_remainder(coin_set, target_value):
    # Strategy 3:
    # Try each coin choice, look at the remainder, and prefer leaving a remainder divisible
    # by the largest denomination possible (so next step can use big coins cleanly).
    remaining = target_value
    picked = []

    while remaining > 0:
        best_coin = None
        best_score = None
        best_remainder = None

        for c in coin_set:
            if c <= remaining:
                rem_after = remaining - c
                quality = score_remainder_quality(coin_set, rem_after)

                # I want MAX quality (largest divisor that divides the remainder).
                # Tie-breaks (my own choice):
                # 1) If quality ties, prefer smaller remainder (feels like progress).
                # 2) If still ties, prefer larger coin (fewer coins overall usually).
                if (best_score is None or
                    quality > best_score or
                    (quality == best_score and rem_after < best_remainder) or
                    (quality == best_score and rem_after == best_remainder and c > best_coin)):
                    best_score = quality
                    best_coin = c
                    best_remainder = rem_after

        if best_coin is None:
            return None

        picked.append(best_coin)
        remaining -= best_coin

    return picked


def count_coins(picked_list):
    # I keep this separate because the report cares about number of coins, not the exact list.
    if picked_list is None:
        return None
    return len(picked_list)


def pretty_run_all(coin_set, target_value):
    # This function just runs all strategies and prints results in a clean way.
    s1 = greedy_largest_first(coin_set, target_value)
    s2 = greedy_closest_to_half(coin_set, target_value)
    s3 = greedy_max_remainder(coin_set, target_value)

    print(f"Coins: {coin_set}  |  V = {target_value}")
    print(f"Strategy 1 (largest-first): {count_coins(s1)} coins -> {s1}")
    print(f"Strategy 2 (closest-to-half): {count_coins(s2)} coins -> {s2}")
    print(f"Strategy 3 (max-remainder): {count_coins(s3)} coins -> {s3}")


def main():
    # I handle two input styles:
    # A) python3 change_maker.py 25,10,5,1 41
    # B) python3 change_maker.py input.txt
    #
    # I use sys.argv because it’s the simplest terminal interface without argparse.
    args = sys.argv[1:]

    if len(args) == 1:
        # If one argument: I assume it's a file path.
        coin_set, target_v = read_input_from_file(args[0])
        pretty_run_all(coin_set, target_v)
        return

    if len(args) == 2:
        # If two arguments: coins and value.
        coin_set = parse_coin_list(args[0])
        target_v = int(args[1])

        if target_v < 0:
            print("V should be non-negative.")
            sys.exit(1)

        if len(coin_set) == 0:
            print("Coin set is empty. Example usage: python3 change_maker.py 25,10,5,1 41")
            sys.exit(1)

        pretty_run_all(coin_set, target_v)
        return

    print("Usage examples:")
    print("  python3 change_maker.py 25,10,5,1 41")
    print("  python3 change_maker.py input.txt")
    sys.exit(1)


if __name__ == "__main__":
    main()
