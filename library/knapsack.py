# AI生成: OpenAI Codex（2026-10-12）。参照資料・運用方針: PROVENANCE.md。
# 動的計画法・0/1ナップサック
# 条件: 重量は非負整数、W>=0。空選択可。昇順更新は同じ品物を再利用してしまう（重さ>0の場合）。
# 計算量: O(NW)時間、O(W)空間。
# API: knapsack(items,capacity)。itemsは(重量,価値)の列。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def knapsack(items, capacity):
    dp = [0] * (capacity + 1)
    for weight, value in items:
        for w in range(capacity, weight - 1, -1):
            dp[w] = max(dp[w], dp[w - weight] + value)
    return dp[capacity]


if __name__ == "__main__":
    print(knapsack([(2, 3), (3, 4), (4, 6)], 5))
