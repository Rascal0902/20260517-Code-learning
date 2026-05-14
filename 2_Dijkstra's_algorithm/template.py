def read_input():
    n, m, start = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    return n, m, start, edges


def solve(n, m, start, edges):
    # TODO: implement
    distances = None
    return distances


def format_output(distances):
    return " ".join("INF" if value == float("inf") else str(value) for value in distances)


def main():
    n, m, start, edges = read_input()
    distances = solve(n, m, start, edges)

    if distances is None:
        return

    print(format_output(distances))


if __name__ == "__main__":
    main()
