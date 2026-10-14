# ヒープ・上位K個の維持
# 条件: 要素がK未満なら全要素を採用。負数も含めて個数を優先する。削除は扱わない。
# 計算量: 追加O(log(K+1))、問合せO(1)、空間O(K)。
# API: TopK(k).add(x)、.total。heapqは最小ヒープ。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
import heapq

class TopK:
    def __init__(self, k):
        if k < 0:
            raise ValueError('k >= 0 が必要')
        self.k, self.heap, self.total = k, [], 0

    def add(self, x):
        if self.k == 0:
            return
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, x)
            self.total += x
        elif x > self.heap[0]:
            self.total += x - heapq.heapreplace(self.heap, x)


if __name__ == "__main__":
    top = TopK(2)
    for x in [3, 1, 5, 2]:
        top.add(x)
    print(top.total)
