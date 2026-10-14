# AI生成: OpenAI Codex（2026-10-12）。出典の確認範囲は PROVENANCE.md を参照。
# 貪欲法・区間スケジューリング
# 条件: l<rの半開区間。端点で接してよい。重み付きの最大価値にはこの貪欲は使えない。
# 計算量: O(N log N)時間、O(N)空間。
# API: schedule(intervals) -> 採用する区間の列。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
def schedule(intervals):
    chosen, end = [], None
    for l, r in sorted(intervals, key=lambda p: p[1]):
        if end is None or end <= l:
            chosen.append((l, r))
            end = r
    return chosen


if __name__ == "__main__":
    print(schedule([(0, 3), (1, 2), (2, 4), (3, 5)]))
