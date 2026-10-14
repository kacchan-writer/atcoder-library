# 最小費用流・ポテンシャル
# 条件: 元の辺の費用・容量は非負整数、s!=t。この実装は負費用の元辺に非対応。未達の場合は実際に流せた量を返す。
# 計算量: 増加回数AとしてO(A(V+(V+E) log(E+2)))時間、O(V+E)空間。整数容量ならA<=要求流量。
# API: min_cost_flow(n,edges,s,t,limit) -> (流量,総費用)。edgesは(u,v,容量,単位費用)。毎回新規計算。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
from heapq import heappush, heappop

def min_cost_flow(n, edges, s, t, limit):
    if s == t or limit < 0:
        raise ValueError('s != t, limit >= 0 が必要')
    graph = [[] for _ in range(n)]
    for u, v, cap, cost in edges:
        if cap < 0 or cost < 0:
            raise ValueError('元辺の容量・費用は非負')
        f = [v, len(graph[v]) + int(u == v), cap, cost]
        r = [u, len(graph[u]), 0, -cost]
        graph[u].append(f)
        graph[v].append(r)
    potential = [0] * n
    flow = total = 0
    inf = float('inf')
    while flow < limit:
        dist, previous = [inf] * n, [None] * n
        dist[s] = 0
        heap = [(0, s)]
        while heap:
            d, v = heappop(heap)
            if d != dist[v]:
                continue
            for i, (u, rev, cap, cost) in enumerate(graph[v]):
                nd = d + cost + potential[v] - potential[u]
                if cap > 0 and nd < dist[u]:
                    dist[u] = nd
                    previous[u] = (v, i)
                    heappush(heap, (nd, u))
        if dist[t] == inf:
            break
        for v in range(n):
            if dist[v] < inf:
                potential[v] += dist[v]
        amount, v = limit - flow, t
        while v != s:
            p, i = previous[v]
            amount = min(amount, graph[p][i][2])
            v = p
        v = t
        while v != s:
            p, i = previous[v]
            edge = graph[p][i]
            total += amount * edge[3]
            edge[2] -= amount
            graph[v][edge[1]][2] += amount
            v = p
        flow += amount
    return flow, total


if __name__ == "__main__":
    print(min_cost_flow(3, [(0, 1, 2, 1), (1, 2, 2, 3), (0, 2, 1, 7)], 0, 2, 3))
