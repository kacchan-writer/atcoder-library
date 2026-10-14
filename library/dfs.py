# AI生成: OpenAI Codex（2026-10-12）。参照資料・運用方針: PROVENANCE.md。
# DFS・連結成分・木の帰りがけ順
# 条件: componentsは無向グラフ用。tree_orderは空でない連結な木専用。再帰を使わない。
# 計算量: O(V+E)時間、O(V)補助空間。
# API: components(graph) -> 成分番号。tree_order(graph,root) -> (親配列,親が先の順序)。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def components(graph):
    label = [-1] * len(graph)
    number = 0
    for s in range(len(graph)):
        if label[s] >= 0:
            continue
        label[s] = number
        stack = [s]
        while stack:
            v = stack.pop()
            for u in graph[v]:
                if label[u] < 0:
                    label[u] = number
                    stack.append(u)
        number += 1
    return label

def tree_order(graph, root=0):
    parent = [-1] * len(graph)
    parent[root] = root
    order = [root]
    for v in order:
        for u in graph[v]:
            if u != parent[v]:
                parent[u] = v
                order.append(u)
    return parent, order


if __name__ == "__main__":
    print(components([[1], [0], [3], [2], []]))
