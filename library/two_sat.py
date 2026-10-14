# AI生成: OpenAI Codex（2026-10-12）。参照資料・運用方針: PROVENANCE.md。
# 閲覧した参考仕様: https://atcoder.github.io/ac-library/master/document_ja/twosat.html
# 2-SAT
# 条件: 節は2リテラルまで。3-SATには使えない。このSCC実装の成分順に依存して割当を作る。
# 計算量: 変数N、節MとしてO(N+M)時間・空間。
# API: two_sat(n,clauses) -> bool列またはNone。節(i,f,j,g)は(x_i==f) OR (x_j==g)。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def scc(graph):
    n = len(graph)
    reverse = [[] for _ in range(n)]
    for v, row in enumerate(graph):
        for u in row:
            reverse[u].append(v)
    seen, order = [False] * n, []
    for start in range(n):
        if seen[start]:
            continue
        seen[start] = True
        stack = [(start, 0)]
        while stack:
            v, i = stack[-1]
            if i == len(graph[v]):
                order.append(v)
                stack.pop()
            else:
                stack[-1] = (v, i + 1)
                u = graph[v][i]
                if not seen[u]:
                    seen[u] = True
                    stack.append((u, 0))
    ids, groups = [-1] * n, []
    for start in reversed(order):
        if ids[start] >= 0:
            continue
        group = []
        ids[start] = len(groups)
        stack = [start]
        while stack:
            v = stack.pop()
            group.append(v)
            for u in reverse[v]:
                if ids[u] < 0:
                    ids[u] = ids[start]
                    stack.append(u)
        groups.append(group)
    return ids, groups


def two_sat(n, clauses):
    graph = [[] for _ in range(2 * n)]
    for i, f, j, g in clauses:
        a, b = 2 * i + int(f), 2 * j + int(g)
        graph[a ^ 1].append(b)
        graph[b ^ 1].append(a)
    ids, _ = scc(graph)
    if any(ids[2*i] == ids[2*i+1] for i in range(n)):
        return None
    return [ids[2*i] < ids[2*i+1] for i in range(n)]


if __name__ == "__main__":
    print(two_sat(1, [(0, True, 0, True)]))
