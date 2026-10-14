# AI生成: OpenAI Codex（2026-10-12）。出典の確認範囲は PROVENANCE.md を参照。
# トポロジカルソート・DAG上のDP
# 条件: 有向グラフ用。longest_pathは辺数の最大値で、空グラフは0。閉路時はValueError。
# 計算量: O(V+E)時間、O(V)補助空間。
# API: topological_sort(graph) -> 順序またはNone。longest_path(graph)。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
from collections import deque

def topological_sort(graph):
    indegree = [0] * len(graph)
    for row in graph:
        for u in row:
            indegree[u] += 1
    queue = deque(v for v, d in enumerate(indegree) if d == 0)
    order = []
    while queue:
        v = queue.popleft()
        order.append(v)
        for u in graph[v]:
            indegree[u] -= 1
            if indegree[u] == 0:
                queue.append(u)
    return order if len(order) == len(graph) else None

def longest_path(graph):
    order = topological_sort(graph)
    if order is None:
        raise ValueError('DAGが必要')
    dp = [0] * len(graph)
    for v in order:
        for u in graph[v]:
            dp[u] = max(dp[u], dp[v] + 1)
    return max(dp, default=0)


if __name__ == "__main__":
    print(longest_path([[1, 2], [2], []]))
