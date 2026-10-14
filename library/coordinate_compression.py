# AI生成: OpenAI Codex（2026-10-12）。参照資料・運用方針: PROVENANCE.md。
# 座標圧縮
# 条件: 距離は保存しない。面積・長さには元の座標差が必要。
# 計算量: O(N log N)時間、O(N)空間。
# API: compress(a) -> (圧縮後の列, 番号から元の値へ戻す列)。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def compress(a):
    values = sorted(set(a))
    rank = {x: i for i, x in enumerate(values)}
    return [rank[x] for x in a], values


if __name__ == "__main__":
    print(compress([100, -5, 100, 7]))
