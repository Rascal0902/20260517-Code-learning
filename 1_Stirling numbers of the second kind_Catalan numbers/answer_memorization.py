stirling_memo = []
catalan_memo = []


def stirling_second_kind(n, k):
    if n == 0 and k == 0:
        return 1
    if n == 0 or k == 0 or k > n:
        return 0
    if k == 1 or k == n:
        return 1
    if stirling_memo[n][k] != -1:
        return stirling_memo[n][k]

    stirling_memo[n][k] = (
        k * stirling_second_kind(n - 1, k)
        + stirling_second_kind(n - 1, k - 1)
    )
    return stirling_memo[n][k]


def catalan(n):
    if n == 0:
        return 1
    if catalan_memo[n] != -1:
        return catalan_memo[n]

    total = 0
    for left_size in range(n):
        right_size = n - 1 - left_size
        total += catalan(left_size) * catalan(right_size)

    catalan_memo[n] = total
    return catalan_memo[n]


if __name__ == "__main__":
    n, k = map(int, input().split())

    stirling_memo = [[-1] * (k + 1) for _ in range(n + 1)]
    catalan_memo = [-1] * (n + 1)

    print(stirling_second_kind(n, k), catalan(n))
