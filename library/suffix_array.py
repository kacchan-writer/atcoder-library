# AI生成: OpenAI Codex（2026-10-12）。参照資料・運用方針: PROVENANCE.md。
# Suffix Array・LCP
# 条件: SA-ISの線形実装ではない。空文字対応。Unicode文字もPythonの比較順で扱う。大規模には高速実装が必要。
# 計算量: このdoubling実装はO(N log^2(N+1))時間・O(N)空間。LCPはO(N)。
# API: suffix_array(s)、lcp_array(s,sa)。lcp[i]はsa[i]とsa[i+1]の一致長。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def suffix_array(s):
    n = len(s)
    values = {c: i for i, c in enumerate(sorted(set(s)))}
    rank, sa = [values[c] for c in s], list(range(n))
    width = 1
    while width < n:
        def key(i):
            return rank[i], rank[i+width] if i+width < n else -1
        sa.sort(key=key)
        nxt = [0] * n
        for j in range(1, n):
            nxt[sa[j]] = nxt[sa[j-1]] + (key(sa[j-1]) != key(sa[j]))
        rank = nxt
        if rank[sa[-1]] == n-1:
            break
        width *= 2
    return sa

def lcp_array(s, sa):
    n = len(s)
    if n <= 1:
        return []
    rank = [0] * n
    for r, i in enumerate(sa):
        rank[i] = r
    lcp, h = [0] * (n-1), 0
    for i in range(n):
        r = rank[i]
        if r == 0:
            h = 0
            continue
        j = sa[r-1]
        while i+h < n and j+h < n and s[i+h] == s[j+h]:
            h += 1
        lcp[r-1] = h
        h = max(0, h-1)
    return lcp


if __name__ == "__main__":
    sa = suffix_array('banana')
    print(sa)
    print(lcp_array('banana', sa))
