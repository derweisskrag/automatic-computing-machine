def count_to_billion() -> int:
    count = 0
    for _ in range(100_000_000_1):
        count += 1
    return count