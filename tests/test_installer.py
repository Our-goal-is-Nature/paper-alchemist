import pytest

from paper_alchemist.installer import AGENTS, install


@pytest.mark.parametrize("agent", sorted(AGENTS))
def test_installer_dry_run_for_every_agent(tmp_path, agent):
    result = install(
        agent,
        "project",
        tmp_path / "project",
        home=tmp_path / "home",
        dry_run=True,
    )
    assert result.agent == agent
    assert result.installed
    assert result.dry_run is True


def test_claude_installs_core_and_module_commands(tmp_path):
    project = tmp_path / "project"
    result = install("claude", "project", project, home=tmp_path / "home")
    assert (project / ".claude" / "skills" / "paper-alchemist" / "SKILL.md").is_file()
    assert (project / ".claude" / "commands" / "abstract.md").is_file()
    assert any(path.endswith("section.md") for path in result.installed)


def test_pi_prompt_uses_native_all_arguments_placeholder(tmp_path):
    project = tmp_path / "project"
    install("pi", "project", project, home=tmp_path / "home")
    prompt = (project / ".pi" / "prompts" / "abstract.md").read_text(encoding="utf-8")
    assert "$ARGUMENTS" in prompt
    assert "{{args}}" not in prompt


def test_kimi_wrapper_uses_native_skill_arguments(tmp_path):
    project = tmp_path / "project"
    install("kimi", "project", project, home=tmp_path / "home")
    wrapper = (project / ".kimi-code" / "skills" / "abstract" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "type: prompt" in wrapper
    assert "$ARGUMENTS" in wrapper


def test_existing_install_requires_force(tmp_path):
    project = tmp_path / "project"
    install("codex", "project", project, home=tmp_path / "home")
    with pytest.raises(FileExistsError):
        install("codex", "project", project, home=tmp_path / "home")
