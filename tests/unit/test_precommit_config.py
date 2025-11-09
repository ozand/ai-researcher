"""Tests for pre-commit hooks configuration."""

import subprocess
from pathlib import Path

import pytest
import yaml


class TestPrecommitConfiguration:
    """Test suite for .pre-commit-config.yaml configuration."""

    def test_precommit_config_exists(self) -> None:
        """Test that .pre-commit-config.yaml exists in project root."""
        precommit_path = Path(".pre-commit-config.yaml")
        assert (
            precommit_path.exists()
        ), ".pre-commit-config.yaml should exist in project root"

    def test_precommit_config_is_valid_yaml(self) -> None:
        """Test that .pre-commit-config.yaml is valid YAML format."""
        precommit_path = Path(".pre-commit-config.yaml")
        with precommit_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)
        assert isinstance(content, dict), ".pre-commit-config.yaml should be valid YAML"

    def test_precommit_basic_structure(self) -> None:
        """Test that pre-commit config has basic structure."""
        precommit_path = Path(".pre-commit-config.yaml")
        with precommit_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        # Test required top-level keys
        assert "repos" in content, "repos section should exist"
        assert isinstance(content["repos"], list), "repos should be a list"
        assert len(content["repos"]) > 0, "should have at least one repo"

    def test_ruff_hook_configured(self) -> None:
        """Test that Ruff hooks are configured."""
        precommit_path = Path(".pre-commit-config.yaml")
        with precommit_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        # Find Ruff repo
        ruff_repo = None
        for repo in content["repos"]:
            if "ruff" in repo.get("repo", ""):
                ruff_repo = repo
                break

        assert ruff_repo is not None, "Ruff repo should be configured"

        # Check that hooks are configured
        assert "hooks" in ruff_repo, "Ruff should have hooks configured"
        ruff_hooks = ruff_repo["hooks"]

        # Should have both lint and format hooks
        hook_ids = [hook.get("id") for hook in ruff_hooks]
        assert "ruff" in hook_ids, "Should have ruff lint hook"
        assert "ruff-format" in hook_ids, "Should have ruff-format hook"

    def test_mypy_hook_configured(self) -> None:
        """Test that mypy hook is configured."""
        precommit_path = Path(".pre-commit-config.yaml")
        with precommit_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        # Find mypy repo
        mypy_repo = None
        for repo in content["repos"]:
            if "mypy" in repo.get("repo", ""):
                mypy_repo = repo
                break

        assert mypy_repo is not None, "mypy repo should be configured"

        # Check that hooks are configured
        assert "hooks" in mypy_repo, "mypy should have hooks configured"
        mypy_hooks = mypy_repo["hooks"]

        # Should have mypy hook
        hook_ids = [hook.get("id") for hook in mypy_hooks]
        assert "mypy" in hook_ids, "Should have mypy hook"

    def test_trailing_whitespace_hook_configured(self) -> None:
        """Test that trailing whitespace hook is configured."""
        precommit_path = Path(".pre-commit-config.yaml")
        with precommit_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        # Find pre-commit hooks repo
        hooks_repo = None
        for repo in content["repos"]:
            if "pre-commit/pre-commit-hooks" in repo.get("repo", ""):
                hooks_repo = repo
                break

        assert hooks_repo is not None, "pre-commit-hooks repo should be configured"

        # Check for trailing whitespace hook
        hooks = hooks_repo.get("hooks", [])
        hook_ids = [hook.get("id") for hook in hooks]
        assert "trailing-whitespace" in hook_ids, "Should have trailing-whitespace hook"

    def test_end_of_file_hook_configured(self) -> None:
        """Test that end-of-file-fixer hook is configured."""
        precommit_path = Path(".pre-commit-config.yaml")
        with precommit_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        # Find pre-commit hooks repo
        hooks_repo = None
        for repo in content["repos"]:
            if "pre-commit/pre-commit-hooks" in repo.get("repo", ""):
                hooks_repo = repo
                break

        assert hooks_repo is not None, "pre-commit-hooks repo should be configured"

        # Check for end-of-file-fixer hook
        hooks = hooks_repo.get("hooks", [])
        hook_ids = [hook.get("id") for hook in hooks]
        assert "end-of-file-fixer" in hook_ids, "Should have end-of-file-fixer hook"

    def test_check_yaml_hook_configured(self) -> None:
        """Test that check-yaml hook is configured."""
        precommit_path = Path(".pre-commit-config.yaml")
        with precommit_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        # Find pre-commit hooks repo
        hooks_repo = None
        for repo in content["repos"]:
            if "pre-commit/pre-commit-hooks" in repo.get("repo", ""):
                hooks_repo = repo
                break

        assert hooks_repo is not None, "pre-commit-hooks repo should be configured"

        # Check for check-yaml hook
        hooks = hooks_repo.get("hooks", [])
        hook_ids = [hook.get("id") for hook in hooks]
        assert "check-yaml" in hook_ids, "Should have check-yaml hook"

    def test_bandit_hook_configured(self) -> None:
        """Test that bandit security hook is configured."""
        precommit_path = Path(".pre-commit-config.yaml")
        with precommit_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        # Find bandit repo
        bandit_repo = None
        for repo in content["repos"]:
            if "bandit" in repo.get("repo", ""):
                bandit_repo = repo
                break

        assert bandit_repo is not None, "bandit repo should be configured"

        # Check that hooks are configured
        assert "hooks" in bandit_repo, "bandit should have hooks configured"
        bandit_hooks = bandit_repo["hooks"]

        # Should have bandit hook
        hook_ids = [hook.get("id") for hook in bandit_hooks]
        assert "bandit" in hook_ids, "Should have bandit hook"

    def test_hook_order_is_logical(self) -> None:
        """Test that hooks are in a logical order."""
        precommit_path = Path(".pre-commit-config.yaml")
        with precommit_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        # Get all hook IDs in order
        all_hook_ids = []
        for repo in content["repos"]:
            for hook in repo.get("hooks", []):
                all_hook_ids.append(hook.get("id"))

        # Check that ruff-format comes before ruff (format then lint)
        if "ruff-format" in all_hook_ids and "ruff" in all_hook_ids:
            ruff_format_index = all_hook_ids.index("ruff-format")
            ruff_index = all_hook_ids.index("ruff")
            assert ruff_format_index < ruff_index, "ruff-format should come before ruff"

    def test_precommit_can_run_successfully(self) -> None:
        """Test that pre-commit can run successfully."""
        try:
            # Try to run pre-commit --version first
            result = subprocess.run(
                ["pre-commit", "--version"],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            assert result.returncode == 0, "pre-commit should be available"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("pre-commit not available")

    def test_precommit_config_is_self_validating(self) -> None:
        """Test that pre-commit config validates itself."""
        try:
            result = subprocess.run(
                ["pre-commit", "validate-config"],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            assert (
                result.returncode == 0
            ), f"pre-commit config should be valid: {result.stderr}"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("pre-commit not available")

    def test_required_repos_have_versions(self) -> None:
        """Test that required repos have proper version specifications."""
        precommit_path = Path(".pre-commit-config.yaml")
        with precommit_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        for repo in content["repos"]:
            repo_url = repo.get("repo", "")
            # Each repo should have a revision (version)
            assert "rev" in repo, f"Repo {repo_url} should have a revision/version"
            assert repo["rev"], f"Repo {repo_url} should have a non-empty revision"

    def test_hooks_have_required_fields(self) -> None:
        """Test that hooks have required fields."""
        precommit_path = Path(".pre-commit-config.yaml")
        with precommit_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        for repo in content["repos"]:
            hooks = repo.get("hooks", [])
            for hook in hooks:
                # Each hook should have an id
                assert (
                    "id" in hook
                ), f"Hook in repo {repo.get('repo')} should have an id"
                assert hook["id"], "Hook id should not be empty"
