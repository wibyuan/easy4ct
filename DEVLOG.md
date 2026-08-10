# DEVLOG

项目开发日志，记录关键决策与进展。随时间线追加。

## 2026-08-09

### 仓库初始化与目录约定

- 确立目录约定：`doc/` 为开源后保留的公开文档；`docs/` 为内部文档（不入库，开源前整体删除）。
- 新增 `README.md`、`AGENTS.md`（协作规则、RSST 溯源状态、脱敏纪律）、`.gitignore`（忽略 `docs/`）。
- git 历史经历一次脱敏重写：早期提交曾包含内部文档与个人关联信息，已通过清空引用 + `gc --prune` + 重建提交彻底清除，远端已 force push 覆盖。

### RSST 代码溯源

- 论文 OCR 记录的 1997 年地址 `www.math.gatech.edu/~thomas/FC/ftpinfo.html`：http 301 → https 同路径 404，已失效。
- 主页 `people.math.gatech.edu/~thomas/FC/fourcolor.html`（2017 更新）301 → `thomas.math.gatech.edu/FC/fourcolor.html`。
- 关键发现：最终域名 `thomas.math.gatech.edu/FC/ftpinfo.html` 仍存活（HTTP 200），即官方文件清单页，列出全部程序与数据。
- `OLDFTP/four/` 目录列表被禁（403），必须已知文件名直连。

### RSST 代码下载（8 个文件，全部 200）

落盘 `rsst/code/`：

| 文件 | 内容 |
|---|---|
| `reduce.c` | 可约性验证程序（C） |
| `discharge.c` | 放电规则验证程序（C） |
| `discharge.pas` | Heckman 的 Pascal 版放电程序 |
| `unavoidable.conf` | 633 个不可避免构型数据 |
| `rules` | 放电规则（机器可读） |
| `present7` ~ `present11` | (4.9) 五情形不可避免性证明 |

### 构建与验证（本机 Ubuntu / gcc 15.2.0）

- 90 年代 K&R C 与现代 gcc 不兼容（隐式声明、旧式函数定义报错），
  以 `gcc -std=gnu90 -O2` 编译，不改动原始源码。
- 生成的二进制 `reduce`、`discharge` 放 `rsst/code/`，不入库。

#### reduce（可约性验证，论文 (3.2)）

- 用法：`./reduce [构型文件]`，默认读 `unavoidable.conf`。
- 方法（见源码 main）：对每个构型计算 `findangles`（环染色角度结构）→
  `findlive`（初始可行染色集 C0）→ `testmatch`/`updatelive` 迭代
  （由 Ci 推 C{i+1}）→ `checkcontract`（核验契约正确性）。
- 响应：`Reducibility of 633 configurations verified`
- 耗时：46.6 s（1997 年 Sun Sparc 20 约 3 小时）。

#### discharge（放电与不可避免性验证，论文 (4.9)）

- 用法：`./discharge <present文件> [<行号> <打印模式>]`；
  运行时读取 `rules`（放电规则）与 `unavoidable.conf`（构型集）。
- 响应（对 present7–present11 逐一执行）：

```
Total of 633 configurations.
present7 verified.  …  present11 verified.
```

### 收尾（2026-08-09 晚）

- 下载 `fcdir/` 文档至 `rsst/docs/`（`reduce.ps`/`discharge.ps`/`unavoidable.ps.gz`/`npfc.pdf`/`unavoidable.pdf`）。
- 为 `rsst/` 添加 README（来源、文件清单、版权说明）。
- `reduce`/`discharge` 编译产物与 `.et` 中间文件通过 `.gitignore` 忽略，不入库。
- 修正 `rsst/README.md` 版权说明：源码头声明 "Permission to use for the purpose of scholarly research is hereby granted"。

## 2026-08-10

### 新增文件处置

- 插图（30 张 PNG）从根目录 `assets/` 移入 `doc/figures/`；`doc/res.md` 的图片引用统一改为相对路径 `doc/figures/`（此前为 Windows 绝对路径，跨平台断链）。
- 收录 RSST 相关 OCR 文本至 `rsst/docs/`：arXiv 1401.6481（可约性文档）、npfc 综述。
- Windows `:Zone.Identifier` 下载标记文件：删除并加入 `.gitignore`（`*:Zone.Identifier`）。
- 更新 README 目录结构（新增 `DEVLOG.md`、`rsst/`、`doc/figures/`）。

### 文章拆分与格式规范化（res.md）

- `res.md`（668 行）按章节拆分为 8 个编辑文件 `doc/res-01-序章.md` ~ `res-08-参考.md`，标题层级升一级（`##`→`#`、`###`→`##`）；原 `res.md` 保留完整副本。
- 修正拆分中发现的格式问题：首部空行、第 65 行列表粘连（"点连通度的定义"与 Kuratowski 清单挤在同一行）、`![img]` alt 不一致、参考条目 7 缺空格。
- 逐步确立文章格式规范（写入 AGENTS.md）：
  - 定义/定理用引用块（`> **定义（名称）**`），定义正文中的核心术语同样加粗；
  - 证明以 `**证明：**` 开始（其后换行留空行接内容）、以 `$\blacksquare$` 结束（紧跟证明末句同行，其后换行留空行）；多情形证明用 `**证明1（xxx）：**`/`**证明2（xxx）：**`（同行直接接内容）；
  - 证明块内不得嵌套引用块，也不得嵌套证明块，引用块与证明块须平级排列；
  - 图注允许图片后空行，不加公式渲染（转 LaTeX 时再补）。
- 对 `res-01` ~ `res-06` 完成格式改造：行文式定义改为引用块（如"定义一个图是平面图"→ 定义（平面图））、补齐全部证明起止标记、定义正文核心术语加粗、将证明块内嵌套的引理/定理/定义移出平级排列（res-02 的"两种性质"证明、res-06 的"极小点割集"引理等）。

### 格式规范收尾（2026-08-10 晚）

- 补充规则并逐文件落实：
  - 引用块内禁用列表结构（无序/有序均不允许），多个性质须以连贯语句联系——res-02"两种性质"定理改连贯语句；
  - 定理与其对应证明块之间不得嵌套引用块/证明块——res-02 辅助结论移至主定理前，res-06"Birkhoff 分离圈可约性"拆分（4-分离圈定理独立紧邻证明）；
  - 命题块、引理块统一改为定理块（引理均带证明，并入定理类别）；
  - 公式 `$...$` 内禁首尾空格（如 `$G_1 $` → `$G_1$`）；
  - Kempe 伪证的证明标记用 `**伪证：**`（换行空行接内容、`$\blacksquare$` 结束），与正常证明区分；
  - 定义正文中被定义的核心术语同样加粗。
- 全文复查无嵌套、无引用块内列表、无公式内空格。

### RSST 定义核查：cartwheel γ 表述疏漏（2026-08-10 晚）

- 重写 `res-06a`（顶点邻域的双圈结构）前，按"严谨到死"标准核查 RSST 配置/cartwheel 定义，发现字面矛盾：按"配置出现在 $T$ 中"（$\gamma_K(v)=d_T(v)$ 对所有顶点）与配置公理 (iii)（环尺寸 $\ge2$），正二十面体（内部 6 连通三角剖分）的顶点不存在合法 cartwheel——帽顶点在 $G(W)$ 中度 4、在 $T$ 中度 5，$\gamma=5$ 时环尺寸 $\sum(5-4-1)=0<2$。
- 结论：RSST 引理 (4.1) 存在**字面表述疏漏**（正二十面体为反例），非逻辑错误，不影响四色定理证明实质（二十面体可 4-染色、非最小反例；Gonthier 2005 Coq 形式化兜底）。
- 曾推测"隐含约定"假说（帽顶点 $\gamma$ 取使环尺寸 $\ge2$ 的值）——已排除：$(4.5)$ 轮辐 $\gamma$ 任意取值符合 $\gamma=d_T$（轮辐度数本就任意）；$(4.2)$ 数值矛盾（空和 $0\ne120$）只推出"失效无害"，推不出隐含约定。
- 分析全文落盘 `rsst/docs/RSST-cartwheel-γ-表述歧义分析.md`。
- 待验证：Gonthier Coq 代码（决定性）；失效是否严格限于二十面体（帽子度 5 局部结构未完全排除）。
- 对文章影响：`res-06a` 重写需显式处理该 edge case（写作策略待定）。

### Gonthier 形式化 submodule 与 cartwheel 判定（2026-08-10 晚）

- 版权处置：用户放入根目录的两篇 Gonthier 文章 OCR（Notices AMS 2008《Formal Proof—The Four-Color Theorem》，© AMS 不可再分发；HAL 2023 报告 hal-04034866）移入 `docs/`（gitignore 忽略、开源前删除），与 Elsevier 版 RSST OCR 同类处理。
- 添加 `fourcolor/` submodule（git@github.com:rocq-community/fourcolor.git，CeCILL-B 许可），README 目录树同步更新。
- 决定性验证完成——在 Coq 代码中检索 cartwheel/环/配置定义（`birkhoff.v`、`revsnip.v`、`redpart.v`）：
  - Gonthier 形式化**没有 RSST 式的 γ 记账**：配置（part）精确匹配（`redpart`），环是简单圈（`proper_ring`：非空且非单边轨道），环尺寸 = 轮廓尺寸，不存在 $\sum(\gamma-d-1)$ 型自由补全算术，故不可能出现"环尺寸 0"；
  - (4.1) 的内容对应物在 `birkhoff.v` Section SpokeRing：极小反例中每个面 x 的轮辐环 `spoke_ring` 是简单环（`scycle_spoke_ring`）、无弦（`chordless_spoke_ring`）、环盘恰为 x 的邻面（`diskF_spoke_ring`）、尺寸 = arity ≥ 5（`size_spoke_ring`/`min_arity`）；放电侧（present5~11）依赖该轮毂结构；
  - 全库无 "icosa"：形式化未排除、也不需要排除二十面体。对偶意义下正十二面体每个面都是合法 cartwheel（轮辐五边形环简单无弦、帽环轮廓尺寸 5 ≥ 2）——按 §5 判定树，**"隐含约定"说得到决定性支持**：RSST (4.1) 的数学内容（Birkhoff 双圈结构，含二十面体）自洽成立，字面失败仅是 RSST 自由补全记账（在帽圈之外另数一环）的表述瑕疵。
- 对文章影响不变：`res-06a` 重写时可引用此结论——RSST 字面按原文如实呈现、以 Gonthier 形式化佐证自洽约定；具体写作策略仍由作者决定。
