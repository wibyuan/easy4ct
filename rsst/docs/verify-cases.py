#!/usr/bin/env python3
# verify-cases.py —— 环尺寸<2 情形 B/C 的无解佐证
#
# 对应底稿 §4 情形 B（无扇、恰一帽 d^*=2）与情形 C（恰一扇 d^*=2、全帽 d^*=1）：
#   手推给出"无解"（帽子带外邻居覆盖沿外圈传播、绕圈必然冲突）。
# 本脚本构造两种情形的最简候选结构（只含基础边：帽子带 + 帽子带外邻居的基础邻接），
#   用三角剖分判定（面数 2n-4、每条边恰在两个三角形中）检验——全部失败，
#   佐证最简构造不合法。（注意：仅佐证，完整无解由底稿 §4 的推导保证。）
#
# 用法：python3 verify-cases.py

import itertools
from collections import Counter


def check_triangulation(adj, n):
    tris = set()
    for u in range(n):
        for v in adj[u]:
            if v < u:
                continue
            for w in adj[u] & adj[v]:
                tris.add(tuple(sorted((u, v, w))))
    cnt = Counter()
    for t in tris:
        for e in itertools.combinations(t, 2):
            cnt[e] += 1
    if len(cnt) != sum(len(a) for a in adj) // 2:
        return False
    if any(c != 2 for c in cnt.values()):
        return False
    return len(tris) == 2 * n - 4


def build_fan_case(k):
    # 情形 C 最简构造：w=0, x=1, 扇 f=2, 轮辐 v_i=3..2+k, 帽 h_i=3+k..2+2k,
    # 帽子带外邻居 a=3+2k, b=4+2k。f 在 h_k 与 h_1 之间；a 邻接 f,h_k，b 邻接 f,h_1。
    n = 2 * k + 5
    adj = [set() for _ in range(n)]

    def add(u, v):
        adj[u].add(v)
        adj[v].add(u)

    w, x, f = 0, 1, 2
    v = lambda i: 3 + (i - 1)
    h = lambda i: 3 + k + (i - 1)
    a, b = 3 + 2 * k, 4 + 2 * k
    for i in range(1, k + 1):
        add(w, v(i))
        add(x, h(i))
        add(v(i), v(i % k + 1))
        add(h(i), h(i % k + 1))
        add(v(i), h(i - 1 if i > 1 else k))
        add(v(i), h(i))
    add(v(1), f)
    add(f, h(k))
    add(f, h(1))
    add(a, f)
    add(b, f)
    return adj, n


def build_hat6_case(k):
    # 情形 B 最简构造：w=0, x=1, 轮辐 v_i=2..1+k, 帽 h_i=2+k..1+2k,
    # 帽 h_1 的帽子带外邻居 a=2+2k, b=3+2k。
    n = 2 * k + 4
    adj = [set() for _ in range(n)]

    def add(u, v):
        adj[u].add(v)
        adj[v].add(u)

    w, x = 0, 1
    v = lambda i: 2 + (i - 1)
    h = lambda i: 2 + k + (i - 1)
    a, b = 2 + 2 * k, 3 + 2 * k
    for i in range(1, k + 1):
        add(w, v(i))
        add(x, h(i))
        add(v(i), v(i % k + 1))
        add(h(i), h(i % k + 1))
        add(v(i), h(i - 1 if i > 1 else k))
        add(v(i), h(i))
    add(a, h(1))
    add(b, h(1))
    return adj, n


def main():
    for k in range(5, 10):
        adj, n = build_fan_case(k)
        print(f"fan case k={k}: triangulation={check_triangulation(adj, n)}")
        assert not check_triangulation(adj, n)
        adj, n = build_hat6_case(k)
        print(f"hat6 case k={k}: triangulation={check_triangulation(adj, n)}")
        assert not check_triangulation(adj, n)


if __name__ == "__main__":
    main()
