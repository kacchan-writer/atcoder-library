# AI生成: OpenAI Codex（2026-10-12）。参照資料・運用方針: PROVENANCE.md。
# 部分集合ゼータ変換・Möbius反転 / SOS DP
# 条件: 長さは正の2冪。ここでは整数の和。単なる部分集合の総和と部分集合畳み込みは別。
# 計算量: Bビット、配列長N=2^BとしてO(B 2^B)時間、O(2^B)空間。
# API: subset_zeta(a)、subset_mobius(a)。元配列を変更せず新しいリストを返す。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def _transform(a, sign):
    n = len(a)
    if not n or n & (n - 1):
        raise ValueError('長さは正の2冪')
    result = list(a)
    bit = 1
    while bit < n:
        for mask in range(n):
            if mask & bit:
                result[mask] += sign * result[mask ^ bit]
        bit <<= 1
    return result

def subset_zeta(a):
    return _transform(a, 1)

def subset_mobius(a):
    return _transform(a, -1)


if __name__ == "__main__":
    print(subset_zeta([1, 2, 3, 4]))
    print(subset_mobius(subset_zeta([1, 2, 3, 4])))
