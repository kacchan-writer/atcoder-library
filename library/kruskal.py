# AI生成: OpenAI Codex（2026-10-12）。参照資料・運用方針: PROVENANCE.md。
# 最小全域木・Kruskal法
# 条件: 負辺・多重辺可。非連結なら最小全域森になる。戻り値の辺数がn-1か確認する。
# 計算量: O(V+E log(E+1))時間、O(V+E)空間。
# API: kruskal(n,edges) -> (合計費用,採用辺)。edgesは(u,v,w)。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def kruskal(n, edges):
    parent = [-1] * n
    def root(v):
        while parent[v] >= 0:
            if parent[parent[v]] >= 0:
                parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    total, chosen = 0, []
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        a, b = root(u), root(v)
        if a == b:
            continue
        if parent[a] > parent[b]:
            a, b = b, a
        parent[a] += parent[b]
        parent[b] = a
        total += w
        chosen.append((u, v, w))
    return total, chosen


if __name__ == "__main__":
    print(kruskal(3, [(0, 1, 3), (1, 2, 1), (0, 2, 2)])[0])
