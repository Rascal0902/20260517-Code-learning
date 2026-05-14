def ccw(p1, p2, p3):
    cross = (
        p1[0] * p2[1]
        + p2[0] * p3[1]
        + p3[0] * p1[1]
        - p1[1] * p2[0]
        - p2[1] * p3[0]
        - p3[1] * p1[0]
    )

    if cross > 0:
        return 1
    if cross < 0:
        return -1
    return 0


def intersects(p1, p2, p3, p4):
    p1p2 = ccw(p1, p2, p3) * ccw(p1, p2, p4)
    p3p4 = ccw(p3, p4, p1) * ccw(p3, p4, p2)

    if p1p2 == 0 and p3p4 == 0:
        if p1 > p2:
            p1, p2 = p2, p1
        if p3 > p4:
            p3, p4 = p4, p3
        return p3 <= p2 and p1 <= p4

    return p1p2 <= 0 and p3p4 <= 0


def read_input():
    x1, y1, x2, y2 = map(int, input().split())
    x3, y3, x4, y4 = map(int, input().split())
    return (x1, y1), (x2, y2), (x3, y3), (x4, y4)


def main():
    p1, p2, p3, p4 = read_input()
    print(1 if intersects(p1, p2, p3, p4) else 0)


if __name__ == "__main__":
    main()
