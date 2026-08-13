#!/usr/bin/env python3
# verify-bipyramid.py —— 双锥族 B_k 的性质验证
#
# 验证对象（对应底稿《RSST-(4.1)-字面失效范围刻画底稿》§5）：
#   双锥 B_k（k=4..10）：两个轮心 + 两个 k 圈 + 帽子带。
# 验证内容：
#   1) 三角剖分：面数 = 2n-4 且每条边恰在两个三角形中；
#   2) 内部 6 连通：无 ≤5 分离圈（5-分离圈要求两侧各 ≥2 顶点）；
#   3) 候选 cartwheel（hub = 各顶点）的环尺寸分布。
# 结论：
#   k=4 最小度 4，非内部 6 连通；k≥5 全部为内部 6 连通三角剖分；
#   轮心处环尺寸 = 0 < 2；非轮心处 k=5 亦为 0（二十面体处处失效）、k≥6 为 2k-10 ≥ 2。
#
# 用法：python3 verify-bipyramid.py
# 运行时间：数秒至数十秒（k=10 时 C(22,5) 子集枚举）。

import itertools
from collections import deque


def bipyramid(k):
    # 顶点：0=w, 1=x, 轮辐 v_i=2+i, 帽 h_i=2+k+i
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


def is_triangulation(adj, n):
    tris = set()
    for u in range(n):
        for v in adj[u]:
            if v < u:
                continue
            for w in adj[u] & adj[v]:
                tris.add(tuple(sorted((u, v, w))))
    cnt = {}
    for t in tris:
        for e in itertools.combinations(t, 2):
            cnt[e] = cnt.get(e, 0) + 1
    if len(cnt) != sum(len(a) for a in adj) // 2:
        return False
    if any(c != 2 for c in cnt.values()):
        return False
    return len(tris) == 2 * n - 4


def comps(adj, n, excluded):
    seen = set(excluded)
    out = []
    for s in range(n):
        if s in seen:
            continue
        seen.add(s)
        q = deque([s])
        sz = 0
        while q:
            u = q.popleft()
            sz += 1
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    q.append(v)
        out.append(sz)
    return out


def internally_6_connected(adj, n):
    for r in range(6):
        for X in itertools.combinations(range(n), r):
            c = comps(adj, n, set(X))
            if len(c) > 2:
                return False
            if len(c) == 2 and not (r == 5 and 1 in c):
                return False
    return True


def connected_after(adj, S, v):
    T = S - {v}
    if not T:
        return True
    seen = {v}
    q = deque([next(iter(T))])
    seen.add(next(iter(T)))
    while q:
        u = q.popleft()
        for w in adj[u]:
            if w in T and w not in seen:
                seen.add(w)
                q.append(w)
    return len(seen) == len(T) + 1


def ringsize(adj, hub):
    C1 = set(adj[hub])
    C2 = set()
    for v in C1:
        for w in adj[v]:
            if w not in C1 and w != hub:
                C2.add(w)
    W = {hub} | C1 | C2
    ring = 0
    for v in C2:
        if connected_after(adj, W, v):
            dT = len(adj[v])
            dG = len(adj[v] & W)
            ring += dT - dG - 1
    return ring


def main():
    for k in range(4, 11):
        adj = bipyramid(k)
        n = len(adj)
        e = sum(len(a) for a in adj) // 2
        tri = is_triangulation(adj, n)
        i6c = internally_6_connected(adj, n)
        pole_ring = ringsize(adj, 0)
        other = [ringsize(adj, h) for h in range(2, n)]
        other_vals = sorted(set(other))
        print(f"k={k} n={n} e={e} triangulation={tri} "
              f"i6c={i6c} pole_ringsize={pole_ring} other={other_vals}")
        assert tri
        if k >= 5:
            assert i6c and pole_ring == 0
        else:
            assert not i6c


if __name__ == "__main__":
    main()
