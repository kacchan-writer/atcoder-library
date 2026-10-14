# 遅延セグメント木・区間加算と区間和
# 条件: ここでは加算と和に特化。代入・affine変換ではlazyの合成順や区間長の扱いを別に設計する。
# 計算量: 構築O(N)、区間更新・問合せO(log N)、空間O(N)。
# API: RangeAddSum(a).add(l,r,x)、sum(l,r)。再帰の深さはO(log N)。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
class RangeAddSum:
    def __init__(self, a):
        self.size = 1 << (max(1, len(a)) - 1).bit_length()
        self.data = [0] * (2 * self.size)
        self.lazy = [0] * (2 * self.size)
        self.data[self.size:self.size+len(a)] = a
        for k in range(self.size - 1, 0, -1):
            self.data[k] = self.data[2*k] + self.data[2*k+1]

    def _apply(self, k, width, x):
        self.data[k] += width * x
        self.lazy[k] += x

    def _push(self, k, width):
        if self.lazy[k] and width > 1:
            self._apply(2*k, width//2, self.lazy[k])
            self._apply(2*k+1, width//2, self.lazy[k])
            self.lazy[k] = 0

    def add(self, l, r, x):
        def visit(k, a, b):
            if r <= a or b <= l:
                return
            if l <= a and b <= r:
                self._apply(k, b-a, x)
                return
            self._push(k, b-a)
            m = (a+b)//2
            visit(2*k, a, m)
            visit(2*k+1, m, b)
            self.data[k] = self.data[2*k] + self.data[2*k+1]
        visit(1, 0, self.size)

    def sum(self, l, r):
        def visit(k, a, b):
            if r <= a or b <= l:
                return 0
            if l <= a and b <= r:
                return self.data[k]
            self._push(k, b-a)
            m = (a+b)//2
            return visit(2*k, a, m) + visit(2*k+1, m, b)
        return visit(1, 0, self.size)


if __name__ == "__main__":
    tree = RangeAddSum([1, 2, 3, 4])
    tree.add(1, 4, 2)
    print(tree.sum(0, 3))
