# 組合せ・階乗・逆元
# 条件: pは素数、0<=N<pが必須。素数判定はしない。N>=pや合成数modには流用不可。
# 計算量: 前計算O(N+log p)、問合せO(1)、空間O(N)。
# API: Combinations(N,mod).choose(n,r)。0<=n<=N、範囲外のrは0。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
class Combinations:
    def __init__(self, n, mod=998244353):
        if not 0 <= n < mod:
            raise ValueError('0 <= n < mod が必要')
        self.mod = mod
        self.fact = [1] * (n + 1)
        for i in range(1, n + 1):
            self.fact[i] = self.fact[i-1] * i % mod
        self.invfact = [1] * (n + 1)
        self.invfact[n] = pow(self.fact[n], mod - 2, mod)
        for i in range(n, 0, -1):
            self.invfact[i-1] = self.invfact[i] * i % mod

    def choose(self, n, r):
        if r < 0 or r > n:
            return 0
        return self.fact[n] * self.invfact[r] % self.mod * self.invfact[n-r] % self.mod


if __name__ == "__main__":
    print(Combinations(10).choose(5, 2))
