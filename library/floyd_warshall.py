# AI生成: OpenAI Codex（2026-10-12）。出典の確認範囲は PROVENANCE.md を参照。
# Warshall-Floyd法
# 条件: 負辺可。負閉路がある場合は最短距離として使えず、d[v][v]<0で検出できる。Pythonの大規模入力は重い。
# 計算量: O(V^3)時間、O(V^2)空間。
# API: floyd_warshall(n,edges,directed=True)。edgesは(u,v,w)、未到達inf。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def floyd_warshall(n, edges, directed=True):
    inf = float('inf')
    d = [[inf] * n for _ in range(n)]
    for v in range(n):
        d[v][v] = 0
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)
        if not directed:
            d[v][u] = min(d[v][u], w)
    for k in range(n):
        for i in range(n):
            if d[i][k] == inf:
                continue
            for j in range(n):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    return d


if __name__ == "__main__":
    print(floyd_warshall(3, [(0, 1, 4), (1, 2, -2), (0, 2, 5)])[0])
