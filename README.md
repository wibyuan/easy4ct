# easy4ct

基于启发式搜索的四色定理多样性证书开源生成器——"四色异迹"系统。

当前阶段：已收录并跑通 RSST 1997 验证引擎（633 构型），四色定理文章按 res-plan 分块推进。`res-01`~`res-06a` 已完成（作者重写 + 助手续写）；第六部分（可约性判定）与第七部分（放电法）的续写底稿已全部完成并提交待审：`res-07c`（D-可约与收缩判据）、`res-07d`（从自由补全回到 T，含 (3.3)(3.4) 自证与 (3.7) 目标定理）、`res-07e`（633 清单与权衡）、`res-07f`（构型的机器表示）、`res-07g`（三染色枚举与一致集迭代）、`res-07h`（contract 验证）、`res-07i`（放电法）、`res-07j`（放电的机器可读证明）——均待作者审阅；第七部分沿用 res-07 系列编号。`res-08-参考.md` 已改名 `res-ref-参考.md`，`res-08`/`res-09` 号留给第八部分（完整证明过程与染色算法）与第九部分（交互式证明器），规划见 `res-plan.md` 块 12/13。术语体系约定见 AGENTS.md 规则 17。RSST 引理 (4.1) 的字面表述疏漏的完整判定见 `rsst/docs/RSST-(4.1)-字面失效范围刻画底稿.md`。

## 目录结构

```
.
├── README.md
├── DEVLOG.md     # 项目开发日志
├── AGENTS.md     # 协作规则与项目约定（供 AI 助手与协作者阅读）
├── doc/          # 开源后保留的文档
│   ├── res.md          # 四色定理证明文章完整副本（主产物，持续撰写）
│   ├── res-01-序章.md  # 文章按章节拆分的编辑文件（01~08）
│   ├── res-02-基础转化.md
│   ├── res-03-欧拉公式与不可避免集.md
│   ├── res-04-可约构型与双色链.md
│   ├── res-05-两大著名伪证.md
│   ├── res-06-连通性归约.md
│   ├── res-06a-顶点邻域的双圈结构.md
│   ├── res-07-可约性判定.md
│   ├── res-07a-标准构型与自由补全.md
│   ├── res-07b-环染色与一致集.md
│   ├── res-07c-D-可约与收缩判据.md
│   ├── res-07d-从自由补全回到T.md
│   ├── res-07e-633清单与权衡.md
│   ├── res-07f-构型的机器表示.md
│   ├── res-07g-三染色的枚举与一致集的迭代.md
│   ├── res-07h-contract的验证.md
│   ├── res-07i-放电法.md
│   ├── res-07j-放电的机器可读证明.md
│   ├── res-07k-代码导览.md  # reduce.c/discharge.c 逐函数导览（完稿待审 3dd63b8）
│   ├── res-plan.md  # 续写全局分片规划（块 4-13：定义-定理分工、代码映射、术语候选）
│   ├── res-08-完整证明过程与染色算法.md  # 第八部分（完稿待审 1be04ba）
│   ├── res-09-交互式证明器.md  # 第九部分（完稿待审 d026cb5）
│   ├── res-ref-参考.md
│   ├── format-example.md # 文章格式参考样例（知乎《环》一文）
│   ├── figures/        # 文章插图
│   └── papers/         # 公有领域论文的 OCR 文本（供文章引用）
│       ├── Kempe-GeographicalProblemFour-1879.md
│       ├── Tait1880.md
│       ├── Heawood1890.md
│       └── Birkhoff-ReducibilityMaps-1913.md
├── rsst/         # RSST 1997 验证代码（学术用途转载，见其 README）
│   ├── README.md       # 来源、文件清单与版权说明
│   ├── code/           # reduce.c / discharge.c / discharge.pas / 数据与证明
│   └── docs/           # 文档、图解与 OCR 文本
├── fourcolor/    # Gonthier Coq 形式化证明（submodule，CeCILL-B 许可）
└── docs/         # 内部文档（.gitignore 忽略，开源前整体删除）
    └── target/   # 项目申请书、内部表单等（含个人信息）
```

## 设计约定

- `doc/`：持续维护的公开内容，随仓库一起开源。
- `docs/`：内部资料，包含版权论文与个人信息，**不入库、开源前删除**。
- `doc/papers/` 仅收录著作权已过期的公版论文；RSST 1997（《The four-colour theorem》, JCTB 70(1), 2-44）仅作引用，附 DOI 即可。
- `rsst/`：RSST 验证引擎，源码头声明仅授学术研究用途，转载保留作者署名。
- `fourcolor/`：rocq-community/fourcolor submodule（Gonthier Coq 形式化），CeCILL-B 许可，随仓库分发。

## 任务背景

对 RSST 1997 年 C 语言验证引擎（633 构型）进行底层解耦（C-API），引入 AI 启发式搜索生成放电规则变体，构建"生成-验证"一体化的开源管线，探索四色定理的多样化证明证书。
