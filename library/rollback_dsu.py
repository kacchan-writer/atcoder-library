# Rollback Union-Find
# 条件: 経路圧縮をしない。snapshotは現在の履歴の祖先だけに戻せる。任意の辺削除を直接処理する構造ではない。
# 計算量: leader/merge O(log N)、snapshot O(1)、rollbackは取り消す併合数O(K)、空間O(N+履歴)。
# API: RollbackDSU(n).merge(a,b)、same(a,b)、snapshot()、rollback(token)。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
class RollbackDSU:
    def __init__(self, n):
        self.parent, self.history = [-1] * n, []

    def leader(self, v):
        while self.parent[v] >= 0:
            v = self.parent[v]
        return v

    def same(self, a, b):
        return self.leader(a) == self.leader(b)

    def merge(self, a, b):
        a, b = self.leader(a), self.leader(b)
        if a == b:
            return False
        if self.parent[a] > self.parent[b]:
            a, b = b, a
        self.history.append((a, self.parent[a], b, self.parent[b]))
        self.parent[a] += self.parent[b]
        self.parent[b] = a
        return True

    def snapshot(self):
        return len(self.history)

    def rollback(self, token):
        if not 0 <= token <= len(self.history):
            raise ValueError('現在の履歴内のsnapshotが必要')
        while len(self.history) > token:
            a, pa, b, pb = self.history.pop()
            self.parent[a], self.parent[b] = pa, pb


if __name__ == "__main__":
    uf = RollbackDSU(3)
    uf.merge(0, 1)
    token = uf.snapshot()
    uf.merge(1, 2)
    print(uf.same(0, 2))
    uf.rollback(token)
    print(uf.same(0, 2))
