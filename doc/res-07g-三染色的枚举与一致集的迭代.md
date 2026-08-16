# 三染色的枚举与一致集的迭代

上一节把构型编码成了配置矩阵，把环染色编码成了三进制码。本节让数字跑起来：reduce.c 的全部工作分三步——枚举自由补全的一切三染色（得到 $\mathcal C$），在环染色空间上迭代计算最大一致子集（得到 $\mathcal C'$），再验证 contract。规模的数字值得先摆出来：环长最多为 $14$，一切染色 $3^{14}\approx478$ 万个；平衡有符号匹配随环长增长，环长 $14$ 时约 $148$ 万个；而"染色-匹配对"的规模量级是两千万（这是形式化工作者的估算，见 Gonthier 对 reducibility 计算的分析）。手算不可能，但每一步都是有限且机械的——这正是计算机出场的理由。

## 枚举自由补全的一切三染色

目标：列出自由补全 $S$ 的一切三染色，并记录每个三染色在环 $R$ 上的限制的码。$S$ 有 $n$ 个顶点、$m=3(n-1)-r$ 条边（环边 $e_1,\dots,e_r$ 先编号）。三染色要求"共面的三条边颜色互异"，颜色用 $\{1,2,4\}$ 表示（三个数的和为 $7$，任意两条的颜色决定第三条：$7-\text{色}_1-\text{色}_2$）。用 $\{1,2,4\}$ 而非 $\{1,2,3\}$ 的原因是位运算：$1,2,4$ 是三个互异的二进制位，$1\to2\to4\to8$ 恰好是左移一位，"换下一种颜色"就是"加倍"。

枚举的关键是边编号。strip 的编号策略是：每条边尽量与"编号更大"的边共面（环边先编号；之后每步从"与已编号顶点在循环序上构成最长连续段"的未编号顶点中选度数最大者）。这样对每条边 $e_i$，与它共面的边中编号大于 $i$ 的都被编号成一段连续区间，可以预先算成禁忌集：$F_j=\{\text{与 }e_j\text{ 共面且编号大于 }j\text{ 的边的颜色}\}$。$e_j$ 的候选颜色必须避开 $F_j$（否则它与某条共面的更晚边同色，违反三染色条件）。

算法从"最晚的边"开始向"最早的边"回溯：初始化 $c(e_m)=1$、$c(e_{m-1})=2$、$j=m-1$。循环：

1. 若 $c(e_j)$ 被 $F_j$ 禁止，则 $c(e_j)$ 加倍（换下一种颜色）；若加倍后溢出（$c(e_j)=8$，三种颜色都试过），则 $j$ 加一（回到更晚的边）并加倍其颜色——这是回溯。
2. 若 $j=r+1$，内部边已全部定色，由三角形关系推出环边的颜色（每条环边恰在一个三角形中，其颜色由共面的两条内部边决定），得到一个三染色；用 record 记录其环限制的码，然后 $c(e_j)$ 加倍继续循环。
3. 若 $j>r+1$，$j$ 减一，置 $c(e_j)=1$，并预计算 $F_j$。

record 的码计算值得说明。设某次定色后，环边中颜色为 $1,2,4$ 的边各自的三进制权重和为 $w_1,w_2,w_4$（$w_v=\sum_{e_i\text{ 颜色 }v}3^{i-1}$），三者之和恒为 $\frac{3^r-1}{2}$（一切位置的权重和）。程序取 $\text{colno}=\frac{3^r-1}{2}-2\min\{w_1,w_2,w_4\}-\max\{w_1,w_2,w_4\}$，即"中间权重减最小权重"。这是上一节定理（相似类唯一规范形）的实现：颜色置换只把三个权重重新排列，不改变 $\min$ 与 $\max$，故 colno 是相似类的不变量，与规范染色的码一一对应（同一类的不同染色得到同一个 colno）。程序的 live 数组就以 colno 为下标：下标处存 $0$ 表示"该码属于 $\mathcal C$"（能扩展到 $S$ 的三染色），存 $1$ 表示"该码不在 $\mathcal C$"。findlive 结束时返回的数目就是 $\mathcal C^*-\mathcal C$ 的大小——也就是上一节定义（D-可约）中迭代的起点 $\mathcal C_0$。

## 一致集的迭代

环长 $14$ 时 $\mathcal C^*$ 有约 $239$ 万个元素，不能直接搜"最大一致子集"。定理（lifts 一致）给出了结构性保证：一致集对"θ-适配"封闭。于是可以从 $\mathcal C_0=\mathcal C^*-\mathcal C$ 出发，反复删除"不满足封闭性"的染色与匹配，直到稳定。形式化地，从 $\mathcal M_0$（全体平衡有符号匹配）与 $\mathcal C_0$ 出发，递推：

$$\mathcal M_{i+1}=\{M\in\mathcal M_i:\mathcal C_i\text{ 包含一切 }\theta\text{-适配 }M\text{ 的染色（对每个 }\theta\text{）}\},$$

$$\mathcal C_{i+1}=\{\kappa\in\mathcal C_i:\text{ 对每个 }\theta\text{ 都存在 }M\in\mathcal M_{i+1}\text{ 使 }\kappa\ \theta\text{-适配 }M\}.$$

> **定理（迭代收敛）**
>
> $\mathcal M_i$ 与 $\mathcal C_i$ 都是有限集合且随 $i$ 单调递减，故存在 $i$ 使 $\mathcal C_i=\mathcal C_{i+1}$。

**证明：**

$\mathcal C_{i+1}\subseteq\mathcal C_i$ 与 $\mathcal M_{i+1}\subseteq\mathcal M_i$ 由递推定义直接可见。有限集合的递减序列必在有限步后稳定。$\blacksquare$

> **定理（一致集的迭代正确）**
>
> 若 $\mathcal C_i=\mathcal C_{i+1}$，则 $\mathcal C_i$ 恰是 $\mathcal C^*-\mathcal C$ 的最大一致子集 $\mathcal C'$。

**证明：**

先证 $\mathcal C_i$ 一致。由 $\mathcal C_i=\mathcal C_{i+1}$ 得 $\mathcal M_{i+1}=\mathcal M_{i+2}$（两个集合都由 $\mathcal M_{i+1}$ 按"$\mathcal C_{i+1}$ 含一切 θ-适配染色"筛选，而 $\mathcal C_{i+1}=\mathcal C_i$）。取 $\kappa\in\mathcal C_i$ 与 $\theta$：$\kappa\in\mathcal C_{i+1}$，故存在 $M\in\mathcal M_{i+1}$ 使 $\kappa$ $\theta$-适配 $M$；而 $M\in\mathcal M_{i+2}$，故一切 $\theta$-适配 $M$ 的染色都属于 $\mathcal C_{i+1}=\mathcal C_i$。$\mathcal C_i$ 一致。

再证 $\mathcal C'\subseteq\mathcal C_j$ 对一切 $j$ 成立（于是 $\mathcal C'\subseteq\mathcal C_i$；又 $\mathcal C_i$ 一致且与 $\mathcal C$ 无交，故 $\mathcal C_i\subseteq\mathcal C'$，两者相等）。归纳于 $j$。$\mathcal C'\subseteq\mathcal C_0$ 显然。设 $\mathcal C'\subseteq\mathcal C_j$，取 $\kappa\in\mathcal C_j-\mathcal C_{j+1}$：存在 $\theta$ 使 $\kappa$ 不 θ-适配任何 $M\in\mathcal M_{j+1}$。若 $\kappa$ 不 θ-适配环上的任何有符号匹配，则 $\kappa\notin\mathcal C'$；否则取 $M$ 使 $\kappa$ $\theta$-适配 $M$。若 $M\notin\mathcal M_0$，$M$ 不平衡，此时 $\kappa$ 不平衡（$\kappa$ 的 θ-适配者 $M$ 的平衡性与 $\kappa$ 的平衡性一致），而 $\mathcal C'$ 的成员都平衡（定义（平衡的染色与有符号匹配）后的一段说明），$\kappa\notin\mathcal C'$。否则 $M\in\mathcal M_0$，由 $\mathcal M$ 的递减性 $M\in\mathcal M_k-\mathcal M_{k+1}$ 对某个 $k\le j$：存在 $\theta'$ 与染色 $\kappa'\notin\mathcal C_k$ 使 $\kappa'$ $\theta'$-适配 $M$；对 $\kappa'$ 作颜色置换可设 $\theta'=\theta$。$\mathcal C'\subseteq\mathcal C_j\subseteq\mathcal C_k$，故 $\kappa'\notin\mathcal C'$；若 $\kappa\in\mathcal C'$，由 $\mathcal C'$ 一致，$\mathcal C'$ 含一切 $\theta$-适配 $M$ 的染色，特别含 $\kappa'$，矛盾。故 $\kappa\notin\mathcal C'$。归纳完成。$\blacksquare$

迭代的每一步都需要回答一个问题：给定一个匹配 $M$，哪些染色的码是"θ-适配 $M$ 的染色"的码？直接枚举染色再检查适配性要扫 $3^r$ 个染色，不可行。匹配自身也要编码：

> **定义（匹配的码与选择序列）**
>
> 设 $M=\{(\{a_i,b_i\},\mu_i):1\le i\le k\}$ 是环 $R$ 的有符号匹配集，$b_i<a_i$，且 $a_1=\max\{a_1,\dots,a_k\}$。若 $a_1<r$，$M$ 的**码**是 $c=\sum_{i=1}^{k}\left(3^{a_i-1}+\mu_i3^{b_i-1}\right)$，**选择序列**是 $h_i=2\left(3^{a_i-1}+\mu_i3^{b_i-1}\right)$（$2\le i\le k$）；若 $a_1=r$，$M$ 的码是 $c=\frac{3^r-1}{2}-\sum_{i=1}^{k}\left(3^{a_i-1}+\frac{3-\mu_i}{2}3^{b_i-1}\right)$，选择序列是 $h_i=3^{a_i-1}+\mu_i3^{b_i-1}$（$2\le i\le k$）。

> **定理（匹配的染色集枚举）**
>
> 设 $M$ 是有符号匹配，码为 $c$，选择序列为 $h_2,\dots,h_k$。则 $\left\{\left|c+\sum_{i=2}^{k}\varepsilon_ih_i\right|:\varepsilon_i\in\{0,1\}\right\}$ 恰是"$\theta$-适配 $M$ 的染色"（对某个 $\theta\in\{-1,0,1\}$）的码的集合。且若 $a_1<r$ 则 $\theta=0$；若 $a_1=r$，设 $d$ 是某 θ-适配染色的码 $c+\sum\varepsilon_ih_i$，则 $d<0$ 时 $\theta=1$、$d>0$ 时 $\theta=-1$。

**证明：**

适配关系逐匹配边独立：$M$ 的每条匹配边 $(\{e,f\},\mu)$ 要求 $\kappa(e)=\kappa(f)$（$\mu=1$）或 $\kappa(e)\ne\kappa(f)$（$\mu=-1$）——每条匹配边给出一个二选一，$k$ 条匹配边给出 $2^k$ 种组合，每个组合确定染色在匹配边上的取值模式。$\theta$ 的取值固定后，"$\kappa(e)\ne\theta$"的边的集合恰是 $E(M)$，故非匹配边的取值都是 $\theta$。这样每种组合唯一决定一个染色；反之每个 θ-适配染色对应一种组合。码的线性结构（三进制按位不重叠）使"第 $i$ 条匹配边的两种选择"反映为码相差 $h_i$：选择 $\varepsilon_i=1$ 对应其中一种取值模式。$\theta$ 的判定（$a_1<r$ 时 $\theta=0$、$a_1=r$ 时由码符号定）来自定义（匹配的码）中两条公式的构造——$a_1=r$ 时 $M$ 用到环的最后一条边，$\theta=\pm1$ 的两种染色互为负，绝对值吸收了这个二重性。$\blacksquare$

这个定理把"找 $M$ 的一切 θ-适配染色"变成 $2^{k}$ 次加法（$k\le7$，因为 $14$ 条边的环至多 $7$ 对匹配），每次加法得到一个码，查一次 live 数组即知该染色是否在 $\mathcal C_i$。

## 程序对照

reduce.c 与本节内容的对应如下。strip 与 ininterval 实现边编号；findlive 实现 $\mathcal C_0$ 的枚举（含 record 的码计算）；testmatch、augment、checkreality 与 stillreal 实现 $\mathcal M$ 的迭代——testmatch 生成全部平衡有符号匹配（matchweight 表预计算每条匹配边的码贡献，parity 变量核对平衡性），checkreality 对每个匹配枚举全部"选择组合"并检查其 θ-适配染色是否都在 live 中，stillreal 负责逐码查表并把 $\theta$ 标记写回 live 的位 2/4/8；updatelive 实现 $\mathcal C_{i+1}$：live 的位 1 表示"在 $\mathcal C_i$"，位 2、4、8 分别表示"被 $\theta=0,\pm1$ 标记过"，三标记齐备（live 值为 15）的染色保留。real 数组的每个位对应一个平衡有符号匹配，迭代中 $\mathcal M_i$ 递减即位的清除。整个迭代在 live 数组上就地完成：程序输出 "D-reducible" 或 "Not D-reducible"，对应 $\mathcal C'=\varnothing$ 与否。

需要说明的是，程序在迭代中并不区分染色与码——上一节定理（相似类唯一规范形）保证码与相似类一一对应，而一致集对相似封闭：设 $\mathcal C$ 一致、$\kappa\in\mathcal C$、$\pi$ 是颜色置换，$\kappa'=\pi\circ\kappa$；对 $\kappa'$ 与任意 $\theta'$，令 $\theta=\pi^{-1}(\theta')$，$\mathcal C$ 一致给出匹配 $M$ 使 $\kappa$ $\theta$-适配 $M$ 且 $\mathcal C$ 含一切 $\theta$-适配 $M$ 的染色；由 $\pi$ 是双射，$\{e:\kappa(e)\ne\theta\}=\{e:\kappa'(e)\ne\theta'\}$ 且 $\kappa(e)=\kappa(f)\iff\kappa'(e)=\kappa'(f)$，故 $\kappa'$ $\theta'$-适配同一个 $M$，而"$\theta'$-适配 $M$"与"$\theta$-适配 $M$"是同一族染色，已全部属于 $\mathcal C$。于是 $\kappa'\in\mathcal C$，一致集是相似类的并，对码操作就是对相似类操作。

$\mathcal C'$ 到手之后，还剩下 contract 的验证：枚举 $S$ 的模 $X$ 三染色，检查其环限制是否都落在 $\mathcal C'$ 之外。这是下一节的内容。
