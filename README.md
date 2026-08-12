# easy4ct

基于启发式搜索的四色定理多样性证书开源生成器——"四色异迹"系统。

当前阶段：已收录并跑通 RSST 1997 验证引擎（633 构型），正在撰写四色定理文章（已完成章节拆分，确立定义/定理引用块、证明起止标记、伪证标记与定义-定理分工规则等格式规范）。`res-06a`（顶点邻域的双圈结构）已由作者重新起草并续写完成：帽/扇顶点独立定义、分节组织，含外圈存在（面环排序）、外圈无弦、车轮构型存在唯一定理；续写部分尚有已知待修点（见 DEVLOG）。RSST 定义核查中发现引理 (4.1) 的字面表述疏漏（正二十面体 edge case，不影响证明实质），判定结论见 `rsst/docs/RSST-cartwheel-γ-表述歧义分析.md`。

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
│   ├── res-08-参考.md
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
