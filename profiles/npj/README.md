# npj 写作画像

基于 Judy Wawira Gichoya 参与的 5 篇 npj Digital Medicine 论文（2021–2026），不是个人模仿、全部著作清单或 npj 全系列/期刊官方写作规则。两篇实证研究、一篇非系统性叙述综述、两篇概念/评论；全文仅从合法 OA 来源取得。检索发现与题录核验使用 Autoverse；作者查询服务繁忙，按已核验篇目的完整作者名单消歧，检索覆盖不保证穷尽。

## 模块覆盖

| 模块 | 英文来源 | 中文来源 |
| --- | ---: | ---: |
| abstract | 5 | 0 |
| introduction | 5 | 0 |
| related-work | 5 | 0 |
| problem-definition | 5 | 0 |
| methodology | 2 | 0 |
| experiment-setup | 2 | 0 |
| results-analysis | 3 | 0 |
| conclusion | 5 | 0 |

方法和实验设置低置信度；结果分析为两篇实证加一篇叙述综述，不是三次系统评估。相关工作、问题定义和结尾常嵌在引言/方法/讨论中，功能片段可重叠，来源数不是独立复现次数。中文零直接证据，70/30 是配置影响权重，不是证据比例。

## 解析与学习边界

使用 MinerU 精准 API、`vlm`、英文及表格/公式识别解析 PDF。随后按审阅过的功能段落生成私有 canonical Markdown，排除重复封面、页眉、引用/作者信息、附录、图像及 HTML 表格；评论的 Box 1 串栏污染段落不参与提炼。已有 IPM 画像本次未重新解析。

MinerU 不等于无误解析：发现空格/词连接、重复段落、错误数值（例如 ICH 置信区间含双小数点）、Box 插入正文、表格续页和 accepted manuscript 页眉。未猜测修复数值，未认证原 PDF 的数值、公式、图表或阅读列序。两个下载版本为未编辑的已接受稿，不冒充最终排版。规范化后的段落/句长不是原版面的写作指标。

概念框架、建议试验设计与政策论证不作为已完成的方法、实验或结果。只提炼表达、结构和证据放置模式；不借语料数据、引用键或结论补写用户原稿，不将画像当科学事实审稿引擎。

## 初始化与使用

```bash
bash cyrus-setup.sh npj
paper-alchemist validate-profile --profile npj --workspace .
```

要求 `generation_ready: true`，已有本地画像只验证、不覆盖；失败停止，不回退到 IPM。读取 AGENTS.md、skill、相关语言模块、integrated 与 bilingual 文件后使用。

## 来源与隐私

source-manifest.json 保留 DOI、作者、题名、OA 记录、原 PDF/MinerU Markdown/canonical 哈希和解析策略。`private-corpus/npj/...` 仅为来源定位记录，不是公开附带文件或下载链接；公开包不能独立重建全文解析与学习。PDF、全文、布局 JSON、observations 和缓存保留服务器私有 `.paper-alchemist/`，公开包不含 API key、签名下载地址或代理凭证。
