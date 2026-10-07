# paper-alchemist on Cyrus

给 Linear 里新建的 AutoVerse Agents 会话用。Cyrus 已接入本仓库；本次更新不需要修改 `.env` 或重启服务。

## 选择仓库与 Agent

议题正文写：

```text
[agent=claude]
[repo=paper-alchemist]
```

`[agent=claude]` 选择已安装的 Claude adapter；省略时默认 runner 为 Cursor。`[repo=paper-alchemist]` 选择本仓库，也可写 `[repo=paper-alchemist#main]`。这些是正文路由指令，不是仅供展示的标签。

技能在 `.claude/skills/paper-alchemist/`，命令包装在 `.claude/commands/`。Agent 必须按根目录 `AGENTS.md` 显式读取 `SKILL.md` 和相关参考文件；不能假定 Cursor 自动加载 Claude skill。

## 默认画像与初始化

默认画像为 **IPM**（显示名称：IPM，CLI 规范 slug 与元数据：`ipm`）。Git 发布包在 `profiles/ipm/`；CLI 使用的工作区画像在被 Git 忽略的 `.paper-alchemist/profiles/ipm/`。

在已有兼容 `paper-alchemist` CLI 的 Linux 环境、仓库根目录运行：

```bash
bash cyrus-setup.sh IPM
paper-alchemist validate-profile --profile ipm --workspace .
```

（不带参数运行 `bash cyrus-setup.sh` 同样默认安装并校验 IPM）。

`cyrus-setup.sh` 的安装与校验机制：
1. 自动发现 `profiles/` 下所有带 `source-manifest.json` 的直接公开画像目录。
2. 对每个待安装的公开画像，先复制到隔离临时工作区（如 `.paper-alchemist/profiles/.profile-install-*`），在该隔离副本中运行 `paper-alchemist validate-profile`，校验通过后再重命名/移动到目标路径。
3. 若本地目标画像已存在，只执行校验、不覆盖本地内容（保留本地画像及可能的较新本地修改）。
4. 接收可选的选中画像参数（位置参数或 `--profile`，默认 `IPM` / `ipm`）；在处理完公开包后，对最终选中的画像执行校验门禁：`validate(workspace, selected)`，必须满足 `generation_ready: true`。
5. 任何步骤（依赖检查、临时副本校验、目标校验、所选画像门禁）失败立即退出并中止流程，绝不静默忽略失败。脚本不下载 PDF、不调用外部 API、不重新蒸馏，也不删除或修改已有私有数据。

Agent 必须确认初始化成功并要求所选画像 `generation_ready: true`。Cyrus 可能在 setup 失败后仍建立工作区，所以不能把“会话已启动”当作画像可用；setup 或校验失败时必须停止写作并报告错误，严禁通过删除私有数据或静默换用其他画像来绕过门禁。

## 画像选择与门禁规则（含 npj 示例）

- 默认使用 IPM 画像；若用户在提示词中显式指定了其他画像（例如 `npj` 或某个私有本地画像），Agent 必须尊重用户的显式选择，不得静默退回 IPM。
- 显式指定画像时，运行 `bash cyrus-setup.sh <selected>`，并运行 `paper-alchemist validate-profile --profile <selected_slug> --workspace .`。
- 门禁规则：所选画像必须具备完整的生成就绪状态（`generation_ready: true`）。若该画像未安装、未发布 bundle 或校验失败，setup 将直接退出报错，Agent 必须停下并向用户报告门禁失败，绝不能在后台静默降级或用 IPM 冒充所选画像。

### npj 画像示例与背景说明

- **语料范围**：`profiles/npj/` 中的 `npj` 画像基于 5 篇合著论文（发表于 *npj Digital Medicine*，2021–2026 年）：包含 2 篇实证/系统评估论文（empirical）、1 篇叙述性综述（narrative review）和 2 篇概念/观点论文（conceptual）。
- **抽取局限与 Agent 处理**：该语料采用 MinerU 解析，但 MinerU 的解析结果并非完美（例如表格、插图标注、公式或多栏阅读顺序可能存在瑕疵与噪声）；蒸馏时已排除表格/图像、附录、重复封面页眉以及评论的 Box 串栏污染片段；未认证数值/视觉保真，使用时必须保留这些限制。
- **覆盖与门禁**：摘要/引言/相关工作/问题定义/结尾各 5 篇，方法/实验设置各 2 篇且低置信度，结果分析 3 篇（两篇实证加一篇叙述综述）。中文零直接语料。公开包见 [npj README](profiles/npj/README.md)；初始化后仍须校验所选画像，失败不得用 IPM 代替。

## IPM 覆盖与用途边界

画像记录 47 篇来源（1998–2026），46 篇纳入、1 篇排除（CACM 2006 无小标题叙事论文因缺乏结构排除）。纳入部分含 44 篇实证/系统评估论文与 2 篇概念/反思论文。主要领域是 Web search/IR、广告、HCI、persona analytics 和数字测量（Jansen 语料），不是 routing optimization。各英文模块覆盖 31–46 篇来源，详细统计见 [画像 README](profiles/ipm/README.md)。

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

**核心事实与限制**：
- `IPM`（CLI slug：`ipm`）是原 `routing-literature` 画像的重命名，仍为 47 篇来源 / 46 篇纳入的混合会议与期刊语料，**不是 IPM 专属语料或经认证的期刊规则**，亦未代表 routing optimization 领域专长。
- **重命名未用 MinerU 等工具重新解析来源**，未重新蒸馏论文，现有的章节抽取限制保持原样。
- 中文所有模块均为零直接语料、低置信度；70/30 是配置影响权重，不是中英文证据比例。
- 来源可能共享作者、数据或会议/期刊版本，覆盖数量不是独立复现次数。旧 PDF 字体/编码、公式表格与列序恢复未获认证，自动章节抽取可能串栏或污染。门禁通过不等于所有模块高置信度。
- 这套画像用于表达润色、结构诊断和证据缺口标记，不是科学事实审稿知识库。必须保留原稿事实、数字、引用键及结论力度，不能借语料中的事实补写原稿。科学正确性、实验有效性和引用真实性需要另行查证。
- Git 只发布可复用画像和脱敏来源记录。PDF、全文、observations、学习缓存和私有数据留在服务器私有目录。manifest 的 `corpus/jansen-learning/...` 相对路径仅用于定位私有来源，不是附带资源或下载链接；公开包不能独立重建全部蒸馏过程。从 Git 删除旧画像不会清除 Git 历史。

## Linear 润色模板（默认 IPM）

```text
[agent=claude]
[repo=paper-alchemist]
使用仓库自带的 IPM 画像润色下面的英文摘要。
先按 AGENTS.md 读取 skill、相关模块及整合文件，运行 bash cyrus-setup.sh IPM，检查初始化成功且 generation_ready: true；失败则停止并报告。
保留全部事实、数字、引用键和结论力度，仅改表达与组织，不从语料补写事实。
输出润色稿、关键修改说明，以及无法核实的证据缺口；说明中文零语料、混合会议语料及抽取限制。
原稿：
<附上需要润色的原稿>
```

## Linear 结构审查模板（默认 IPM）

```text
[agent=claude]
[repo=paper-alchemist#main]
使用 IPM 画像检查以下论文的表达与结构，而非判断科学事实正确性。
先按 AGENTS.md 加载 skill 与相关模块，运行 bash cyrus-setup.sh IPM，检查初始化成功且 generation_ready: true；失败则停止并报告。
逐项报告问题位置、结构/表达问题、修改建议，以及需要作者提供证据的缺口。
区分“原稿已有证据”“待核实科学主张”和“画像中的写作模式”；不虚构数据、引用或实验，不增强结论力度。
说明该画像的领域范围（混合语料非 IPM 专属）、中文零直接语料及抽取限制。
原稿：
<附上需要审查的原稿>
```

## Linear npj 显式选择模板（门禁示例）

```text
[agent=claude]
[repo=paper-alchemist]
使用 npj 画像润色下面的论文摘要。
先按 AGENTS.md 运行 bash cyrus-setup.sh npj，门禁校验该所选画像并要求 generation_ready: true；若 npj 画像未就绪或校验失败，立即停止并报告，不得静默回退或用 IPM 冒充。
（注：npj 画像基于 5 篇合著 npj Digital Medicine 2021-2026 论文，包含 2 篇实证、1 篇叙述性综述、2 篇概念性论文；MinerU 解析并非完美，相关片段与局限需由 Agent 处理；保留原稿事实、数字和引用键，不将概念建议冒充实验结论）。
原稿：
<附上需要润色的原稿>
```

## 更新与验收范围

推送更新后，使用新会话的新 worktree 获取最新 `main`。已有会话不会自动更新；需要复用旧会话时，先人工确认其提交和工作区状态，不覆盖会话里的用户改动或私有画像。

本地 setup、画像校验及干净 worktree 测试只能证明本地初始化与门禁可用，不能替代真实 Linear webhook、远程 Agent 执行或论文润色效果的端到端验收。
