# AI生成: OpenAI Codex（2026-10-12）。出典の確認範囲は PROVENANCE.md を参照。
# セグメント木
# 条件: opは結合的、eは単位元。交換則は不要。区間更新はGの遅延セグ木へ。
# 計算量: 構築O(N)、更新・問合せO(log N)、空間O(N)。opがO(1)のとき。
# API: SegTree(a,op,e).set(i,x)、prod(l,r)。例: 和はop=lambda a,b:a+b、e=0。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
class SegTree:
    def __init__(self, a, op=min, e=float('inf')):
        self.n, self.op, self.e = len(a), op, e
        self.size = 1 << (max(1, len(a)) - 1).bit_length()
        self.data = [e] * (2 * self.size)
        self.data[self.size:self.size + len(a)] = a
        for i in range(self.size - 1, 0, -1):
            self.data[i] = op(self.data[i*2], self.data[i*2+1])

    def set(self, i, x):
        i += self.size
        self.data[i] = x
        while i > 1:
            i //= 2
            self.data[i] = self.op(self.data[i*2], self.data[i*2+1])

    def prod(self, l, r):
        left = right = self.e
        l, r = l + self.size, r + self.size
        while l < r:
            if l & 1:
                left = self.op(left, self.data[l])
                l += 1
            if r & 1:
                r -= 1
                right = self.op(self.data[r], right)
            l //= 2
            r //= 2
        return self.op(left, right)


if __name__ == "__main__":
    seg = SegTree([5, 2, 7, 1])
    print(seg.prod(1, 3))
    seg.set(1, 9)
    print(seg.prod(1, 3))
