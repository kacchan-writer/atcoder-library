# AI生成: OpenAI Codex（2026-10-12）。出典の確認範囲は PROVENANCE.md を参照。
# 閲覧した参考仕様: https://atcoder.github.io/ac-library/master/document_ja/maxflow.html
# 最大流・最小カット / Dinic
# 条件: 整数の非負容量、s!=t。flowは残余容量を変更し、追加で流れた量を返す。深いDFSも反復で処理。
# 計算量: 一般にO(V^2 E)時間、O(V+E)空間。
# API: Dinic(n).add_edge(u,v,cap)、flow(s,t)、min_cut(s) -> 到達可否。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
from collections import deque

class Dinic:
    def __init__(self, n):
        self.graph = [[] for _ in range(n)]

    def add_edge(self, u, v, cap):
        if cap < 0:
            raise ValueError('非負容量が必要')
        forward = [v, len(self.graph[v]) + int(u == v), cap]
        backward = [u, len(self.graph[u]), 0]
        self.graph[u].append(forward)
        self.graph[v].append(backward)

    def flow(self, s, t):
        if s == t:
            raise ValueError('s != t が必要')
        n, total = len(self.graph), 0
        while True:
            level = [-1] * n
            level[s] = 0
            queue = deque([s])
            while queue:
                v = queue.popleft()
                for u, rev, cap in self.graph[v]:
                    if cap > 0 and level[u] < 0:
                        level[u] = level[v] + 1
                        queue.append(u)
            if level[t] < 0:
                return total
            ptr = [0] * n
            while True:
                vertices, path = [s], []
                while vertices and vertices[-1] != t:
                    v = vertices[-1]
                    while ptr[v] < len(self.graph[v]):
                        u, rev, cap = self.graph[v][ptr[v]]
                        if cap > 0 and level[u] == level[v] + 1:
                            break
                        ptr[v] += 1
                    if ptr[v] == len(self.graph[v]):
                        level[v] = -1
                        vertices.pop()
                        if path:
                            pv, _ = path.pop()
                            ptr[pv] += 1
                    else:
                        path.append((v, ptr[v]))
                        vertices.append(self.graph[v][ptr[v]][0])
                if not vertices:
                    break
                amount = min(self.graph[v][i][2] for v, i in path)
                for v, i in path:
                    edge = self.graph[v][i]
                    edge[2] -= amount
                    self.graph[edge[0]][edge[1]][2] += amount
                total += amount

    def min_cut(self, s):
        seen = [False] * len(self.graph)
        seen[s] = True
        stack = [s]
        while stack:
            v = stack.pop()
            for u, rev, cap in self.graph[v]:
                if cap > 0 and not seen[u]:
                    seen[u] = True
                    stack.append(u)
        return seen


if __name__ == "__main__":
    net = Dinic(4)
    for edge in [(0, 1, 2), (0, 2, 1), (1, 3, 1), (2, 3, 2), (1, 2, 1)]:
        net.add_edge(*edge)
    print(net.flow(0, 3))
