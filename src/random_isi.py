import random

def split_time_integer(total_seconds=60, parts=10, min_val=3, max_val=11):
    splits = []
    remaining = total_seconds

    for i in range(parts):
        remaining_parts = parts - i - 1
        min_possible = min_val * remaining_parts
        max_possible = max_val * remaining_parts
        # print(remaining_parts, min_possible, max_possible)
        if remaining_parts == 0:
            chunk = remaining  # last chunk takes all the rest
        else:
            lower = max(min_val, remaining - max_possible)
            upper = min(max_val, remaining - min_possible)
            chunk = random.randint(lower, upper)
            # print(lower, upper, chunk)
        splits.append(chunk)
        remaining -= chunk
        # print(remaining)

    return splits

# Example usage
if __name__ == "__main__":
    random_splits = split_time_integer()
    print(random_splits)
    print(f"Total: {sum(random_splits)}")


