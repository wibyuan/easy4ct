# RSST 四色定理验证代码

Robertson–Sanders–Seymour–Thomas 1997 年四色定理机器证明的原始验证程序与数据。

## 来源

- 原始地址（论文 [1] 附录记载）：`http://www.math.gatech.edu/~thomas/FC/ftpinfo.html`（已失效）
- 现行镜像：`https://thomas.math.gatech.edu/OLDFTP/four/`（程序与数据）、`https://thomas.math.gatech.edu/OLDFTP/fcdir/`（文档与图解）
- 主页：`https://thomas.math.gatech.edu/FC/fourcolor.html`
- arXiv 备份：[arXiv:1401.6481](https://arxiv.org/abs/1401.6481)（可约性）、[arXiv:1401.6485](https://arxiv.org/abs/1401.6485)（放电）

## 目录内容

`code/`：程序与数据

| 文件 | 用途 |
|---|---|
| `reduce.c` | 可约性验证程序（C），对应论文 (3.2) |
| `discharge.c` | 放电规则验证程序（C），对应论文 (4.9) |
| `discharge.pas` | Heckman 用 Pascal 独立重写的放电程序 |
| `unavoidable.conf` | 633 个不可避免构型数据（格式见 ftpinfo.html） |
| `rules` | 放电规则的机器可读形式 |
| `present7` ~ `present11` | (4.9) 五情形的不可避免性形式化证明 |

`docs/`：文档与图解

| 文件 | 用途 |
|---|---|
| `reduce.ps` | `reduce.c` 的使用文档（即 `reduce.tex`） |
| `discharge.ps` | `discharge.c` 的使用文档（即 `discharge.tex`） |
| `unavoidable.ps.gz` | 633 构型的图解版本 |
| `npfc.pdf` | 10 页综述（A New Proof of the Four Colour Theorem） |
| `unavoidable.pdf` | 不可避免性证明的概述 |

## 版权说明

`reduce.c` 与 `discharge.c` 头部均载明：

> Copyright 1995 by N. Robertson, D.P. Sanders, P.D. Seymour and R. Thomas.
> Permission to use for the purpose of scholarly research is hereby granted.

即明确授予**学术研究用途**的使用许可；论文 [1] 正文亦称 "we are making the
necessary programs and data available to the public for checking"。
本目录转载仅供学术研究与验证目的，**保留作者署名**，不声明为本项目自有代码。
若需修改再分发或商用，请自行确认许可状况。

论文正文（JCTB 70(1), 2-44，Elsevier 版权）不在本目录中，仅作引用：

[1] N. Robertson, D. P. Sanders, P. Seymour, R. Thomas, *The four-colour
theorem*, J. Combin. Theory Ser. B 70(1) (1997) 2–44.
doi:10.1006/jctb.1997.1750
