# ダブリング・LCA
# 条件: 空でない連結な無向木。ancestor(v,k)はk>=0、根を越えると-1。distanceは辺数。
# 計算量: 構築O(N log N)、各問合せO(log N)、空間O(N log N)。
# API: LCA(graph,root=0).lca(u,v)、ancestor(v,k)、distance(u,v)。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
class LCA:
    def __init__(self, graph, root=0):
        n = len(graph)
        parent = [-1] * n
        self.depth = [0] * n
        parent[root] = root
        order = [root]
        for v in order:
            for u in graph[v]:
                if u != parent[v]:
                    parent[u] = v
                    self.depth[u] = self.depth[v] + 1
                    order.append(u)
        self.up = [parent]
        for _ in range(1, n.bit_length()):
            prev = self.up[-1]
            self.up.append([prev[prev[v]] for v in range(n)])

    def ancestor(self, v, k):
        if k < 0:
            raise ValueError('k >= 0 が必要')
        if k > self.depth[v]:
            return -1
        bit = 0
        while k:
            if k & 1:
                v = self.up[bit][v]
            k >>= 1
            bit += 1
        return v

    def lca(self, u, v):
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        u = self.ancestor(u, self.depth[u] - self.depth[v])
        if u == v:
            return u
        for row in reversed(self.up):
            if row[u] != row[v]:
                u, v = row[u], row[v]
        return self.up[0][u]

    def distance(self, u, v):
        return self.depth[u] + self.depth[v] - 2 * self.depth[self.lca(u, v)]


if __name__ == "__main__":
    tree = LCA([[1, 2], [0, 3], [0], [1]])
    print(tree.lca(3, 2), tree.distance(3, 2), tree.ancestor(3, 1))
