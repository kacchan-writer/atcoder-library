# AI生成: OpenAI Codex（2026-10-12）。参照資料・運用方針: PROVENANCE.md。
# 参照: 既存のローカル二分探索雛形（詳細は PROVENANCE.md）。
# 二分探索・bisect
# 条件: 単調性が必要。okは真、ngは偽と既知の整数（領域外の番兵でもよい）。番兵は判定しない。
# 計算量: 判定T、初期幅WとしてO(T log W)時間、補助空間O(1)。
# API: boundary(ok,ng,check)。bisect_left(a,x)はx以上が始まる位置、bisect_rightはxより大きい位置。
# 添字は原則0始まり、区間は [l, r)。末尾は単独実行用の例。
from bisect import bisect_left, bisect_right

def boundary(ok, ng, check):
    while abs(ok - ng) > 1:
        mid = (ok + ng) // 2
        if check(mid):
            ok = mid
        else:
            ng = mid
    return ok


if __name__ == "__main__":
    print(boundary(0, 101, lambda x: x * x <= 100))
    a = [1, 3, 3, 7]
    print(bisect_left(a, 3), bisect_right(a, 3))
