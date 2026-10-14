# AI生成: OpenAI Codex（2026-10-12）。参照資料・運用方針: PROVENANCE.md。
# 凸包・単調鎖法
# 条件: 整数座標を想定。辺上の中間点は除く。全て一直線なら両端だけ。浮動小数点では誤差の設計が別途必要。
# 計算量: O(N log N)時間、O(N)空間。
# API: convex_hull(points) -> 反時計回りの頂点列。始点は末尾に重複しない。cross(o,a,b)は外積。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def cross(o, a, b):
    return (a[0]-o[0]) * (b[1]-o[1]) - (a[1]-o[1]) * (b[0]-o[0])

def convex_hull(points):
    points = sorted(set(map(tuple, points)))
    if len(points) <= 1:
        return points
    lower, upper = [], []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


if __name__ == "__main__":
    print(convex_hull([(0, 0), (2, 0), (2, 2), (0, 2), (1, 1)]))
