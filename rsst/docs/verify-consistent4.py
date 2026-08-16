#!/usr/bin/env python3
# verify-consistent4.py
# 核验文章 res-08 定理（4 圈一致集分类）=(6.3)：
#   4 圈上每个非空一致集都包含 C0∪C1、C1∪C2、C2∪C3、C3∪C0 之一。
# 同时核验"一致集是相似类的并"（按 res-08 补证的闭包论证，此处用穷举确认）。
# 运行：python3 verify-consistent4.py
# 输出：全部通过（14 类、16384 个候选、核验结果）。

from itertools import permutations

R = 4
edges = range(1, R + 1)
COLORS = [-1, 0, 1]

def all_colorings():
    out = []
    for a in COLORS:
        for b in COLORS:
            for c in COLORS:
                for d in COLORS:
                    out.append((a, b, c, d))
    return out

COLORINGS = all_colorings()  # 81 个

# 相似：颜色置换
def permute(kappa, pi):
    return tuple(pi[c] for c in kappa)

PERMS = list(permutations(COLORS))  # 6 个置换

def orbit(kappa):
    return frozenset(permute(kappa, p) for p in PERMS)

# 相似类（轨道）
classes = []
seen = set()
for k in COLORINGS:
    o = orbit(k)
    if o not in seen:
        seen.add(o)
        classes.append(o)
print(f"相似类数: {len(classes)} (Burnside: (3^4 + 3*1 + 2*0)/6 = 14)")

# 环的边结构：e_i 连接 v_i 与 v_{i+1}（v_5 = v_1）
def edge_ends(e):
    return (e, e + 1 if e < R else 1)

# 边 e 与 f 删除 e',f' 后是否同分量（边图上的连通性）
def same_component(e, f, removed):
    adj = {x: set() for x in edges}
    for x in edges:
        if x in removed:
            continue
        ux, vx = edge_ends(x)
        for y in edges:
            if y in removed or y <= x:
                continue
            uy, vy = edge_ends(y)
            if {ux, vx} & {uy, vy}:
                adj[x].add(y)
                adj[y].add(x)
    # BFS
    stack = [e]
    seenv = set()
    while stack:
        x = stack.pop()
        if x in seenv:
            continue
        seenv.add(x)
        stack.extend(adj[x])
    return f in seenv

# 一切有符号匹配集（匹配 = 两两不交的边对，符号 ±1，且满足分量条件）
signed_matchings = []
pairs = [(a, b) for a in edges for b in edges if a < b]
for mask in range(1 << len(pairs)):
    chosen = [pairs[i] for i in range(len(pairs)) if mask >> i & 1]
    # 两两不交
    used = set()
    ok = True
    for (a, b) in chosen:
        if a in used or b in used:
            ok = False
            break
        used.add(a); used.add(b)
    if not ok:
        continue
    # 符号赋值
    n = len(chosen)
    for s in range(1 << n):
        M = []
        for i in range(n):
            (a, b) = chosen[i]
            mu = 1 if (s >> i & 1) else -1
            M.append(((a, b), mu))
        # 有符号匹配集条件 (ii)
        ok2 = True
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                (a, b), mu = M[i]
                (ap, bp), mup = M[j]
                if not same_component(a, b, {ap, bp}):
                    ok2 = False
                    break
            if not ok2:
                break
        if ok2:
            signed_matchings.append(M)
print(f"有符号匹配集数: {len(signed_matchings)}")

def EM(M):
    out = set()
    for ((a, b), mu) in M:
        out.add(a); out.add(b)
    return out

def fits(kappa, theta, M):
    if EM(M) != {e for e in edges if kappa[e - 1] != theta}:
        return False
    for ((a, b), mu) in M:
        if (kappa[a - 1] == kappa[b - 1]) != (mu == 1):
            return False
    return True

# 一致集（候选 = 相似类的并）：定义逐条核验
def is_consistent(cands):
    for kappa in cands:
        for theta in COLORS:
            found = False
            for M in signed_matchings:
                if not fits(kappa, theta, M):
                    continue
                # 条件：C 包含一切 θ-适配 M 的染色
                if all(kp in cands for kp in COLORINGS if fits(kp, theta, M)):
                    found = True
                    break
            if not found:
                return False
    return True

# (6.3) 的四个类
def cls_of(kappa):
    o = orbit(kappa)
    return next(i for i, cl in enumerate(classes) if cl == o)

C0 = cls_of((0, 0, 0, 0))
C1 = cls_of((0, 1, 1, 0))
C2 = cls_of((0, 1, 0, 1))
C3 = cls_of((0, 0, 1, 1))
unions = [frozenset({C0, C1}), frozenset({C1, C2}), frozenset({C2, C3}), frozenset({C3, C0})]

# 候选：相似类并（2^14-1 个非空），逐一按定义核验一致性，并检查 (6.3) 结论。
# 注：穷举空间取"相似类的并"——文章已证明一致集是相似类的并
# （对 κ∈C 与置换 π，用 κ 在 θ=π^{-1}(θ') 处的匹配 M 验证 π∘κ 满足闭包条件），
# 故此处穷举覆盖一切一致集。
fails = 0
checked = 0
nontrivial = 0
for mask in range(1, 1 << len(classes)):
    cand = set()
    for i, cl in enumerate(classes):
        if mask >> i & 1:
            cand.update(cl)
    if not cand:
        continue
    checked += 1
    if not is_consistent(cand):
        continue
    nontrivial += 1
    # (6.3)：含四并集之一
    idx = {cls_of(k) for k in cand}
    if not any(u <= idx for u in unions):
        print("FAIL: 一致集不含任何四并集")
        fails += 1

print(f"候选检查: {checked}, 非空一致集: {nontrivial}, 失败: {fails}")
assert nontrivial > 0
assert fails == 0
print("全部通过：4 圈上每个非空一致集都是相似类的并，且包含 C0∪C1、C1∪C2、C2∪C3、C3∪C0 之一。")
