# AI生成: OpenAI Codex（2026-10-12）。出典の確認範囲は PROVENANCE.md を参照。
# 全方位木DP・全頂点からの距離和
# 条件: 連結な無向・重みなしの木。一般の全方位木DPでは除外計算用のprefix/suffixも設計する。
# 計算量: O(N)時間、O(N)空間。
# API: all_distance_sums(graph) -> 各頂点から全頂点への距離和。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def all_distance_sums(graph):
    n = len(graph)
    if not n:
        return []
    parent, depth = [-1] * n, [0] * n
    parent[0] = 0
    order = [0]
    for v in order:
        for u in graph[v]:
            if u != parent[v]:
                parent[u] = v
                depth[u] = depth[v] + 1
                order.append(u)
    size = [1] * n
    for v in reversed(order[1:]):
        size[parent[v]] += size[v]
    answer = [0] * n
    answer[0] = sum(depth)
    for u in order[1:]:
        answer[u] = answer[parent[u]] + n - 2 * size[u]
    return answer


if __name__ == "__main__":
    print(all_distance_sums([[1], [0, 2], [1]]))
