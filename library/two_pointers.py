# AI生成: OpenAI Codex（2026-10-12）。出典の確認範囲は PROVENANCE.md を参照。
# 尺取り法
# 条件: aの全要素が非負であること。負数があるなら累積和+辞書などを検討。空区間は数えない。
# 計算量: O(N)時間、O(1)補助空間。
# API: count_sum_at_most(a,k)。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def count_sum_at_most(a, k):
    if k < 0:
        return 0
    left = total = answer = 0
    for right, x in enumerate(a):
        total += x
        while total > k:
            total -= a[left]
            left += 1
        answer += right - left + 1
    return answer


if __name__ == "__main__":
    print(count_sum_at_most([1, 2, 1], 3))
