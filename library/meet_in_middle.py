# AI生成: OpenAI Codex（2026-10-12）。参照資料・運用方針: PROVENANCE.md。
# 半分全列挙
# 条件: 負数も可。空集合も含む。Pythonでは2^20個程度でもメモリ量に注意。
# 計算量: O(N 2^(N/2))時間、O(2^(N/2))空間（奇数Nは切上げ側）。
# API: subset_sums(a)、count_subset_sum(a,target)。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
from bisect import bisect_left, bisect_right

def subset_sums(a):
    sums = [0]
    for x in a:
        sums += [s + x for s in sums]
    return sums

def count_subset_sum(a, target):
    m = len(a) // 2
    left, right = subset_sums(a[:m]), sorted(subset_sums(a[m:]))
    return sum(bisect_right(right, target-s) - bisect_left(right, target-s) for s in left)


if __name__ == "__main__":
    print(count_subset_sum([1, 2, 3, 4], 5))
