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
  - 定义/定理/引理用引用块（`> **定义（名称）**`），定义正文中的核心术语同样加粗；
  - 证明以 `**证明：**` 开始（其后换行留空行接内容）、以 `$\blacksquare$` 结束（紧跟证明末句同行，其后换行留空行）；多情形证明用 `**证明1（xxx）：**`/`**证明2（xxx）：**`（同行直接接内容）；
  - 证明块内不得嵌套引用块，也不得嵌套证明块，引用块与证明块须平级排列；
  - 图注允许图片后空行，不加公式渲染（转 LaTeX 时再补）。
- 对 `res-01` ~ `res-06` 完成格式改造：行文式定义改为引用块（如"定义一个图是平面图"→ 定义（平面图））、补齐全部证明起止标记、定义正文核心术语加粗、将证明块内嵌套的引理/定理/定义移出平级排列（res-02 的"两种性质"证明、res-06 的"极小点割集"引理等）。
