def point_on_segment(point, start, end):
    x, y = point
    x1, y1 = start
    x2, y2 = end

    if x < min(x1, x2) or x > max(x1, x2):
        return False
    if y < min(y1, y2) or y > max(y1, y2):
        return False

    return (x2 - x1) * (y - y1) == (y2 - y1) * (x - x1)


def overlap_one_dimension(a1, a2, b1, b2):
    left = max(min(a1, a2), min(b1, b2))
    right = min(max(a1, a2), max(b1, b2))
    return left <= right


def collinear_overlap(p1, p2, p3, p4):
    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2:
        return overlap_one_dimension(y1, y2, p3[1], p4[1])
    return overlap_one_dimension(x1, x2, p3[0], p4[0])


def intersects(p1, p2, p3, p4):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    dx1 = x2 - x1
    dy1 = y2 - y1
    dx2 = x4 - x3
    dy2 = y4 - y3

    determinant = dx1 * dy2 - dy1 * dx2

    if determinant == 0:
        # Parallel or collinear
        cross = (x3 - x1) * dy1 - (y3 - y1) * dx1
        if cross != 0:
            return False
        return collinear_overlap(p1, p2, p3, p4)

    numerator_first = (x3 - x1) * dy2 - (y3 - y1) * dx2
    numerator_second = (x3 - x1) * dy1 - (y3 - y1) * dx1

    if determinant > 0:
        if numerator_first < 0 or numerator_first > determinant:
            return False
        if numerator_second < 0 or numerator_second > determinant:
            return False
    else:
        if numerator_first > 0 or numerator_first < determinant:
            return False
        if numerator_second > 0 or numerator_second < determinant:
            return False

    intersection_x_numerator = x1 * determinant + dx1 * numerator_first
    intersection_y_numerator = y1 * determinant + dy1 * numerator_first

    if determinant < 0:
        determinant = -determinant
        intersection_x_numerator = -intersection_x_numerator
        intersection_y_numerator = -intersection_y_numerator

    intersection = (
        intersection_x_numerator / determinant,
        intersection_y_numerator / determinant,
    )

    return point_on_segment(intersection, p1, p2) and point_on_segment(intersection, p3, p4)


def read_input():
    x1, y1, x2, y2 = map(int, input().split())
    x3, y3, x4, y4 = map(int, input().split())
    return (x1, y1), (x2, y2), (x3, y3), (x4, y4)


def main():
    p1, p2, p3, p4 = read_input()
    print(1 if intersects(p1, p2, p3, p4) else 0)


if __name__ == "__main__":
    main()
