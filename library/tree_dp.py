# AI生成: OpenAI Codex（2026-10-12）。参照資料・運用方針: PROVENANCE.md。
# 木DP・独立集合の数え上げ
# 条件: 連結な無向木、mod>=1。空集合も数える。空グラフは1通り。一般グラフには流用不可。
# 計算量: O(N)時間、O(N)空間。
# API: independent_sets(graph,mod=1000000007)。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def independent_sets(graph, mod=1000000007):
    n = len(graph)
    if n == 0:
        return 1 % mod
    parent = [-1] * n
    parent[0] = 0
    order = [0]
    for v in order:
        for u in graph[v]:
            if u != parent[v]:
                parent[u] = v
                order.append(u)
    white, black = [1] * n, [1] * n
    for v in reversed(order):
        for u in graph[v]:
            if u != parent[v]:
                white[v] = white[v] * (white[u] + black[u]) % mod
                black[v] = black[v] * white[u] % mod
    return (white[0] + black[0]) % mod


if __name__ == "__main__":
    print(independent_sets([[1], [0, 2], [1]]))
