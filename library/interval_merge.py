# AI生成: OpenAI Codex（2026-10-12）。出典の確認範囲は PROVENANCE.md を参照。
# 区間の合併
# 条件: l<=rの半開区間。空区間は除く。接する区間もまとめる設定。
# 計算量: O(N log N)時間、O(N)空間。
# API: merge_intervals(intervals) -> [(l,r), ...]。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def merge_intervals(intervals):
    result = []
    for l, r in sorted(intervals):
        if l == r:
            continue
        if result and l <= result[-1][1]:
            result[-1] = (result[-1][0], max(result[-1][1], r))
        else:
            result.append((l, r))
    return result


if __name__ == "__main__":
    print(merge_intervals([(5, 8), (1, 4), (3, 6), (10, 11)]))
