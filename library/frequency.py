# AI生成: OpenAI Codex（2026-10-12）。参照資料・運用方針: PROVENANCE.md。
# 辞書・出現回数・同じ値のペア
# 条件: キーはハッシュ可能な値。辞書のO(1)は平均計算量。
# 計算量: 平均O(N)時間、O(K)空間。Kは異なる値の数。
# API: equal_pairs(a) -> 同値ペア数。Counter(a) -> 値ごとの頻度。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
from collections import Counter

def equal_pairs(a):
    count = {}
    answer = 0
    for x in a:
        answer += count.get(x, 0)  # 自分自身を入れるより先に数える
        count[x] = count.get(x, 0) + 1
    return answer


if __name__ == "__main__":
    print(equal_pairs([3, 1, 3, 3, 1]))
