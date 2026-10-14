# AI生成: OpenAI Codex（2026-10-12）。出典の確認範囲は PROVENANCE.md を参照。
# 0-1 BFS
# 条件: 0と1以外の重みは不可。未到達はinf。距離付きキューで古い候補を読み飛ばす。
# 計算量: O(V+E)時間、O(V+E)補助空間。
# API: zero_one_bfs(graph,start)。graph[v]は(行先,0または1)。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
from collections import deque

def zero_one_bfs(graph, start):
    dist = [float('inf')] * len(graph)
    dist[start] = 0
    queue = deque([(0, start)])
    while queue:
        d, v = queue.popleft()
        if d != dist[v]:
            continue
        for u, w in graph[v]:
            if d + w < dist[u]:
                dist[u] = d + w
                if w == 0:
                    queue.appendleft((d, u))
                else:
                    queue.append((d + 1, u))
    return dist


if __name__ == "__main__":
    print(zero_one_bfs([[(1, 1), (2, 0)], [], [(1, 0)]], 0))
