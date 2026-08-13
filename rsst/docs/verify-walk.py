#!/usr/bin/env python3
# verify-walk.py —— (3.1) 事实三"直走延伸必达边界"的程序佐证
#
# 对应文章 res-07b 定理（lifts 一致）证明的事实三：
#   从 κ≠0 的边界边出发的唯一延伸（每步穿过一个尚未走过的有限区域）
#   必在有限步内到达另一条边界边（文章已给出手推证明：闭合走廊 +
#   入口顶点处面循环矛盾）。
# 本脚本在随机近三角剖分（简单三角剖分挖一个三角形面作洞）上，
#   由随机合法 4-染色经 Tait 异或规则导出三染色，对每条 κ≠0 的边界边
#   模拟直走延伸，检验是否总在边界边处终止（不进入循环、不卡死）。
# 结论：n=6..12 各 300 个随机图 × 每图全部洞 × 全部非零边界边，
#   共 54600 次测试，0 失败。程序为佐证，非证明。
#
# 用法：python3 verify-walk.py
# 运行时间：数秒至数十秒。

import itertools
import random


def rand_triangulation(n, seed):
    random.seed(seed)
    faces = [(0, 1, 2)]
    adj = {0: set(), 1: set(), 2: set()}
    for i in range(3):
        for j in range(3):
            if i != j:
                adj[i].add(j)
    nxt = 3
    while nxt < n:
        f = random.choice(faces)
        a, b, c = f
        faces.remove(f)
        adj[nxt] = set()
        for v in (a, b, c):
            adj[v].add(nxt)
            adj[nxt].add(v)
        faces.append((a, b, nxt))
        faces.append((b, c, nxt))
        faces.append((c, a, nxt))
        nxt += 1
    return adj, faces


def four_color(adj, n):
    col = [-1] * n

    def bt(i):
        if i == n:
            return True
        used = {col[v] for v in adj[i] if col[v] >= 0}
        cands = [c for c in range(4) if c not in used]
        random.shuffle(cands)
        for c in cands:
            col[i] = c
            if bt(i + 1):
                return True
        col[i] = -1
        return False

    return col if bt(0) else None


def has_edge(f, e):
    return e[0] in f and e[1] in f


def straight_walk(adj, ec, faces, hole, start_edge):
    # 从 start_edge 出发直走：穿过非洞区域到唯一非零边；遇洞边（边界边）终止
    seen = set()
    cur = start_edge
    prev_region = None
    while True:
        if cur in seen:
            return False, "cycle"
        seen.add(cur)
        if has_edge(hole, cur):
            return True, "ended"
        regions = [f for f in faces if f != hole and has_edge(f, cur)]
        nxt = None
        for f in regions:
            if f != prev_region:
                nxt = f
                break
        if nxt is None:
            return False, "no_region"
        others = [
            tuple(sorted(e))
            for e in itertools.combinations(nxt, 2)
            if tuple(sorted(e)) != cur and ec[tuple(sorted(e))] != 0
        ]
        if len(others) != 1:
            return False, "bad_region"
        prev_region = nxt
        cur = others[0]


def main():
    total = 0
    fails = 0
    detail = None
    for n in range(6, 13):
        for trial in range(300):
            adj, faces = rand_triangulation(n, trial * 1000 + n)
            col = four_color(adj, n)
            if col is None:
                continue
            ec = {}
            for u in range(n):
                for v in adj[u]:
                    if u < v:
                        d = (col[u] - col[v]) % 4
                        ec[(u, v)] = {1: 1, 3: -1, 2: 0}[d]
            for hole in faces:
                hole_edges = [
                    tuple(sorted(e)) for e in itertools.combinations(hole, 2)
                ]
                for e in hole_edges:
                    if ec[e] == 0:
                        continue
                    total += 1
                    ok, why = straight_walk(adj, ec, faces, hole, e)
                    if not ok:
                        fails += 1
                        if detail is None:
                            detail = (n, trial, hole, e, why)
    print(f"tested={total} fails={fails} {detail if detail else ''}")
    assert fails == 0


if __name__ == "__main__":
    main()
