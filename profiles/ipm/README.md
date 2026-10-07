# IPM 可复用写作画像

这是蒸馏后的写作结构与表达画像，不是论文全文库或科学正确性审稿引擎。Git 只分发可复用画像及脱敏来源记录；PDF、全文、observations 和学习缓存留在服务器私有目录。

## 来源与覆盖

47 篇来源（1998–2026），46 篇纳入、1 篇因缺少适用论文结构排除。纳入部分为 44 篇实证/系统评估论文与 2 篇概念/反思论文。主要领域为 Web search/IR、广告、HCI、persona analytics 和数字测量；`IPM`（CLI slug：`ipm`）是原 `routing-literature` 画像的重命名，仍为 47 篇来源 / 46 篇纳入的混合会议与期刊语料（Jansen 语料），并非 IPM 专属语料或经认证的期刊规则，也不代表 routing optimization 领域专长。重命名未用 MinerU 重新解析来源，也未重新蒸馏论文，现有抽取限制不变。

| 模块 | 英文来源数 | 中文来源数 |
| --- | ---: | ---: |
| abstract | 45 | 0 |
| introduction | 45 | 0 |
| related-work | 45 | 0 |
| problem-definition | 37 | 0 |
| methodology | 41 | 0 |
| experiment-setup | 31 | 0 |
| results-analysis | 46 | 0 |
| conclusion | 43 | 0 |

计数是自动章节归类后的覆盖，不是独立实验或干净段落的认证数量。同作者、共享数据及会议/期刊版本可能重叠。中文模块全部为低置信度、零直接语料；70/30 是配置影响权重，不是中英文证据比例。

## 初始化与使用

在仓库根目录、已有兼容 `paper-alchemist` CLI 的 Linux 环境运行：

```bash
bash cyrus-setup.sh IPM
paper-alchemist validate-profile --profile ipm --workspace .
```

（不带参数运行 `bash cyrus-setup.sh` 同样默认安装并校验 IPM）。脚本将本目录复制到 `.paper-alchemist/profiles/ipm/`，先验证隔离的临时副本，再执行安装。已有画像只验证、不覆盖；无效就失败退出，请人工检查，不要删除私有数据来强行通过。脚本不安装外部依赖，也不下载论文。

CLI 从工作区的 `.paper-alchemist/profiles/` 读取画像，不能直接把 `profiles/` 当作工作区校验。要求 `generation_ready: true`，但此门禁不代表所有模块高置信度。

按照根目录 `AGENTS.md` 和 `.claude/skills/paper-alchemist/SKILL.md`，阅读相关语言/模块、integrated 与 bilingual 文件后使用。保留原稿事实、数字、引用及结论力度；可做表达润色、结构诊断与证据缺口标记，不能借语料中的事实补写原稿或冒充已验证的科学审稿结论。

## 可追溯性与限制

- `source-manifest.json` 保存来源、排除记录及输入哈希。`corpus/jansen-learning/...` 等相对路径仅是私有来源定位记录，不是本仓库附带文件或下载链接。
- 英文模块中的私有 observation 路径已移除。公开包支持画像复用，但不能单独重建全部蒸馏过程。
- 旧 PDF 的字体/编码、Poppler syntax/xref、表格公式及列序恢复未获认证；自动章节路由可能存在串栏、标题缺失及内容污染。
- 跨领域、中文写作或科学事实验证需额外证据。详细限制见 `en/integrated.md`、各模块及双语整合文件。
- 本次从 Git 索引移除旧工作区画像不等于清除 Git 历史，也不会删除服务器上保留的私有画像。
