# AI生成: OpenAI Codex（2026-10-12）。出典の確認範囲は PROVENANCE.md を参照。
# 区間DP・隣接併合
# 条件: 隣接併合専用。N=0,1なら0。全ての組から選ぶ併合問題とは別。大規模には最適化が必要。
# 計算量: O(N^3)時間、O(N^2)空間。
# API: merge_cost(a) -> 最小総費用。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def merge_cost(a):
    n = len(a)
    p = [0]
    for x in a:
        p.append(p[-1] + x)
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    for width in range(2, n + 1):
        for l in range(n - width + 1):
            r = l + width
            dp[l][r] = min(dp[l][k] + dp[k][r] for k in range(l+1, r)) + p[r] - p[l]
    return dp[0][n]


if __name__ == "__main__":
    print(merge_cost([10, 20, 30]))
