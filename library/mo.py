# Moのアルゴリズム・区間の種類数
# 条件: オンライン問合せや途中の値変更にはこの実装は使えない。空区間可。値はハッシュ可能。
# 計算量: B≈sqrt(N)としてO(Q log Q + QB + N^2/B)時間、O(N+Q)空間。
# API: distinct_queries(a,queries) -> 入力順の答え。queriesは(l,r)。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
from math import isqrt

def distinct_queries(a, queries):
    block = max(1, isqrt(len(a)))
    order = sorted(range(len(queries)), key=lambda i: (
        queries[i][0] // block,
        queries[i][1] * (-1 if queries[i][0] // block % 2 else 1)))
    count, distinct = {}, 0
    left = right = 0
    answer = [0] * len(queries)
    def add(i):
        nonlocal distinct
        x = a[i]
        if count.get(x, 0) == 0:
            distinct += 1
        count[x] = count.get(x, 0) + 1
    def remove(i):
        nonlocal distinct
        x = a[i]
        count[x] -= 1
        if count[x] == 0:
            distinct -= 1
    for i in order:
        l, r = queries[i]
        while left > l:
            left -= 1
            add(left)
        while right < r:
            add(right)
            right += 1
        while left < l:
            remove(left)
            left += 1
        while right > r:
            right -= 1
            remove(right)
        answer[i] = distinct
    return answer


if __name__ == "__main__":
    print(distinct_queries([1, 2, 1, 3], [(0, 3), (1, 4), (2, 2)]))
