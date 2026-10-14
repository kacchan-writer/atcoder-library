# Li Chao Tree・直線の最小値
# 条件: 問合せ座標を事前に全て渡す離散版。任意の曲線には使えない。直線がなければinf。
# 計算量: 座標M個: 準備O(M log M)、直線追加・問合せO(log(M+1))、空間O(M)。
# API: LiChao(xs).add_line(a,b)、query(x)。xは初期xs内の値。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
from bisect import bisect_left

class LiChao:
    def __init__(self, xs):
        self.xs = sorted(set(xs))
        if not self.xs:
            raise ValueError('座標が1個以上必要')
        self.lines = [None] * (4 * len(self.xs))

    def add_line(self, a, b):
        def put(k, l, r, line):
            if self.lines[k] is None:
                self.lines[k] = line
                return
            m = (l + r) // 2
            current = self.lines[k]
            left_better = line[0] * self.xs[l] + line[1] < current[0] * self.xs[l] + current[1]
            mid_better = line[0] * self.xs[m] + line[1] < current[0] * self.xs[m] + current[1]
            if mid_better:
                self.lines[k], line = line, current
            if r-l == 1:
                return
            if left_better != mid_better:
                put(2*k, l, m, line)
            else:
                put(2*k+1, m, r, line)
        put(1, 0, len(self.xs), (a, b))

    def query(self, x):
        i = bisect_left(self.xs, x)
        if i == len(self.xs) or self.xs[i] != x:
            raise ValueError('初期座標にないx')
        k, l, r, result = 1, 0, len(self.xs), float('inf')
        while True:
            line = self.lines[k]
            if line is not None:
                result = min(result, line[0] * x + line[1])
            if r-l == 1:
                return result
            m = (l+r)//2
            if i < m:
                k, r = 2*k, m
            else:
                k, l = 2*k+1, m


if __name__ == "__main__":
    tree = LiChao([-2, 0, 3])
    tree.add_line(2, 1)
    tree.add_line(-1, 4)
    print([tree.query(x) for x in [-2, 0, 3]])
