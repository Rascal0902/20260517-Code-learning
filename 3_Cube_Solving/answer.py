from collections import deque


FACE_ORDER = ("U", "D", "F", "B", "L", "R")
FACE_COLORS = {
    "U": "W",
    "D": "Y",
    "F": "G",
    "B": "B",
    "L": "O",
    "R": "R",
}
MOVE_ORDER = (
    "U", "U'", "U2",
    "D", "D'", "D2",
    "L", "L'", "L2",
    "R", "R'", "R2",
    "F", "F'", "F2",
    "B", "B'", "B2",
)
BASE_MOVE_INFO = {
    "U": ("y", 1, 1),
    "D": ("y", -1, -1),
    "L": ("x", -1, -1),
    "R": ("x", 1, 1),
    "F": ("z", 1, -1),
    "B": ("z", -1, 1),
}
MAX_VISITED_STATES = 300000


def build_face_definitions():
    definitions = []

    for face in FACE_ORDER:
        for row in range(3):
            for col in range(3):
                if face == "U":
                    position = (-1 + col, 1, -1 + row)
                    normal = (0, 1, 0)
                elif face == "D":
                    position = (-1 + col, -1, 1 - row)
                    normal = (0, -1, 0)
                elif face == "F":
                    position = (-1 + col, 1 - row, 1)
                    normal = (0, 0, 1)
                elif face == "B":
                    position = (1 - col, 1 - row, -1)
                    normal = (0, 0, -1)
                elif face == "L":
                    position = (-1, 1 - row, -1 + col)
                    normal = (-1, 0, 0)
                else:
                    position = (1, 1 - row, 1 - col)
                    normal = (1, 0, 0)

                definitions.append((face, row, col, position, normal))

    return definitions


def rotate_vector(vector, axis, direction):
    x, y, z = vector
    if axis == "x":
        return (x, -direction * z, direction * y)
    if axis == "y":
        return (direction * z, y, -direction * x)
    return (direction * y, -direction * x, z)


def build_move_permutations():
    definitions = build_face_definitions()
    index_by_geometry = {
        (position, normal): index
        for index, (_, _, _, position, normal) in enumerate(definitions)
    }

    base_permutations = {}
    axis_index = {"x": 0, "y": 1, "z": 2}

    for move, (axis, layer, direction) in BASE_MOVE_INFO.items():
        permutation = [0] * len(definitions)
        coordinate_index = axis_index[axis]

        for old_index, (_, _, _, position, normal) in enumerate(definitions):
            if position[coordinate_index] == layer:
                new_position = rotate_vector(position, axis, direction)
                new_normal = rotate_vector(normal, axis, direction)
            else:
                new_position = position
                new_normal = normal

            new_index = index_by_geometry[(new_position, new_normal)]
            permutation[new_index] = old_index

        base_permutations[move] = tuple(permutation)

    permutations = {}
    for face in BASE_MOVE_INFO:
        permutations[face] = base_permutations[face]
        permutations[f"{face}2"] = compose_permutations(base_permutations[face], base_permutations[face])
        permutations[f"{face}'"] = compose_permutations(
            permutations[f"{face}2"],
            base_permutations[face],
        )

    return permutations


def compose_permutations(first, second):
    return tuple(second[index] for index in first)


def apply_permutation(state, permutation):
    return "".join(state[permutation[index]] for index in range(len(permutation)))


def solved_state():
    return "".join(FACE_COLORS[face] * 9 for face in FACE_ORDER)


def inverse_move(move):
    if move.endswith("2"):
        return move
    if move.endswith("'"):
        return move[0]
    return f"{move}'"


def validate_state(state):
    if len(state) != 54:
        raise ValueError("Input must contain exactly 54 stickers.")

    counts = {}
    for color in state:
        counts[color] = counts.get(color, 0) + 1

    for color in FACE_COLORS.values():
        if counts.get(color, 0) != 9:
            raise ValueError("Each color must appear exactly 9 times.")


def expand_frontier(frontier, visited, other_visited, permutations):
    next_frontier = deque()

    while frontier:
        state = frontier.popleft()

        for move in MOVE_ORDER:
            next_state = apply_permutation(state, permutations[move])
            if next_state in visited:
                continue

            visited[next_state] = (state, move)
            if next_state in other_visited:
                return next_state, next_frontier

            next_frontier.append(next_state)

            if len(visited) > MAX_VISITED_STATES:
                raise RuntimeError("Search space became too large for this educational solver.")

    return None, next_frontier


def reconstruct_solution(meeting_state, forward_visited, backward_visited):
    forward_moves = []
    state = meeting_state
    while forward_visited[state][0] is not None:
        parent, move = forward_visited[state]
        forward_moves.append(move)
        state = parent
    forward_moves.reverse()

    backward_moves = []
    state = meeting_state
    while backward_visited[state][0] is not None:
        parent, move = backward_visited[state]
        backward_moves.append(inverse_move(move))
        state = parent

    return forward_moves + backward_moves


def solve_cube(initial_state):
    validate_state(initial_state)
    target_state = solved_state()
    if initial_state == target_state:
        return []

    permutations = build_move_permutations()
    forward_visited = {initial_state: (None, None)}
    backward_visited = {target_state: (None, None)}
    forward_frontier = deque([initial_state])
    backward_frontier = deque([target_state])

    while forward_frontier and backward_frontier:
        if len(forward_frontier) <= len(backward_frontier):
            meeting_state, forward_frontier = expand_frontier(
                forward_frontier,
                forward_visited,
                backward_visited,
                permutations,
            )
        else:
            meeting_state, backward_frontier = expand_frontier(
                backward_frontier,
                backward_visited,
                forward_visited,
                permutations,
            )

        if meeting_state is not None:
            return reconstruct_solution(meeting_state, forward_visited, backward_visited)

    raise RuntimeError("No solution found.")


if __name__ == "__main__":
    initial_state = "".join(input().strip() for _ in range(6))
    solution_moves = solve_cube(initial_state)
    print(len(solution_moves))
    print(" ".join(solution_moves))
