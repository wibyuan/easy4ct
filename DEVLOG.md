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

### 待办

- [ ] 为 `rsst/` 添加来源与版权说明 README
- [ ] 跑通 `reduce.c` / `discharge.c`，建立对验证代码的基本认识
