# paper-alchemist on Cyrus

给 Linear 里新建的 AutoVerse Agents 会话用。

技能在 `.claude/skills/paper-alchemist/`。Claude 会话从这里加载。命令包装在 `.claude/commands/`。

议题正文写：

```text
[agent=claude]
[repo=paper-alchemist]
```

`[agent=claude]` 选择 Claude。`[repo=paper-alchemist]` 选择本仓库。两个标签都写在正文里。

`cyrus-setup.sh` 确认 CLI、skill 启动和默认画像可用。它不下载论文，也不重新蒸馏。

## 已蒸馏画像

默认画像为 `jansen-2020-2026`，完整模块及整合文件在 `.paper-alchemist/profiles/jansen-2020-2026/`，跟随 main 分支进入每个新工作区。润色任务无需重新下载 PDF。Agent 应按根目录 `AGENTS.md` 加载相关模块，保留原稿事实、数字和引文。

画像基于 10 篇英文公开可下载论文，中文无语料，部分模块没有独立证据；自动章节抽取存在串栏与章节污染。详细覆盖、来源哈希和限制见画像 README 与审计文件。不能把可用性门禁通过理解为所有模块高置信度。

Linear 议题示例：

```text
[agent=claude]
[repo=paper-alchemist]
使用仓库自带的 jansen-2020-2026 画像润色下面的英文摘要。
保留全部数字、引用和研究结论，仅改表达与组织。
<附上需要润色的原稿>
```

新建 Linear 会话即可检出最新 main；已有会话的 worktree 不会自动更新。本地模拟验证覆盖 worktree、初始化和画像调用，不包含真实 webhook 或远程 Agent 自动发现。
