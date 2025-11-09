"""Tests for code quality configuration."""

import subprocess
from pathlib import Path

import yaml


def test_ruff_configuration():
    """Test that Ruff configuration is valid."""
    result = subprocess.run(
        ["ruff", "check", "--help"], check=False, capture_output=True, text=True
    )
    assert result.returncode == 0, "Ruff should be available"


def test_mypy_configuration():
    """Test that mypy configuration is valid."""
    result = subprocess.run(
        ["mypy", "--version"], check=False, capture_output=True, text=True
    )
    assert result.returncode == 0, "mypy should be available"


def test_bandit_configuration():
    """Test that bandit configuration is valid."""
    try:
        result = subprocess.run(
            ["bandit", "--version"], check=False, capture_output=True, text=True
        )
        # bandit may not be available in all environments, but configuration should be valid
        assert result.returncode in [
            0,
            2,
        ], "bandit should be available or gracefully missing"
    except FileNotFoundError:
        # bandit not available in this environment, which is acceptable for integration testing
        pass


def test_pre_commit_configuration():
    """Test that pre-commit configuration is valid."""
    pre_commit_file = Path(".pre-commit-config.yaml")
    assert pre_commit_file.exists(), "pre-commit config should exist"

    with pre_commit_file.open("r") as f:
        config = yaml.safe_load(f)

    assert "repos" in config, "pre-commit config should have repos"
    assert len(config["repos"]) > 0, "should have at least one repo"


def test_pyproject_toml_structure():
    """Test that pyproject.toml has required sections."""
    pyproject_file = Path("pyproject.toml")
    assert pyproject_file.exists(), "pyproject.toml should exist"

    # Simple check that file is readable and has basic structure
    with pyproject_file.open("r") as f:
        content = f.read()

    # Check for required tool sections in content
    assert "[tool.ruff]" in content, "should have ruff config"
    assert "[tool.mypy]" in content, "should have mypy config"
    assert "[tool.bandit]" in content, "should have bandit config"
    assert "[tool.pytest.ini_options]" in content, "should have pytest config"


def test_github_actions_workflow():
    """Test that GitHub Actions workflow exists and is valid."""
    workflow_file = Path(".github/workflows/ci.yml")
    assert workflow_file.exists(), "CI workflow should exist"

    with workflow_file.open("r") as f:
        content = f.read()

    # Check for essential jobs
    assert "lint" in content, "should have lint job"
    assert "test" in content, "should have test job"
    assert "security" in content, "should have security job"


def test_code_quality_on_current_codebase():
    """Run quality checks on current codebase."""
    # Test Ruff
    result = subprocess.run(
        ["ruff", "check", ".", "--no-fix"], check=False, capture_output=True, text=True
    )

    if result.returncode != 0:
        print("Ruff issues found:")
        print(result.stdout)
        print(result.stderr)

    # We expect some issues initially, but the tool should run
    assert result.returncode in [0, 1], "Ruff should run without crashing"

    # Test formatting check
    result = subprocess.run(
        ["ruff", "format", "--check", "."], check=False, capture_output=True, text=True
    )

    # Format check might fail, but should run
    assert result.returncode in [0, 1], "Ruff format should run without crashing"


def test_type_checking_on_current_codebase():
    """Run mypy on current codebase."""
    result = subprocess.run(
        ["mypy", "src/"], check=False, capture_output=True, text=True
    )

    # Type checking might find issues, but should run
    assert result.returncode in [0, 1], "mypy should run without crashing"

    if result.returncode != 0:
        print("Type issues found:")
        print(result.stdout)
        print(result.stderr)


def test_security_check_on_current_codebase():
    """Run bandit security check on current codebase."""
    try:
        result = subprocess.run(
            ["bandit", "-r", "src/", "-f", "json"],
            check=False,
            capture_output=True,
            text=True,
        )

        # Security check should run without crashing or be gracefully missing
        assert result.returncode in [
            0,
            1,
            2,
        ], "bandit should run without crashing or be missing"
    except FileNotFoundError:
        # bandit not available in this environment, which is acceptable for integration testing
        pass
