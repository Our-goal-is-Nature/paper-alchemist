# paper-alchemist on Cyrus

给 Linear 里新建的 AutoVerse Agents 会话用。

技能在 `.claude/skills/paper-alchemist/`。Claude 会话从这里加载。命令包装在 `.claude/commands/`。

议题正文写：

```text
[agent=claude]
[repo=paper-alchemist]
```

`[agent=claude]` 选择 Claude。`[repo=paper-alchemist]` 选择本仓库。两个标签都写在正文里。

`cyrus-setup.sh` 只确认 `paper-alchemist` 命令和技能目录。它不下载论文，也不创建画像。
