import heapq
import math
import sys
import tkinter as tk
from dataclasses import dataclass


@dataclass
class Edge:
    source: int
    target: int
    weight: int


@dataclass
class DijkstraSnapshot:
    distances: tuple
    visited: frozenset
    current: int | None
    highlighted_edge: tuple[int, int] | None
    message: str


class Graph:
    def __init__(self, node_count, start_node, edges):
        self.node_count = node_count
        self.start_node = start_node
        self.edges = [Edge(*edge) for edge in edges]
        self.adjacency = [[] for _ in range(node_count + 1)]
        for edge in self.edges:
            self.adjacency[edge.source].append((edge.target, edge.weight))

    def node_positions(self, width, height):
        cx = width / 2
        cy = height / 2
        radius = min(width, height) * 0.36
        positions = {}

        for node in range(1, self.node_count + 1):
            angle = -math.pi / 2 + 2 * math.pi * (node - 1) / self.node_count
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            positions[node] = (x, y)

        return positions


class DijkstraTracer:
    def __init__(self, graph):
        self.graph = graph

    def run(self):
        n = self.graph.node_count
        start = self.graph.start_node
        distances = [float("inf")] * (n + 1)
        distances[start] = 0
        visited = set()
        heap = [(0, start)]

        snapshots = [
            DijkstraSnapshot(
                distances=tuple(distances),
                visited=frozenset(),
                current=None,
                highlighted_edge=None,
                message=f"Initialize: start node {start} has distance 0.",
            )
        ]

        while heap:
            current_distance, node = heapq.heappop(heap)
            if node in visited:
                continue

            snapshots.append(
                DijkstraSnapshot(
                    distances=tuple(distances),
                    visited=frozenset(visited),
                    current=node,
                    highlighted_edge=None,
                    message=f"Select node {node} with tentative distance {current_distance}.",
                )
            )

            visited.add(node)

            for neighbor, weight in self.graph.adjacency[node]:
                candidate = distances[node] + weight
                improved = candidate < distances[neighbor]

                if improved:
                    distances[neighbor] = candidate
                    heapq.heappush(heap, (candidate, neighbor))
                    message = (
                        f"Relax edge {node} -> {neighbor} (weight {weight}): "
                        f"update distance to {candidate}."
                    )
                else:
                    message = (
                        f"Relax edge {node} -> {neighbor} (weight {weight}): "
                        f"keep distance {self._format_distance(distances[neighbor])}."
                    )

                snapshots.append(
                    DijkstraSnapshot(
                        distances=tuple(distances),
                        visited=frozenset(visited),
                        current=node,
                        highlighted_edge=(node, neighbor),
                        message=message,
                    )
                )

        snapshots.append(
            DijkstraSnapshot(
                distances=tuple(distances),
                visited=frozenset(visited),
                current=None,
                highlighted_edge=None,
                message="Done: all reachable shortest distances are finalized.",
            )
        )
        return distances, snapshots

    @staticmethod
    def _format_distance(value):
        return "INF" if value == float("inf") else str(value)


class GraphRenderer:
    def __init__(self, canvas, graph):
        self.canvas = canvas
        self.graph = graph
        self.positions = graph.node_positions(width=760, height=520)

    def draw(self, snapshot):
        self.canvas.delete("all")
        self._draw_edges(snapshot)
        self._draw_nodes(snapshot)

    def _draw_edges(self, snapshot):
        for edge in self.graph.edges:
            x1, y1 = self.positions[edge.source]
            x2, y2 = self.positions[edge.target]

            color = "#64748b"
            width = 2
            if snapshot.highlighted_edge == (edge.source, edge.target):
                color = "#dc2626"
                width = 4

            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width, arrow=tk.LAST)

            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            self.canvas.create_rectangle(mx - 18, my - 12, mx + 18, my + 12, fill="white", outline="")
            self.canvas.create_text(mx, my, text=str(edge.weight), font=("Arial", 11, "bold"))

    def _draw_nodes(self, snapshot):
        for node in range(1, self.graph.node_count + 1):
            x, y = self.positions[node]
            fill = "#e2e8f0"
            outline = "#475569"

            if node in snapshot.visited:
                fill = "#dcfce7"
                outline = "#16a34a"
            if node == self.graph.start_node:
                fill = "#dbeafe" if node not in snapshot.visited else fill
                outline = "#2563eb" if node not in snapshot.visited else outline
            if node == snapshot.current:
                fill = "#fde68a"
                outline = "#d97706"

            self.canvas.create_oval(x - 28, y - 28, x + 28, y + 28, fill=fill, outline=outline, width=3)
            self.canvas.create_text(x, y - 4, text=str(node), font=("Arial", 14, "bold"))

            distance = snapshot.distances[node]
            distance_text = "INF" if distance == float("inf") else str(distance)
            self.canvas.create_text(x, y + 18, text=distance_text, font=("Arial", 11), fill="#1d4ed8")


class DijkstraVisualizationApp:
    def __init__(self, graph, snapshots):
        self.graph = graph
        self.snapshots = snapshots
        self.index = 0

        self.root = tk.Tk()
        self.root.title("Dijkstra Visualization")

        self.title_label = tk.Label(
            self.root,
            text="Dijkstra Interactive Visualization",
            font=("Arial", 18, "bold"),
        )
        self.title_label.pack(pady=(12, 8))

        self.canvas = tk.Canvas(self.root, width=760, height=520, bg="#f8fafc", highlightthickness=0)
        self.canvas.pack(padx=16, pady=8)

        self.message_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 12),
            justify="left",
            anchor="w",
            width=90,
        )
        self.message_label.pack(padx=16, pady=(4, 8), anchor="w")

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=(0, 12))

        tk.Button(button_frame, text="Previous", width=12, command=self.previous_step).grid(row=0, column=0, padx=6)
        tk.Button(button_frame, text="Next", width=12, command=self.next_step).grid(row=0, column=1, padx=6)
        tk.Button(button_frame, text="Reset", width=12, command=self.reset).grid(row=0, column=2, padx=6)

        self.renderer = GraphRenderer(self.canvas, graph)
        self.render()

    def render(self):
        snapshot = self.snapshots[self.index]
        self.renderer.draw(snapshot)
        self.message_label.config(
            text=f"Step {self.index + 1} / {len(self.snapshots)}\n{snapshot.message}"
        )

    def previous_step(self):
        if self.index > 0:
            self.index -= 1
            self.render()

    def next_step(self):
        if self.index + 1 < len(self.snapshots):
            self.index += 1
            self.render()

    def reset(self):
        self.index = 0
        self.render()

    def run(self):
        self.root.mainloop()


def read_input():
    n, m, start = map(int, sys.stdin.readline().split())
    edges = [tuple(map(int, sys.stdin.readline().split())) for _ in range(m)]
    return n, start, edges


def format_distances(distances):
    return " ".join("INF" if value == float("inf") else str(value) for value in distances[1:])


def main():
    n, start, edges = read_input()
    graph = Graph(n, start, edges)
    tracer = DijkstraTracer(graph)
    distances, snapshots = tracer.run()
    print(format_distances(distances))

    if "--no-gui" in sys.argv:
        return

    try:
        app = DijkstraVisualizationApp(graph, snapshots)
        app.run()
    except tk.TclError:
        pass


if __name__ == "__main__":
    main()
