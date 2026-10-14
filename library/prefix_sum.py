# 累積和・二次元累積和
# 条件: 更新には不向き。二次元は長方形のリストを渡す。負数も扱える。
# 計算量: 一次元: 構築O(N)、問合せO(1)、空間O(N)。二次元: 構築・空間O(HW)、問合せO(1)。
# API: prefix_sum(a)、range_sum(p,l,r)、prefix_sum_2d(grid)、rect_sum(p,top,left,bottom,right)。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def prefix_sum(a):
    p = [0]
    for x in a:
        p.append(p[-1] + x)
    return p

def range_sum(p, l, r):
    return p[r] - p[l]

def prefix_sum_2d(grid):
    h, w = len(grid), len(grid[0]) if grid else 0
    p = [[0] * (w + 1) for _ in range(h + 1)]
    for i in range(h):
        for j in range(w):
            p[i+1][j+1] = grid[i][j] + p[i][j+1] + p[i+1][j] - p[i][j]
    return p

def rect_sum(p, top, left, bottom, right):
    return p[bottom][right] - p[top][right] - p[bottom][left] + p[top][left]


if __name__ == "__main__":
    print(range_sum(prefix_sum([2, -1, 4, 3]), 1, 4))
    print(rect_sum(prefix_sum_2d([[1, 2], [3, 4]]), 0, 1, 2, 2))
