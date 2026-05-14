from collections import deque
import sys
import tkinter as tk


class CubeMoveLibrary:
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
    COLOR_MAP = {
        "W": "#f8fafc",
        "Y": "#facc15",
        "G": "#22c55e",
        "B": "#3b82f6",
        "O": "#fb923c",
        "R": "#ef4444",
    }

    def __init__(self):
        self._definitions = self._build_face_definitions()
        self._permutations = self._build_move_permutations()
        self._solved_state = "".join(self.FACE_COLORS[face] * 9 for face in self.FACE_ORDER)

    @property
    def permutations(self):
        return self._permutations

    @property
    def solved_state(self):
        return self._solved_state

    def apply_move(self, state, move):
        permutation = self._permutations[move]
        return "".join(state[permutation[index]] for index in range(len(permutation)))

    def validate_state(self, state):
        if len(state) != 54:
            raise ValueError("Input must contain exactly 54 stickers.")

        counts = {}
        for color in state:
            counts[color] = counts.get(color, 0) + 1

        for color in self.FACE_COLORS.values():
            if counts.get(color, 0) != 9:
                raise ValueError("Each color must appear exactly 9 times.")

    def face_grid(self, state, face):
        start = self.FACE_ORDER.index(face) * 9
        return state[start:start + 9]

    def inverse_move(self, move):
        if move.endswith("2"):
            return move
        if move.endswith("'"):
            return move[0]
        return f"{move}'"

    def _build_face_definitions(self):
        definitions = []

        for face in self.FACE_ORDER:
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

    def _rotate_vector(self, vector, axis, direction):
        x, y, z = vector
        if axis == "x":
            return (x, -direction * z, direction * y)
        if axis == "y":
            return (direction * z, y, -direction * x)
        return (direction * y, -direction * x, z)

    def _compose_permutations(self, first, second):
        return tuple(second[index] for index in first)

    def _build_move_permutations(self):
        index_by_geometry = {
            (position, normal): index
            for index, (_, _, _, position, normal) in enumerate(self._definitions)
        }
        axis_index = {"x": 0, "y": 1, "z": 2}
        base_permutations = {}

        for move, (axis, layer, direction) in self.BASE_MOVE_INFO.items():
            permutation = [0] * len(self._definitions)
            coordinate_index = axis_index[axis]

            for old_index, (_, _, _, position, normal) in enumerate(self._definitions):
                if position[coordinate_index] == layer:
                    new_position = self._rotate_vector(position, axis, direction)
                    new_normal = self._rotate_vector(normal, axis, direction)
                else:
                    new_position = position
                    new_normal = normal

                new_index = index_by_geometry[(new_position, new_normal)]
                permutation[new_index] = old_index

            base_permutations[move] = tuple(permutation)

        permutations = {}
        for face in self.BASE_MOVE_INFO:
            permutations[face] = base_permutations[face]
            permutations[f"{face}2"] = self._compose_permutations(base_permutations[face], base_permutations[face])
            permutations[f"{face}'"] = self._compose_permutations(permutations[f"{face}2"], base_permutations[face])

        return permutations


class BidirectionalCubeSolver:
    MAX_VISITED_STATES = 300000

    def __init__(self, move_library):
        self.move_library = move_library

    def solve(self, initial_state):
        self.move_library.validate_state(initial_state)
        target_state = self.move_library.solved_state
        if initial_state == target_state:
            return []

        forward_visited = {initial_state: (None, None)}
        backward_visited = {target_state: (None, None)}
        forward_frontier = deque([initial_state])
        backward_frontier = deque([target_state])

        while forward_frontier and backward_frontier:
            if len(forward_frontier) <= len(backward_frontier):
                meeting_state, forward_frontier = self._expand_frontier(
                    forward_frontier,
                    forward_visited,
                    backward_visited,
                )
            else:
                meeting_state, backward_frontier = self._expand_frontier(
                    backward_frontier,
                    backward_visited,
                    forward_visited,
                )

            if meeting_state is not None:
                return self._reconstruct_solution(meeting_state, forward_visited, backward_visited)

        raise RuntimeError("No solution found.")

    def _expand_frontier(self, frontier, visited, other_visited):
        next_frontier = deque()

        while frontier:
            state = frontier.popleft()

            for move in self.move_library.MOVE_ORDER:
                next_state = self.move_library.apply_move(state, move)
                if next_state in visited:
                    continue

                visited[next_state] = (state, move)
                if next_state in other_visited:
                    return next_state, next_frontier

                next_frontier.append(next_state)
                if len(visited) > self.MAX_VISITED_STATES:
                    raise RuntimeError("Search space became too large for this educational solver.")

        return None, next_frontier

    def _reconstruct_solution(self, meeting_state, forward_visited, backward_visited):
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
            backward_moves.append(self.move_library.inverse_move(move))
            state = parent

        return forward_moves + backward_moves


class CubeModel:
    def __init__(self, move_library, state):
        self.move_library = move_library
        self.state = state

    def copy(self):
        return CubeModel(self.move_library, self.state)

    def apply_move(self, move):
        self.state = self.move_library.apply_move(self.state, move)

    def face_grid(self, face):
        return self.move_library.face_grid(self.state, face)


class CubeRenderer:
    FACE_LAYOUT = {
        "U": (3, 0),
        "L": (0, 3),
        "F": (3, 3),
        "R": (6, 3),
        "B": (9, 3),
        "D": (3, 6),
    }

    def __init__(self, canvas, move_library, tile_size=42):
        self.canvas = canvas
        self.move_library = move_library
        self.tile_size = tile_size

    def draw(self, cube_model):
        self.canvas.delete("all")

        for face, (grid_x, grid_y) in self.FACE_LAYOUT.items():
            self._draw_face(cube_model, face, grid_x, grid_y)

    def _draw_face(self, cube_model, face, grid_x, grid_y):
        start_x = 40 + grid_x * self.tile_size
        start_y = 30 + grid_y * self.tile_size
        stickers = cube_model.face_grid(face)

        self.canvas.create_text(
            start_x + 1.5 * self.tile_size,
            start_y - 18,
            text=face,
            font=("Arial", 14, "bold"),
        )

        for index, color_code in enumerate(stickers):
            row = index // 3
            col = index % 3
            x1 = start_x + col * self.tile_size
            y1 = start_y + row * self.tile_size
            x2 = x1 + self.tile_size
            y2 = y1 + self.tile_size

            self.canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=self.move_library.COLOR_MAP[color_code],
                outline="#0f172a",
                width=2,
            )


class CubeVisualizationApp:
    def __init__(self, initial_state, solution_moves, move_library):
        self.move_library = move_library
        self.solution_moves = solution_moves
        self.frames = self._build_frames(initial_state)
        self.current_step = 0

        self.root = tk.Tk()
        self.root.title("Cube Solving Visualization")

        self.title_label = tk.Label(
            self.root,
            text="Cube Solving Interactive Visualization",
            font=("Arial", 18, "bold"),
        )
        self.title_label.pack(pady=(12, 8))

        self.canvas = tk.Canvas(self.root, width=640, height=430, bg="#f8fafc", highlightthickness=0)
        self.canvas.pack(padx=16, pady=8)

        self.info_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 12),
            justify="left",
            anchor="w",
            width=80,
        )
        self.info_label.pack(padx=16, pady=(4, 8), anchor="w")

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=(0, 12))

        tk.Button(button_frame, text="Previous", width=12, command=self.previous_step).grid(row=0, column=0, padx=6)
        tk.Button(button_frame, text="Next", width=12, command=self.next_step).grid(row=0, column=1, padx=6)
        tk.Button(button_frame, text="Reset", width=12, command=self.reset).grid(row=0, column=2, padx=6)

        self.renderer = CubeRenderer(self.canvas, move_library)
        self.render()

    def _build_frames(self, initial_state):
        frames = [CubeModel(self.move_library, initial_state)]
        current_model = CubeModel(self.move_library, initial_state)

        for move in self.solution_moves:
            current_model = current_model.copy()
            current_model.apply_move(move)
            frames.append(current_model)

        return frames

    def render(self):
        current_model = self.frames[self.current_step]
        self.renderer.draw(current_model)

        if self.current_step == 0:
            message = "Initial state"
        else:
            message = f"Apply move: {self.solution_moves[self.current_step - 1]}"

        completed_moves = " ".join(self.solution_moves[:self.current_step]) or "(none)"
        remaining_moves = " ".join(self.solution_moves[self.current_step:]) or "(none)"

        self.info_label.config(
            text=(
                f"Step {self.current_step} / {len(self.solution_moves)}\n"
                f"{message}\n"
                f"Completed: {completed_moves}\n"
                f"Remaining: {remaining_moves}"
            )
        )

    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.render()

    def next_step(self):
        if self.current_step < len(self.solution_moves):
            self.current_step += 1
            self.render()

    def reset(self):
        self.current_step = 0
        self.render()

    def run(self):
        self.root.mainloop()


def read_input():
    lines = [sys.stdin.readline().strip() for _ in range(6)]
    return "".join(lines)


def print_solution(solution_moves):
    print(len(solution_moves))
    print(" ".join(solution_moves))


def main():
    initial_state = read_input()
    move_library = CubeMoveLibrary()
    solver = BidirectionalCubeSolver(move_library)
    solution_moves = solver.solve(initial_state)
    print_solution(solution_moves)

    if "--no-gui" in sys.argv:
        return

    try:
        app = CubeVisualizationApp(initial_state, solution_moves, move_library)
        app.run()
    except tk.TclError:
        pass


if __name__ == "__main__":
    main()
