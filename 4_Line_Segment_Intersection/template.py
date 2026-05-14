def read_input():
    x1, y1, x2, y2 = map(int, input().split())
    x3, y3, x4, y4 = map(int, input().split())
    return (x1, y1), (x2, y2), (x3, y3), (x4, y4)


def solve(p1, p2, p3, p4):
    # TODO: implement
    return None


def main():
    p1, p2, p3, p4 = read_input()
    answer = solve(p1, p2, p3, p4)

    if answer is None:
        return

    print(answer)


if __name__ == "__main__":
    main()
