def read_input():
    faces = [input().strip() for _ in range(6)]
    return "".join(faces)


def solve(initial_state):
    # TODO: implement
    solution_moves = None
    return solution_moves


def main():
    initial_state = read_input()
    solution_moves = solve(initial_state)

    if solution_moves is None:
        return

    print(len(solution_moves))
    print(" ".join(solution_moves))


if __name__ == "__main__":
    main()
