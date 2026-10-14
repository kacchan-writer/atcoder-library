# AI生成: OpenAI Codex（2026-10-12）。参照資料・運用方針: PROVENANCE.md。
# 強連結成分分解 / SCC
# 条件: 成分番号は縮約DAGのトポロジカル順。異成分の辺v→uではid[v]<id[u]。無向の成分分解とは違う。
# 計算量: O(V+E)時間、O(V+E)空間。
# API: scc(graph) -> (各頂点の成分番号, 成分ごとの頂点リスト)。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def scc(graph):
    n = len(graph)
    reverse = [[] for _ in range(n)]
    for v, row in enumerate(graph):
        for u in row:
            reverse[u].append(v)
    seen, order = [False] * n, []
    for start in range(n):
        if seen[start]:
            continue
        seen[start] = True
        stack = [(start, 0)]
        while stack:
            v, i = stack[-1]
            if i == len(graph[v]):
                order.append(v)
                stack.pop()
            else:
                stack[-1] = (v, i + 1)
                u = graph[v][i]
                if not seen[u]:
                    seen[u] = True
                    stack.append((u, 0))
    ids, groups = [-1] * n, []
    for start in reversed(order):
        if ids[start] >= 0:
            continue
        group = []
        ids[start] = len(groups)
        stack = [start]
        while stack:
            v = stack.pop()
            group.append(v)
            for u in reverse[v]:
                if ids[u] < 0:
                    ids[u] = ids[start]
                    stack.append(u)
        groups.append(group)
    return ids, groups


if __name__ == "__main__":
    print(scc([[1], [0, 2], [3], [2]])[0])
