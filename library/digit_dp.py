# AI生成: OpenAI Codex（2026-10-12）。出典の確認範囲は PROVENANCE.md を参照。
# 桁DP
# 条件: 非負整数の十進文字列、D>=1、mod>=1。0は最後に除き、1..Nを数える。
# 計算量: L桁、剰余DとしてO(10LD)時間、O(D)空間。
# API: count_digit_sum_multiple(bound,divisor,mod=1000000007)。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def count_digit_sum_multiple(bound, divisor, mod=1000000007):
    if divisor < 1:
        raise ValueError('divisor >= 1 が必要')
    dp = [[0] * divisor for _ in range(2)]
    dp[1][0] = 1  # tight=1: ここまで上限と一致
    for ch in str(bound):
        limit = int(ch)
        nxt = [[0] * divisor for _ in range(2)]
        for tight in range(2):
            for r, ways in enumerate(dp[tight]):
                for digit in range((limit if tight else 9) + 1):
                    nt = int(tight and digit == limit)
                    nr = (r + digit) % divisor
                    nxt[nt][nr] = (nxt[nt][nr] + ways) % mod
        dp = nxt
    return (dp[0][0] + dp[1][0] - 1) % mod


if __name__ == "__main__":
    print(count_digit_sum_multiple('20', 3))
