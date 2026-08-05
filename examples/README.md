# Grounded generation examples

These six original examples exercise the three requested generation modules in both supported output formats and writing languages. They are grounded only in [`paper-context.yaml`](paper-context.yaml); they do not quote or derive research facts from any external paper.

| Module | LaTeX | Markdown |
|---|---|---|
| Abstract | `abstract-en.tex` | `abstract-zh.md` |
| Experiment setup | `experiment-setup-en.tex` | `experiment-setup-zh.md` |
| Results analysis | `results-analysis-zh.tex` | `results-analysis-en.md` |

The English outputs are expected to use English surface conventions while borrowing only high-level organization from the Chinese profile. The Chinese outputs apply the inverse rule. Because the fixture corpus contains one paper per language, a real generation run must label its profile confidence as low.

The setup examples intentionally omit hardware, random seeds, stopping criteria, and parameters because the context does not supply them. The results examples do not claim statistical significance or offer an unsupported causal explanation.
