# 代码导览

本篇是 reduce.c 与 discharge.c 的逐函数导览，供读完正文后对照阅读：每个函数的目的、数据流、以及与正文章节的对应。正文只讲概念与算法，本篇讲实现。代码全文在仓库 rsst/code/ 目录；记号沿用正文（码、$\mathcal C$、$\mathcal C'$、轴、出口等）。

## reduce.c：可约性验证

### 常量与主流程

`VERTS=27`、`DEG=13`、`EDGES=62`、`MAXRING=14` 是自由补全的规模上限（顶点数、顶点度数、边数、环长各加一，因为行 0 也占用）。`tp_confmat` 是配置矩阵（res-07f 定义（配置矩阵）），`tp_angle` 是"角度表"（每条边的共面边列表），`tp_edgeno` 是边编号表。

main 对文件中的每个构型依次执行四步，对应正文的四节：

1. `findangles`：从配置矩阵算出角度表与 contract 信息（res-07h）；
2. `findlive`：枚举自由补全的一切三染色，算出 $\mathcal C_0=\mathcal C^*-\mathcal C$（res-07g）；
3. `testmatch` 与 `updatelive` 交替迭代：算出最大一致子集 $\mathcal C'$（res-07g）；
4. `checkcontract`：若 $\mathcal C'\ne\varnothing$，验证声明的 contract（res-07h）。

`power[i]=3^{i-1}`、`ncodes=(3^{r-1}+1)/2`（res-07f 定理（相似类唯一规范形）的码数）、`simatchnumber` 表是平衡有符号匹配的个数（环长 $r$ 时）。`live` 与 `real` 是两个字节数组：live 以码为下标（初值全 1），real 以"平衡有符号匹配的编号"为下标、逐位使用。

### ReadConf：读入与七条检查

读取顺序与 res-07f 的"文件与程序"段一致：名字行、第二行（$n,r,\mathcal C$ 的码数、$\mathcal C'$ 的码数）、contract 行（个数加端点对）、$n$ 行邻接表、坐标区（`C==NULL` 时跳过）、空行。随后逐条执行 res-07f 的条件 1 至 7，每条的代码就是定义的字面翻译——例如条件 7 的检查（"$i$ 的邻接表中 $k$ 的后继恰是 $k$ 的邻接表中 $i$ 的前驱"）在循环里对每个邻接项 $k$ 在 $A[k]$ 中找匹配项 $p$，找不到即 `ReadErr(7)`；条件 6 的"切换"计数按循环下标处理（`A[i][j<d?j+1:1]`、`j+2-d`）。前两个计数（`A[0][2]`、`A[0][3]`）不在此处核对——它们是文件自报值，留待与 `findlive`、迭代的实际结果对拍（`printstatus` 与 `checkcontract` 中的 "DISCREPANCY" 分支）。

### strip 与 ininterval：边编号

编号的目标（res-07g）：每条边尽量与"编号更大的共面边"同侧，使禁忌集 $F_j$ 可以预计算。阶段一给环边编号 $1,\dots,r$（`edgeno[u][v]=v`）。阶段二处理内部边：每步在未编号顶点中选"其已编号邻居在循环序中构成最长连续段"者（`ininterval` 返回这个段长，长度相同取度数大者），然后把该顶点与已编号邻居的边从编号 $3(n-1)-r$ 起向下编号——`ininterval` 的实现是循环序上找第一个已编号位置、数连续段、再检查剩余位置无已编号者（有则整个返回 0，因为"已编号邻居不成单段"会让共面边的编号分散）。阶段三处理环与内部之间的边（同样的思路，启发式 `3*deg+4*(done[u]+done[w])` 优先"两侧邻居都已完成"的环顶点）。三阶段合起来保证：每条边与其共面边在编号上"扎堆"，`findangles` 里"编号更大的共面边"集合小而集中。

### findangles：角度表与 contract 检查

`strip` 之后，`findangles` 对每个三角形取其最小编号边 $c$，把另外两条边 $a,b$（编号更大者）记入 `angle[c]`；若三角形不含 $X$ 的边则同时记入 `diffangle[c]`，若第三边在 $X$ 中则记入 `sameangle[c]`。这正是 res-07h 模 $X$ 枚举所需的 $D_i$ 与 $S_i$。contract 的合法性检查也在这里：`contract[0]` 来自矩阵行 0，端点对经 `edgeno` 转成边号，若某条 $X$ 边是环边报 "CONTRACT IS NOT SPARSE"（稀疏性条款）；$|X|=4$ 时的三叉点检查（res-07d 定义（三叉点））按定义字面实现：对每个内部顶点数其邻居中"接 $X$ 边"的个数，至少 $3$ 且（度数 $\ge6$ 或存在 $X$ 端点不在其邻居中）即通过，否则报 "CONTRACT HAS NO TRIAD"。

### findlive：$\mathcal C_0$ 的枚举

实现即 res-07g 的三步骤回溯。颜色用 $1,2,4$ 三个位表示（`c[j]<<=1` 是"换下一种颜色"，溢出位 $8$ 表示三种颜色都试过）。`forbidden[j]` 是禁忌集的位掩码：`c[j]&forbidden[j]` 非零即被禁；初始化 `c(e_m)=1`、`c(e_{m-1})=2`、`forbidden[m-1]=5`（禁位 $1$ 与 $4$：$e_m$ 的颜色与三角形的"第三色"）。主循环：被禁则加倍；溢出则回溯（`c[++j]<<=1`，到 `j>=edges-1` 即穷尽）；`j==ring+1` 时内部边全部定色，调 `record` 记录环限制的码；否则 `j` 减一、`c[j]=1`、`forbidden[j]` 置为"与 $e_j$ 共面的更晚边颜色"的并（`angle[j]` 表的直接使用）。

`record` 的码计算是 res-07f 定理（相似类唯一规范形）的实现：环边 $e_i$ 的颜色由共面的两条内部边推出（`sum=7-col[a]-col[b]`），三色各自的三进制权重和为 $w_1,w_2,w_4$，`colno=bigno-2*min-max`（即"中间权重减最小权重"，res-07g 已解释它是相似类不变量），`live[colno]=0` 标记"在 $\mathcal C$"。`inlive` 是同一计算的非破坏版本（只查不改）。

### testmatch、augment、checkreality、stillreal：匹配迭代

这组函数实现 res-07g 的 $\mathcal M$ 迭代（1401.6481 §3）。`matchweight[a][b]` 的四个预计算值对应定义（匹配的码与选择序列）中 $a_1<r$ 与 $a_1=r$ 两种情形的码贡献（前两个含因子 $2$、后两个不含，恰是选择序列的两种形态）。`testmatch` 对每对 $(a,b)$ 生成候选匹配边，把"可与 $a,b$ 同时入选的其他匹配边"限制在与 $a,b$ 不交错的区间 $[1,b-1]\cup[b+1,a-1]$（匹配集条件 (ii) 的"不交错"），递归交给 `augment` 枚举全部匹配组合。

`checkreality` 对每个匹配枚举"选择组合"（位运算 `left` 逐位取），`col` 累计码、`parity` 累计奇偶（平衡匹配的检查：偶数条"反号"匹配边——对应定义（平衡的染色与有符号匹配）的奇偶条件），最后把组合交给 `stillreal`。`stillreal` 逐匹配边生成 θ-适配染色的码（`sum[j]-choice[i]` 或正或负，负数取绝对值查表——(3.2) 的 $|c+\sum\varepsilon_ih_i|$），任一码不在 live 中即淘汰该匹配；全部通过则把 $\theta$ 标记写回 live 的位 $2$（$\theta=0$）或位 $4,8$（$\theta=\pm1$，由匹配是否用到环的最后一条边区分，对应 (3.2) 的 $a_1=r$ 情形）。

`updatelive` 实现 $\mathcal C_{i+1}$：位 $1$ 表示"在 $\mathcal C_i$"，三个 $\theta$ 标记齐备（值 $15$）者保留并复位为 $1$，否则清零；`live[0]` 有特殊处理（全 $0$ 染色是唯一"被一切 $\theta$ 适配"的退化成员）。$n$ 下降且不为零则继续迭代，降为零输出 "D-reducible"，否则 "Not D-reducible"。

### checkcontract：contract 的验证

入口的四个分支对应 contract 定义与文件对拍："CONTRACT PROPOSED"（$\mathcal C'=\varnothing$ 却给了 $X$）、"NO CONTRACT PROPOSED"（$\mathcal C'\ne\varnothing$ 却没有 $X$）、"DISCREPANCY IN EXTERIOR SIZE"（$|\mathcal C'|$ 与文件自报不符）、"INPUT CONTRACT IS INCORRECT"（某模 $X$ 三染色的限制落在 $\mathcal C'$ 中）。枚举本身与 `findlive` 同构，差别在 res-07h 讲的三处：回溯只在非 $X$ 边上前进（`while(contract[++j])` 与 `while(contract[--j])` 跳过 $X$ 的边）、`forbidden` 由 `diffangle` 与 `sameangle` 合成（`u=4` 起手、`~c[sm[i]]` 是"除 $c(f)$ 外的两种颜色"——$S_i$ 的"必须同色"禁忌）、`j==1` 时用 `inlive` 检查环限制是否落入 $\mathcal C'$。

## discharge.c：放电的机器可读证明验证

### 数据与主流程

`tp_axle` 是轴（`low[0]=upp[0]=deg`，`low[i],upp[i]` 是位置 $i$ 的界，`INFTY` 表示 $12$ 之上的"无约束"）。`tp_outlet` 是出口（`number` 是规则号、`value=\pm1$ 是值、`nolines` 与 `pos/low/upp` 数组是三元组序列）。`tp_posout` 是"定位出口"（出口 + 位置 $x$）。`tp_question` 是提问（`query` 序列，每项含 `u,v,z,xi`——三角形第三顶点 $z$、两个已定顶点 $u,v$、全度数 $\xi$）。

main 的流程：读 Degree 行（轮心度数）；`CheckHubcap(axles,NULL,...)` 初始化出口（读 rules 文件、算出口、写入 outlet.et 文件）；`Reduce(NULL,0,0)` 初始化（读 unavoidable.conf、编译成提问表）；随后按缩进深度循环读行：行首 "L%d" 是深度，其后首字符分派——`C` 调 `CheckCondition`（条件行，处理后深度加一）、`R` 调 `Reduce`（可约性处置）、`H` 调 `CheckHubcap`（毂盖处置）、`S` 调 `CheckSymmetry`（对称处置）；处理完深度减一；最后一行必须是 `Q.E.D.`。这对应 res-07j 定义（断言与呈现）的树形结构：缩进即深度，条件行开子断言，处置行落在叶子上。

### ReadOutlets 与 DoOutlet：规则到出口的编译

rules 文件的格式即 res-07j 定理（出口对等）证明中描述的顶点序列：每条规则两行，首行是规则号与 $\beta(v_0),\delta(v_0),\beta(v_1),\delta(v_1)$，次行是 $(i,\beta(v_i),\delta(v_i))$ 三元组。`U,V` 两张静态表是 $T(u,v)$ 三角形函数的两个方向的展开模板（1401.6485 §2 末段）。`DoOutlet` 从顶点序列出发，用 `adjmat`（骨架的三角形函数表，见下）把每个顶点位置 $z_j$ 映射成轴的位置 $p_i$：`adjmat[u][v]` 给出"与 $u,v$ 成顺时针三角形的第三顶点"，从而在轴的位置编号 $1,\dots,5d$ 中定位（轮辐 $i$、帽 $d+i$、扇 $2d+i,\dots$）。`b[j]` 的两位数编码 $\beta,\delta$ 拆成 `low/upp`（$9$ 表 $\infty$、$0$ 表示"上下界相同"）；若规则要求轮心位置（$j=k$）的界与当前度数不符，该出口对本度数不适用（返回 0）。规则号取负即出口的镜像（源汇互换），`value` 相应取 $\pm1$。这实现了 (2.2) 的"每条规则对应一对互为负值的出口"。

### CheckCondition 与 CheckSymmetry

条件行 "C n m" 的解析与检查对应 res-07j 定义（条件与细分）：`n` 在 $1..5d$、`m$ 在允许集合中、$n>2d$ 时要求所属轮辐已固定（(C3)）。细分的实现是互补对的关键：当前轴 `A` 的 `upp[n]` 压低为 $m-1$（$m>0$ 时，即"度数 $\le m-1$"的分支），下一层轴 `A+1` 的 `low[n]` 抬高为 $m$（"度数 $\ge m$"的分支）；`m<0$ 时对称。若历史条件不含扇位置，该条件被记录为对称候选（`sym` 条目，含各条件的界），供 `S` 行引用——`CheckSymmetry` 找到对应条目后，用 `OutletForced`（或 `ReflForced`）核验"配合当前轴的每个轮形构型都配合旋转（或反射）后的对称轴"：`ReflForced` 把位置 $p$ 按反射公式映射到 $q$（轮辐 $i\to d+1-i$、帽与扇相应镜像）再逐项比较界。

### CheckHubcap 与 CheckBound

毂盖行 "H (x₁,y₁,v₁)(x₂,y₂,v₂)..." 的解析与检查：`covered` 数组核对"每个轮辐恰好出现两次"（重复条目只列一次时 `x==y` 的处理）；`total` 是 $2\sum v_i$（$x=y$ 时加倍）或 $\sum v_i$（成对时按 (H2) 的 $\lfloor\frac12\sum v_i\rfloor$ 语义），`total > 20(deg-6)+1` 报 (H2) 违反（对应 $10(6-d)+\lfloor\frac12\sum v_i\rfloor\le0$）。对每个毂盖成员 $(x_i,y_i,v_i)$，构造"定位出口"列表（每个出口在 $x_i$ 处、$x_i\ne y_i$ 时再在 $y_i$ 处，$s$ 数组初值 0、末尾哨兵 99），调 `CheckBound`。

`CheckBound` 即 res-07j 描述的带剪枝递归枚举，实现与 1401.6485 §3 的五步一一对应：扫描定位出口表，把"被当前轴强制"者置 $s=1$ 并计入 `forcedch`、把"不被允许"者置 $s=-1$ 剪枝、其余正值者计入 `allowedch`；`forcedch+allowedch\le maxch$ 则界成立返回；`forcedch>maxch$ 则调 `Reduce`（此路只可能被"可约"救回）；否则逐个尝试接受"可选"定位出口——接受时 `CopyAxle` 出临时轴、逐项应用出口的界（位置经模 $d$ 移位）、若使此前拒绝者变为强制则放弃此路，递归深入；拒绝则 `s=-1` 并更新 `allowedch`，不等式一旦成立即返回。

### Reduce、SubConf、RootedSubConf：半可约测试

`Reduce(NULL,...)` 读 unavoidable.conf（`GetConf`），对每个构型 `GetQuestion` 编译提问、`Radius` 核验半径至多 $2$。`Reduce(A,...)` 实现 res-07j 定义的骨架测试：把轴压栈，弹栈后 `Getadjmat`/`GetEdgelist` 算出骨架的三角形函数表与"按度数对分组的边表"，对每个提问 `SubConf`——`SubConf` 枚举 `edgelist` 中"提问前两顶点的度数对"对应的骨架边作为起点，`RootedSubConf` 从起点沿提问序列走：`adjmat[image[u]][image[v]]` 给出下一顶点，度数（`xi`）不符或顶点重复即失败，走完后核验良置。任一提问成功即找到好配置；此后把骨架中"上界未固定"的内部顶点逐一压低上界压栈（对应 (7.2) 前引理：好配置出现只依赖上界，降低上界是分支的机器形态）；栈空即半可约成立，返回 1。`CheckIso` 是独立的复核：单射性、度数一致、扇位置合法（(T4) 的检查）、良置、三角形保序（`adjmat[x][y]==image[w]`）、诱导性（`INDUCHECK` 宏按轴的轮辐-帽-扇结构逐位置核对）——这正是 res-07j 提到的"生成同构与验证同构分开"。

### Getadjmat、DoFan、GetEdgelist、GetQuestion

`Getadjmat` 构建骨架的三角形函数表：`adjmat[u][v]=w$ 表示 $u,v,w$ 构成顺时针三角形。轮辐 $i$ 的邻居（轮心 $0$、轮辐圈上的 $h$、帽 $deg+h$）的三角形直接赋值；$A.upp[i]<9$ 时按 $5..8$ 分档调 `DoFan` 展开辐扇的三角形（扇顶点 $2d+i,\dots$ 依次插入，档位对应扇顶点个数 $\gamma-5$，与 res-07j 定义（辐扇）一致）。`GetEdgelist` 按度数对收集骨架边（供 `SubConf` 起点枚举）。`GetQuestion` 从度数最大的内部顶点出发广度展开提问：先取起点与其次大度数邻居，然后沿循环序从已定顶点两侧展开三角形链（顺时针方向与逆时针方向各一轮），跳过环顶点，扇顶点链成段加入——得到满足 res-07j 定义（提问判据）的提问序列（每个新顶点与两个已定顶点成三角形）。

至此两个程序的所有函数都有了正文的对应。读完正文再对照本篇，reduce.c 与 discharge.c 的每一行都可以定位到文章的定义、定理或程序对照段。
