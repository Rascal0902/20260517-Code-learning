def read_input():
    n, k = map(int, input().split())
    return n, k


def solve(n, k):
    # TODO: implement
    stirling_value = None
    catalan_value = None
    return stirling_value, catalan_value


def main():
    n, k = read_input()
    stirling_value, catalan_value = solve(n, k)

    if stirling_value is None or catalan_value is None:
        return

    print(stirling_value, catalan_value)


if __name__ == "__main__":
    main()
