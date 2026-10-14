# 累積和＋辞書
# 条件: 初期値0を1個登録。現在の累積和を登録する前に答えを加算し、空区間を避ける。
# 計算量: 平均O(N)時間、O(N)空間。
# API: count_sum_equal(a,k)。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def count_sum_equal(a, k):
    seen = {0: 1}
    total = answer = 0
    for x in a:
        total += x
        answer += seen.get(total - k, 0)
        seen[total] = seen.get(total, 0) + 1
    return answer


if __name__ == "__main__":
    print(count_sum_equal([1, -1, 1], 1))
