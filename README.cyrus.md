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

默认画像为 `routing-literature`。Git 发布包在 `profiles/routing-literature/`；CLI 使用的工作区画像在被 Git 忽略的 `.paper-alchemist/profiles/routing-literature/`。

在已有兼容 `paper-alchemist` CLI 的 Linux 环境、仓库根目录运行：

```bash
bash cyrus-setup.sh
paper-alchemist validate-profile --profile routing-literature --workspace .
```

`cyrus-setup.sh` 检查 CLI、skill 和 launcher，将发布包复制到隔离临时工作区，通过验证后再安装。已有目标画像只验证、不覆盖；无效则退出。它不安装依赖、不下载 PDF、不重新蒸馏，也不删除或覆盖旧本地画像。

Agent 必须确认初始化成功并要求 `generation_ready: true`。Cyrus 可能在 setup 失败后仍建立工作区，所以不能把“会话已启动”当作画像可用；setup 或校验失败时应停止写作，报告错误，不通过删除私有数据绕过门禁。

## 覆盖与用途边界

画像记录 47 篇来源（1998–2026），46 篇纳入、1 篇排除；纳入部分含 44 篇实证/系统评估论文与 2 篇概念/反思论文。主要领域是 Web search/IR、广告、HCI、persona analytics 和数字测量，不是 routing optimization。各英文模块覆盖 31–46 篇来源，详细统计见 [画像 README](profiles/routing-literature/README.md)。

中文所有模块均为零直接语料、低置信度；70/30 是配置影响权重，不是中英文证据比例。来源可能共享作者、数据或会议/期刊版本，覆盖数量不是独立复现次数。PDF 字体/编码、公式表格与列序恢复未获认证，自动章节抽取可能串栏或污染。门禁通过不等于所有模块高置信度。

这套画像用于表达润色、结构诊断和证据缺口标记，不是科学事实审稿知识库。必须保留原稿事实、数字、引用键及结论力度，不能借语料中的事实补写原稿。科学正确性、实验有效性和引用真实性需要另行查证。

Git 只发布可复用画像和脱敏来源记录。PDF、全文、observations、学习缓存和其他本地画像留在服务器私有目录。manifest 的 `corpus/jansen-learning/...` 相对路径仅用于定位私有来源，不是附带资源或下载链接；公开包不能独立重建全部蒸馏过程。从 Git 删除旧画像不会清除 Git 历史。

## Linear 润色模板

```text
[agent=claude]
[repo=paper-alchemist]
使用仓库自带的 routing-literature 画像润色下面的英文摘要。
先按 AGENTS.md 读取 skill、相关模块及整合文件，检查初始化成功且 generation_ready: true；失败则停止并报告。
保留全部事实、数字、引用键和结论力度，仅改表达与组织，不从语料补写事实。
输出润色稿、关键修改说明，以及无法核实的证据缺口；说明中文零语料及跨领域限制。
原稿：
<附上需要润色的原稿>
```

## Linear 结构审查模板

```text
[agent=claude]
[repo=paper-alchemist#main]
使用 routing-literature 画像检查以下论文的表达与结构，而非判断科学事实正确性。
先按 AGENTS.md 加载 skill 与相关模块，检查初始化成功且 generation_ready: true；失败则停止并报告。
逐项报告问题位置、结构/表达问题、修改建议，以及需要作者提供证据的缺口。
区分“原稿已有证据”“待核实科学主张”和“画像中的写作模式”；不虚构数据、引用或实验，不增强结论力度。
说明该画像的领域范围、中文零直接语料及抽取限制。
原稿：
<附上需要审查的原稿>
```

## 更新与验收范围

推送更新后，使用新会话的新 worktree 获取最新 `main`。已有会话不会自动更新；需要复用旧会话时，先人工确认其提交和工作区状态，不覆盖会话里的用户改动或私有画像。

本地 setup、画像校验及干净 worktree 测试只能证明本地初始化与门禁可用，不能替代真实 Linear webhook、远程 Agent 执行或论文润色效果的端到端验收。
