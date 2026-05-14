from functools import lru_cache


@lru_cache(maxsize=None)
def stirling_second_kind(n, k):
    if n == 0 and k == 0:
        return 1
    if n == 0 or k == 0 or k > n:
        return 0
    if k == 1 or k == n:
        return 1
    return k * stirling_second_kind(n - 1, k) + stirling_second_kind(n - 1, k - 1)


@lru_cache(maxsize=None)
def catalan(n):
    if n == 0:
        return 1

    total = 0
    for left_size in range(n):
        right_size = n - 1 - left_size
        total += catalan(left_size) * catalan(right_size)
    return total


if __name__ == "__main__":
    n, k = map(int, input().split())
    print(stirling_second_kind(n, k), catalan(n))
