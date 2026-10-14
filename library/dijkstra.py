# AI生成: OpenAI Codex（2026-10-12）。参照資料・運用方針: PROVENANCE.md。
# Dijkstra法
# 条件: 負辺は不可。未到達はfloat("inf")。ヒープの古い距離を読み飛ばす。
# 計算量: O(V+(V+E) log(E+2))時間、O(V+E)補助空間。
# API: dijkstra(graph,start)。graph[v]は(行先,重み)の列。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
from heapq import heappush, heappop

def dijkstra(graph, start):
    dist = [float('inf')] * len(graph)
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        d, v = heappop(heap)
        if d != dist[v]:
            continue
        for u, cost in graph[v]:
            nd = d + cost
            if nd < dist[u]:
                dist[u] = nd
                heappush(heap, (nd, u))
    return dist


if __name__ == "__main__":
    print(dijkstra([[(1, 5), (2, 1)], [], [(1, 2)]], 0))
