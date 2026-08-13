#!/usr/bin/env python3
# verify-coloring.py —— 双锥 B_k 的 4-染色（统一构造的发现与确认）
#
# 对应底稿 §6 与文章 res-07a 定理（双锥可 4-染色）：
#   回溯搜索 B_k 的 4-染色并打印染色模式，据此归纳统一构造：
#     k 偶：w=0, x=1, 轮辐 1,2 交替, 帽 3,0 交替；
#     k 奇：w=0, x=1, 轮辐 1,2 交替末位 3, 帽 3,0 交替末位 2。
# 文章中的定理以"构造 + 逐条核验"为纯组合证明，不依赖本脚本；
# 本脚本用于确认构造在 k=4..15 上的合法性（打印输出与公式一致）。
#
# 用法：python3 verify-coloring.py

import sys


def bipyramid(k):
    n = 2 * k + 2
    adj = [set() for _ in range(n)]

    def add(u, v):
        adj[u].add(v)
        adj[v].add(u)

    for i in range(k):
        vi, hi = 2 + i, 2 + k + i
        add(0, vi)
        add(1, hi)
        add(vi, 2 + (i + 1) % k)
        add(hi, 2 + k + (i + 1) % k)
        add(vi, 2 + k + (i - 1) % k)
        add(vi, hi)
    return adj


def four_color(adj):
    n = len(adj)
    col = [-1] * n

    def bt(i):
        if i == n:
            return True
        used = {col[v] for v in adj[i] if col[v] >= 0}
        for c in range(4):
            if c not in used:
                col[i] = c
                if bt(i + 1):
                    return True
        col[i] = -1
        return False

    return col if bt(0) else None


def formula_coloring(k):
    # 文章 res-07a 定理（双锥可 4-染色）的统一构造
    col = {}
    col[0] = 0  # w
    col[1] = 1  # x
    for i in range(k):
        vi = 2 + i
        hi = 2 + k + i
        if k % 2 == 0:
            col[vi] = 1 + (i % 2)
            col[hi] = 3 - 3 * (i % 2)  # 3,0,3,0,...
        else:
            col[vi] = 3 if i == k - 1 else 1 + (i % 2)
            col[hi] = 2 if i == k - 1 else 3 - 3 * (i % 2)
    return col


def check(adj, col):
    n = len(adj)
    for u in range(n):
        for v in adj[u]:
            if u < v and col[u] == col[v]:
                return False
    return True


def main():
    for k in range(4, 16):
        adj = bipyramid(k)
        col = formula_coloring(k)
        ok = check(adj, col)
        v = [col[2 + i] for i in range(k)]
        h = [col[2 + k + i] for i in range(k)]
        print(f"k={k} formula_ok={ok} w={col[0]} x={col[1]} "
              f"spokes={v} hats={h}")
        assert ok
        # 对照：回溯染色必须存在（B_k 可 4-染）
        assert four_color(adj) is not None


if __name__ == "__main__":
    sys.exit(main())
