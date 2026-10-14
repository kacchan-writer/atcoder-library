# 最長増加部分列 / LIS
# 条件: 同値を伸ばさない狭義増加。非減少ならbisect_rightに変更。tailsそのものは復元解とは限らない。
# 計算量: O(N log(N+1))時間、O(N)空間。
# API: lis_length(a) -> 長さ。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
from bisect import bisect_left

def lis_length(a):
    tails = []
    for x in a:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)


if __name__ == "__main__":
    print(lis_length([3, 1, 2, 2, 5, 4]))
