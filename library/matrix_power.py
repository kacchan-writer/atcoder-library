# AI生成: OpenAI Codex（2026-10-12）。参照資料・運用方針: PROVENANCE.md。
# 行列累乗
# 条件: 正方行列、指数T>=0、mod>=1。行・列ベクトルの向きを統一する。Pythonの大きなKには重い。
# 計算量: K×K行列をT乗: O(K^3 log(T+1))時間、O(K^2)空間。
# API: matmul(a,b,mod)、matpow(a,exponent,mod=1000000007)。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def matmul(a, b, mod):
    n = len(a)
    c = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if a[i][k]:
                for j in range(n):
                    c[i][j] = (c[i][j] + a[i][k] * b[k][j]) % mod
    return c

def matpow(a, exponent, mod=1000000007):
    if exponent < 0:
        raise ValueError('exponent >= 0 が必要')
    n = len(a)
    result = [[int(i == j) % mod for j in range(n)] for i in range(n)]
    while exponent:
        if exponent & 1:
            result = matmul(result, a, mod)
        a = matmul(a, a, mod)
        exponent >>= 1
    return result


if __name__ == "__main__":
    print(matpow([[1, 1], [1, 0]], 5))
