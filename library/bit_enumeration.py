# bit全探索
# 条件: この実装は空集合を含む。負数も可。Nが30以上だと単純全探索は重い。
# 計算量: O(N 2^N)時間、補助空間O(1)。
# API: count_subset_sum(a,target) -> 合計がtargetになる部分集合の個数。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def count_subset_sum(a, target):
    answer = 0
    for mask in range(1 << len(a)):
        total = 0
        for i, x in enumerate(a):
            if mask >> i & 1:
                total += x
        answer += total == target
    return answer


if __name__ == "__main__":
    print(count_subset_sum([1, 2, 3], 3))
