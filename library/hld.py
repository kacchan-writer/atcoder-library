# Heavy-Light Decomposition / 重軽分解
# 条件: 空でない連結な無向木。頂点の値を足す。非可換演算や辺の値には向き・LCAの扱いを変更する。
# 計算量: この実装: 構築O(N log N)、一点加算O(log N)、経路和O(log^2 N)、空間O(N)。
# API: HLDPathSum(graph,values).add(v,x)、path_sum(u,v)。両端の頂点も含む。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
class HLDPathSum:
    def __init__(self, graph, values):
        n = len(graph)
        self.n = n
        self.parent, self.depth = [-1] * n, [0] * n
        self.parent[0] = 0
        order = [0]
        for v in order:
            for u in graph[v]:
                if u != self.parent[v]:
                    self.parent[u] = v
                    self.depth[u] = self.depth[v] + 1
                    order.append(u)
        size, heavy = [1] * n, [-1] * n
        for v in reversed(order):
            for u in graph[v]:
                if u != self.parent[v]:
                    size[v] += size[u]
                    if heavy[v] < 0 or size[u] > size[heavy[v]]:
                        heavy[v] = u
        self.head, self.pos = [0] * n, [0] * n
        stack, timer = [(0, 0)], 0
        while stack:
            v, h = stack.pop()
            while v >= 0:
                self.head[v], self.pos[v] = h, timer
                timer += 1
                for u in graph[v]:
                    if u != self.parent[v] and u != heavy[v]:
                        stack.append((u, u))
                v = heavy[v]
        self.bit = [0] * (n + 1)
        for v, x in enumerate(values):
            self.add(v, x)

    def add(self, v, x):
        i = self.pos[v] + 1
        while i <= self.n:
            self.bit[i] += x
            i += i & -i

    def _prefix(self, r):
        total = 0
        while r:
            total += self.bit[r]
            r -= r & -r
        return total

    def path_sum(self, u, v):
        total = 0
        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] < self.depth[self.head[v]]:
                u, v = v, u
            h = self.head[u]
            total += self._prefix(self.pos[u] + 1) - self._prefix(self.pos[h])
            u = self.parent[h]
        l, r = sorted((self.pos[u], self.pos[v]))
        return total + self._prefix(r + 1) - self._prefix(l)


if __name__ == "__main__":
    tree = HLDPathSum([[1, 2], [0, 3], [0], [1]], [1, 2, 3, 4])
    print(tree.path_sum(2, 3))
    tree.add(1, 10)
    print(tree.path_sum(2, 3))
