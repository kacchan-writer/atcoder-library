# AI生成: OpenAI Codex（2026-10-12）。出典の確認範囲は PROVENANCE.md を参照。
# Z algorithm・文字列の前方一致
# 条件: 空列は[]、非空ではz[0]=N。文字列以外の比較可能な列でも可。
# 計算量: O(N)時間、O(N)空間。
# API: z_algorithm(s) -> 各suffixとsの最長共通接頭辞の長さ。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def z_algorithm(s):
    n = len(s)
    if not n:
        return []
    z = [0] * n
    z[0] = n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i-l])
        while i + z[i] < n and s[z[i]] == s[i+z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z


if __name__ == "__main__":
    print(z_algorithm('aabcaab'))
