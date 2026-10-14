# AI生成: OpenAI Codex（2026-10-12）。参照資料・運用方針: PROVENANCE.md。
# 二部マッチング・増加路
# 条件: 二部グラフ専用。一般グラフにはBlossom等が必要。大規模にはHopcroft-Karpを検討。
# 計算量: 左L、右RとしてO(L(L+R+E))時間、O(L+R)補助空間。
# API: matching(graph,right_size) -> (個数,各左頂点の相手)。graphは左→右の隣接リスト、未割当-1。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
from collections import deque

def matching(graph, right_size):
    left_match, right_match = [-1] * len(graph), [-1] * right_size
    count = 0
    for start in range(len(graph)):
        seen_left = [False] * len(graph)
        parent_right = [-1] * right_size
        seen_left[start] = True
        queue = deque([start])
        end = -1
        while queue and end < 0:
            v = queue.popleft()
            for u in graph[v]:
                if parent_right[u] >= 0:
                    continue
                parent_right[u] = v
                if right_match[u] < 0:
                    end = u
                    break
                nxt = right_match[u]
                if not seen_left[nxt]:
                    seen_left[nxt] = True
                    queue.append(nxt)
        if end < 0:
            continue
        count += 1
        while end >= 0:
            v = parent_right[end]
            previous = left_match[v]
            left_match[v] = end
            right_match[end] = v
            end = previous
    return count, left_match


if __name__ == "__main__":
    print(matching([[0, 1], [0], [1, 2]], 3)[0])
