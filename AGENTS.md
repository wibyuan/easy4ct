# AGENTS.md

## 项目概述

easy4ct：基于启发式搜索的四色定理多样性证书开源生成器——"四色异迹"系统（本科生研究项目）。

当前阶段：资料整理、文章撰写（`doc/res.md`）、RSST 1997 验证代码的溯源与复现。

## 目录约定

- `doc/`：开源后保留的公开文档（`res.md` 文章主产物、`doc/papers/` 四篇公版论文 OCR：Kempe 1879 / Tait 1880 / Heawood 1890 / Birkhoff 1913）。
- `docs/`：内部文档（项目申请书、个人信息、RSST 1997 OCR——Elsevier 版权，不可分发），已被 `.gitignore` 忽略、不进入版本控制；开源前须整体删除。
- `README.md` 记录完整约定，修改目录结构时同步更新。

## 协作规则（用户明确要求，必须遵守）

1. **逐步确认制**：每一步先盘问细节、与用户达成一致再动手；禁止自动推进整个任务链。
2. **理清决策依赖**：先做前置决策（如：先定下载源 → 再定目录结构 → 再谈实现），后做后置决策；不要越级推进。
3. **先查库再问**：能从仓库已有代码/文本（`doc/`、`docs/` 的 OCR、`res.md`）回答的问题，先探索再提问。
4. **每个问题必带推荐答案**：不允许把决策纯抛给用户。
5. **细粒度 commit**：单次修改独立提交，禁止把多个不同修改合并为一个 commit。
6. **一次只问一个问题**。
7. **用户 abort 是停止信号**：用户中止命令后，立即停止当前动作，总结汇报，等待指示。

## 脱敏纪律（开源前强制）

- `docs/`、申请材料、个人身份信息（姓名、学号、手机、邮箱、学校与项目计划关联）不得出现在任何已跟踪文件中。
- 历史中若存在敏感内容，未推送时直接重写本地历史；已推送需 `git filter-repo` 清历史后再 force push。

## RSST 代码溯源状态

- 论文 OCR 中记录的原始地址（1997）：`http://www.math.gatech.edu/~thomas/FC/ftpinfo.html` —— 返回 301 重定向至 https 同路径（此前 webfetch 误报 404，实为 https 路径缺失）。
- 现行地址（2017 更新）：`https://people.math.gatech.edu/~thomas/FC/fourcolor.html`（301 → `https://thomas.math.gatech.edu/FC/fourcolor.html`）
  - 程序与数据目录：`http://people.math.gatech.edu/~thomas/OLDFTP/four/`（目录列表 403，需已知文件名直连）
  - 综述 PDF：`http://people.math.gatech.edu/~thomas/OLDFTP/fcdir/npfc.pdf`、`unavoidable.pdf`
- 分工：用户负责逐个下载文件到仓库；助手负责定位、验证连通性、跑通与讲解代码。
- 待决决策（按依赖顺序）：① 下载源确认 ② 落盘目录结构 ③ 构建/运行环境。

## 环境备注

- WSL（Linux）+ Windows 并存；Windows 侧有 PowerShell + Word/Excel COM（`/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe`），用于转换 `.doc/.xls` 等 Office 文件。
- Linux 侧 LibreOffice 无中文字体，转换中文 Office 文件请走 Windows COM 路线。
