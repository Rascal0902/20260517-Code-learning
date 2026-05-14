import heapq


def build_graph(n, edges):
    graph = [[] for _ in range(n + 1)]
    for u, v, w in edges:
        graph[u].append((v, w))
    return graph


def dijkstra(n, graph, start):
    distances = [float("inf")] * (n + 1)
    distances[start] = 0

    heap = [(0, start)]

    while heap:
        current_distance, node = heapq.heappop(heap)
        if current_distance > distances[node]:
            continue

        for neighbor, weight in graph[node]:
            candidate = current_distance + weight
            if candidate >= distances[neighbor]:
                continue

            distances[neighbor] = candidate
            heapq.heappush(heap, (candidate, neighbor))

    return distances


def format_distances(distances):
    result = []
    for value in distances[1:]:
        result.append("INF" if value == float("inf") else str(value))
    return " ".join(result)


if __name__ == "__main__":
    n, m, start = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    graph = build_graph(n, edges)
    distances = dijkstra(n, graph, start)
    print(format_distances(distances))
