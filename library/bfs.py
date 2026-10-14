# AI生成: OpenAI Codex（2026-10-12）。参照資料・運用方針: PROVENANCE.md。
# BFS・多始点BFS
# 条件: 重み付きにはDijkstra等を使う。未到達は-1。gridは長方形で#を壁とする。
# 計算量: O(V+E)時間、O(V)補助空間。
# API: bfs(graph,sources) -> 距離。grid_bfs(grid,start) -> 四近傍距離。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
from collections import deque

def bfs(graph, sources):
    dist = [-1] * len(graph)
    queue = deque()
    for s in sources:
        if dist[s] == -1:
            dist[s] = 0
            queue.append(s)
    while queue:
        v = queue.popleft()
        for u in graph[v]:
            if dist[u] == -1:
                dist[u] = dist[v] + 1
                queue.append(u)
    return dist

def grid_bfs(grid, start):
    h, w = len(grid), len(grid[0])
    dist = [[-1] * w for _ in range(h)]
    sy, sx = start
    if grid[sy][sx] == '#':
        return dist
    dist[sy][sx] = 0
    queue = deque([start])
    while queue:
        y, x = queue.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and grid[ny][nx] != '#' and dist[ny][nx] < 0:
                dist[ny][nx] = dist[y][x] + 1
                queue.append((ny, nx))
    return dist


if __name__ == "__main__":
    print(bfs([[1], [0, 2], [1], []], [0]))
