# AI生成: OpenAI Codex（2026-10-12）。参照資料・運用方針: PROVENANCE.md。
# bit DP・巡回セールスマン
# 条件: 0始点で全頂点を一度ずつ訪れ0へ戻る。有向も可、欠辺はinf。N=0,1は移動なしで0。
# 計算量: O(N^2 2^N)時間、O(N 2^N)空間。
# API: tsp(cost) -> 最小巡回費用またはinf。costはN×N。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def tsp(cost):
    n = len(cost)
    if n <= 1:
        return 0
    inf = float('inf')
    dp = [[inf] * n for _ in range(1 << n)]
    dp[1][0] = 0
    for mask in range(1 << n):
        for v in range(n):
            if dp[mask][v] == inf:
                continue
            for u in range(n):
                if not (mask >> u & 1):
                    nxt = mask | (1 << u)
                    dp[nxt][u] = min(dp[nxt][u], dp[mask][v] + cost[v][u])
    return min(dp[-1][v] + cost[v][0] for v in range(1, n))


if __name__ == "__main__":
    print(tsp([[0, 2, 4], [2, 0, 3], [4, 3, 0]]))
