# AI生成: OpenAI Codex（2026-10-12）。参照資料・運用方針: PROVENANCE.md。
# 閲覧した参考仕様: https://atcoder.github.io/ac-library/master/document_ja/convolution.html
# NTT・畳み込み
# 条件: modは998244353固定。必要長<=2^23。整数そのままの畳み込みではなくmodを取った結果。Pythonの最大長実行は非現実的。
# 計算量: 必要な2冪長をLとしてO(L log L)時間、O(L)空間。
# API: convolution(a,b) -> 長さlen(a)+len(b)-1の係数。空列を含むと[]。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
MOD = 998244353

def _ntt(a, inverse=False):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    width = 2
    while width <= n:
        root = pow(3, (MOD - 1) // width, MOD)
        if inverse:
            root = pow(root, MOD - 2, MOD)
        half = width // 2
        for left in range(0, n, width):
            w = 1
            for i in range(left, left + half):
                u, v = a[i], a[i+half] * w % MOD
                a[i], a[i+half] = (u+v) % MOD, (u-v) % MOD
                w = w * root % MOD
        width *= 2
    if inverse:
        scale = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * scale % MOD

def convolution(a, b):
    if not a or not b:
        return []
    length = len(a) + len(b) - 1
    n = 1 << (length - 1).bit_length()
    if n > 1 << 23:
        raise ValueError('NTT長は2^23以下')
    fa = [x % MOD for x in a] + [0] * (n-len(a))
    fb = [x % MOD for x in b] + [0] * (n-len(b))
    _ntt(fa)
    _ntt(fb)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD
    _ntt(fa, True)
    return fa[:length]


if __name__ == "__main__":
    print(convolution([1, 2, 3], [4, 5]))
