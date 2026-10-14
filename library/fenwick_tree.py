# AI生成: OpenAI Codex（2026-10-12）。出典の確認範囲は PROVENANCE.md を参照。
# Fenwick Tree / BIT・転倒数
# 条件: 外部添字は0始まり、内部だけ1始まり。同値は転倒に数えない。
# 計算量: 初期化O(N)、更新・和O(log N)、空間O(N)。転倒数O(N log(N+1))。
# API: Fenwick(n).add(i,x)、prefix(r)、sum(l,r)。inversions(a)。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
class Fenwick:
    def __init__(self, n):
        self.n, self.bit = n, [0] * (n + 1)

    def add(self, i, x):
        if not 0 <= i < self.n:
            raise IndexError(i)
        i += 1
        while i <= self.n:
            self.bit[i] += x
            i += i & -i

    def prefix(self, r):
        result = 0
        while r:
            result += self.bit[r]
            r -= r & -r
        return result

    def sum(self, l, r):
        return self.prefix(r) - self.prefix(l)

def inversions(a):
    rank = {x: i for i, x in enumerate(sorted(set(a)))}
    tree = Fenwick(len(rank))
    result = 0
    for i, x in enumerate(a):
        r = rank[x]
        result += i - tree.prefix(r + 1)
        tree.add(r, 1)
    return result


if __name__ == "__main__":
    print(inversions([3, 1, 2, 2]))
