<div align="center">

# Paper Alchemist

### 蒸馏优秀论文的写法，用可信证据完成写作。

一个与模型无关、支持模块化双语文风蒸馏和事实约束写作的 Agent Skill。

[![CI](https://github.com/Wang-Ruibin/paper-alchemist/actions/workflows/ci.yml/badge.svg)](https://github.com/Wang-Ruibin/paper-alchemist/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/Wang-Ruibin/paper-alchemist)](https://github.com/Wang-Ruibin/paper-alchemist/releases)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-6f42c1)](https://agentskills.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[English](README.md) · **简体中文**

</div>

## 为什么需要 Paper Alchemist？

论文语料可以告诉 Agent **应该怎样写**：摘要如何从问题推进到证据，引言如何放置研究缺口，结果分析如何区分观察与解释。但论文语料不能替你的研究回答 **什么是真的**。

Paper Alchemist 将这两类职责严格分离：

- 本地 Python 负责抽取、分段、哈希、统计和校验；
- 当前 Agent 负责跨论文语义蒸馏和正文写作；
- `paper-context.yaml` 与使用者明确回答的信息是研究事实的唯一来源；
- 内置脚本不调用任何 LLM API；
- 不模仿单一作者，也不在画像中保存论文长句。

## 核心能力

- **模块化蒸馏**：分别处理摘要、引言、相关工作、问题定义、方法、实验设置、结果分析和结论。
- **原生双语设计**：蒸馏阶段分别保存中英文证据；生成阶段同时借鉴两种语言，目标语言约占 70%。
- **事实约束生成**：语义画像未完成时禁止写作；检查当前章节缺失的研究事实，并只允许使用声明过的 citation key。
- **增量与续跑**：复用哈希一致的抽取缓存，只将受到语料变化影响的模块画像标记为过期。
- **支持图表型 PDF**：保留具有文本层的图表密集论文，统计图表引用，并可对低文本或扫描页执行 OCR。
- **跨 Agent 使用**：同一开放 Skill 支持 Codex、Claude Code、OpenCode、Hermes、Pi Agent 和 Kimi Code。
- **默认保护隐私**：论文原文、抽取全文、研究上下文和生成画像默认不进入版本控制。

## 60 秒上手

需要 Python 3.11 或更高版本。PDF 推荐安装 `pdftotext`，文本层抽取失败时回退到 `pypdf`。可选 OCR 需要系统 `PATH` 中同时存在 `pdftoppm` 和 `tesseract`；处理中文页面还需安装 Tesseract 中文语言数据。

```bash
git clone https://github.com/Wang-Ruibin/paper-alchemist.git
cd paper-alchemist
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
```

为当前 Agent 安装：

```bash
paper-alchemist install --agent codex --scope user
# agent: codex | claude | opencode | hermes | pi | kimi
# scope: user | project
```

蒸馏论文目录：

```bash
paper-alchemist distill ./papers --profile routing-literature --language auto --ocr auto
```

让已安装的 Skill 完成模块语义蒸馏，然后整合：

```bash
paper-alchemist integrate --profile routing-literature
paper-alchemist validate-profile --profile routing-literature
```

通过 Agent 生成摘要：

```text
/abstract profile=routing-literature lang=zh format=latex context=paper-context.yaml
```

## 工作原理

```mermaid
flowchart LR
    A[PDF / LaTeX / DOCX / Markdown / TXT] --> B[文本层 / 可选 OCR]
    B --> C[章节识别与图表引用统计]
    C --> D[私有中英文证据包]
    D --> E[Agent 按模块进行语义蒸馏]
    E --> F[中文画像与英文画像]
    F --> G[跨语言整合]
    H[已核验的 paper-context.yaml] --> I[事实约束章节生成]
    G --> I
```

1. `distill` 发现文件、抽取文本层或执行可选 OCR、排除参考文献和附录、检测语言、识别论文结构并生成私有证据包。
2. 当前 Agent 阅读证据包，将定量 seed profile 替换为跨论文语义规律。
3. `integrate` 拒绝未完成或已过期的模块画像，再生成中文、英文、跨语言和冲突画像。
4. 章节命令生成写作 brief，检查必要事实与引用，然后以指定语言和格式写作。

## 命令

| 命令 | 用途 |
|---|---|
| `distill SOURCE --profile NAME --language auto\|en\|zh --ocr auto\|never\|always` | 抽取并划分论文语料，可选 PDF OCR |
| `integrate --profile NAME` | 整合已经完成的语义画像 |
| `validate-profile --profile NAME` | 报告结构、语义、置信度和整合状态 |
| `brief MODULE --profile NAME --language en\|zh` | 生成受事实约束的双语写作 brief |
| `install --agent AGENT --scope user\|project` | 安装核心 Skill 与平台命令包装器 |
| `package-skill --output dist` | 构建 `paper-alchemist.skill` |
| `validate-skill [PATH]` | 校验可移植 Agent Skill 包 |

章节操作包括：

`abstract` · `introduction` · `related-work` · `problem-definition` · `methodology` · `experiment-setup` · `results-analysis` · `conclusion` · `section`

## Agent 支持

| Agent | 安装后的入口 |
|---|---|
| Codex | `$paper-alchemist abstract ...` |
| Claude Code | `/abstract ...` |
| OpenCode | `/abstract ...` |
| Hermes | `/abstract ...` |
| Pi Agent | `/abstract ...` |
| Kimi Code | `/skill:abstract ...` |

用户级、项目级目录和各平台原生行为见[平台说明](paper-alchemist/references/platforms.md)。

## 双语与事实边界

生成时按以下顺序使用画像：

1. 目标语言当前模块画像；
2. 另一语言当前模块画像；
3. 目标语言综合画像；
4. 跨语言结构画像；
5. 事实约束与学术写作底线。

另一语言只贡献修辞功能和信息组织，不迁移表层句式。如果某一种语言没有有效证据，系统会使用已有画像继续生成，并明确标记低置信度单语降级。

Paper Alchemist 不会编造贡献、方法、数据集、基线、参数、结果、显著性、局限或引用。LaTeX 使用 `\cite{key}`；Markdown 只使用上下文中声明的引用格式与 citation key。

对于图表型 PDF，语料可以用于提炼作者如何引入、比较和解释图表证据，但数值仍属于研究事实：只有当数值同时出现在 `paper-context.yaml` 中，或由使用者明确确认时，Agent 才能将其写入正文。OCR 只恢复文字，不推断曲线几何关系或未标注数值。

## 仓库结构

```text
paper_alchemist/             确定性 Python 引擎
paper-alchemist/             可移植 Agent Skill
adapters/                    跨 Agent 安装清单
.github/workflows/           最小构建与兼容性检查
```

公开仓库只包含可安装的项目主体。测试、原创 fixtures、事实约束样例、论文原文、抽取文本、生成画像、研究上下文和临时产物全部保留在本地，并由 Git 忽略。

## 验证情况

GitHub Actions 会在 Python 3.11–3.13 上检查构建、可移植 Skill 结构、打包、CLI 启动和六种 Agent 的安装器 dry-run。完整行为测试与真实论文语料验证仅在本地运行，避免 fixtures、生成画像或受版权保护的输入进入公开项目。

## 开发

```bash
python -m pip install -e '.[dev]'
ruff check paper_alchemist
paper-alchemist validate-skill
python -m build
paper-alchemist package-skill --output dist
```

## 开源协议

MIT © 2026 [misakimei0331](https://github.com/misakimei0331)。详见 [LICENSE](LICENSE)。
