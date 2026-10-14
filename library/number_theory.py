# AI生成: OpenAI Codex（2026-10-12）。出典の確認範囲は PROVENANCE.md を参照。
# GCD・約数列挙・素数のふるい
# 条件: divisorsはn>=1。sieveはn>=0。0の約数列挙は定義しない。
# 計算量: gcd: O(log min(a,b))。約数: O(sqrt(n)+D log D)時間・O(D)空間。ふるい: O(N log log N)時間・O(N)空間。
# API: gcd(a,b)、lcm(a,b)、divisors(n)、sieve(n) -> n以下の素数リスト。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
from math import gcd, lcm, isqrt

def divisors(n):
    if n < 1:
        raise ValueError('n >= 1 が必要')
    result = []
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            result.append(d)
            if d * d != n:
                result.append(n // d)
    return sorted(result)

def sieve(n):
    prime = [True] * (n + 1)
    if n >= 0:
        prime[0] = False
    if n >= 1:
        prime[1] = False
    for p in range(2, isqrt(n) + 1):
        if prime[p]:
            for x in range(p * p, n + 1, p):
                prime[x] = False
    return [i for i, ok in enumerate(prime) if ok]


if __name__ == "__main__":
    print(gcd(12, 18), lcm(12, 18))
    print(divisors(12))
    print(sieve(12))
