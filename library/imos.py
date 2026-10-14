# いもす法・差分配列
# 条件: 途中の問合せにはこのままでは対応できない。更新は0<=l<=r<=n。
# 計算量: O(N+Q)時間、O(N)空間。
# API: imos(n, updates)。updatesは(l,r,加算値)の列。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def imos(n, updates):
    diff = [0] * (n + 1)
    for l, r, x in updates:
        diff[l] += x
        diff[r] -= x
    a, current = [], 0
    for i in range(n):
        current += diff[i]
        a.append(current)
    return a


if __name__ == "__main__":
    print(imos(5, [(1, 4, 2), (2, 5, 1)]))
