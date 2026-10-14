# AI生成: OpenAI Codex（2026-10-12）。参照資料・運用方針: PROVENANCE.md。
# Union-Find / DSU
# 条件: 通常のDSUで辺の削除はできない。頂点は0..n-1。
# 計算量: 初期化O(N)。Q回の操作は合計O((N+Q) α(N))、空間O(N)。
# API: DSU(n)。merge(a,b)は併合したらTrue、same(a,b)、size(a)、leader(a)。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
class DSU:
    def __init__(self, n):
        self.parent = [-1] * n  # 根だけ負のサイズ、それ以外は親の添字

    def leader(self, a):
        root = a
        while self.parent[root] >= 0:
            root = self.parent[root]
        while a != root:
            nxt = self.parent[a]
            self.parent[a] = root
            a = nxt
        return root

    def merge(self, a, b):
        a, b = self.leader(a), self.leader(b)
        if a == b:
            return False
        if self.parent[a] > self.parent[b]:
            a, b = b, a
        self.parent[a] += self.parent[b]
        self.parent[b] = a
        return True

    def same(self, a, b):
        return self.leader(a) == self.leader(b)

    def size(self, a):
        return -self.parent[self.leader(a)]


if __name__ == "__main__":
    uf = DSU(4)
    uf.merge(0, 1)
    uf.merge(1, 2)
    print(uf.same(0, 2), uf.size(0), uf.same(0, 3))
