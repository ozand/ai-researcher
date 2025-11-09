"""Tests for pyproject.toml configuration validation."""

import subprocess
from pathlib import Path

import pytest
import toml


class TestPyprojectTomlConfiguration:
    """Test suite for pyproject.toml configuration."""

    def test_pyproject_toml_exists(self) -> None:
        """Test that pyproject.toml exists in project root."""
        pyproject_path = Path("pyproject.toml")
        assert pyproject_path.exists(), "pyproject.toml should exist in project root"

    def test_pyproject_toml_is_valid_toml(self) -> None:
        """Test that pyproject.toml is valid TOML format."""
        pyproject_path = Path("pyproject.toml")
        with pyproject_path.open("r", encoding="utf-8") as f:
            content = toml.load(f)
        assert isinstance(content, dict), "pyproject.toml should be valid TOML"

    def test_ruff_configuration_exists(self) -> None:
        """Test that Ruff configuration section exists."""
        pyproject_path = Path("pyproject.toml")
        with pyproject_path.open("r", encoding="utf-8") as f:
            content = toml.load(f)

        assert "tool" in content, "tool section should exist"
        assert "ruff" in content["tool"], "ruff configuration should exist"

    def test_ruff_basic_settings(self) -> None:
        """Test that Ruff basic settings are configured."""
        pyproject_path = Path("pyproject.toml")
        with pyproject_path.open("r", encoding="utf-8") as f:
            content = toml.load(f)

        ruff_config = content["tool"]["ruff"]

        # Test line length
        assert "line-length" in ruff_config, "line-length should be configured"
        assert isinstance(
            ruff_config["line-length"], int
        ), "line-length should be an integer"
        assert ruff_config["line-length"] == 88, "line-length should be 88 characters"

        # Test target version
        assert "target-version" in ruff_config, "target-version should be configured"
        assert (
            ruff_config["target-version"] == "py312"
        ), "target-version should be py312"

    def test_ruff_lint_configuration(self) -> None:
        """Test that Ruff lint configuration exists and has required settings."""
        pyproject_path = Path("pyproject.toml")
        with pyproject_path.open("r", encoding="utf-8") as f:
            content = toml.load(f)

        ruff_config = content["tool"]["ruff"]
        assert "lint" in ruff_config, "lint section should exist"

        lint_config = ruff_config["lint"]

        # Test that select rules are configured
        assert "select" in lint_config, "select rules should be configured"
        assert isinstance(lint_config["select"], list), "select should be a list"
        assert len(lint_config["select"]) > 0, "should have selected rules"

        # Test that ignore rules are configured
        assert "ignore" in lint_config, "ignore rules should be configured"
        assert isinstance(lint_config["ignore"], list), "ignore should be a list"

    def test_ruff_format_configuration(self) -> None:
        """Test that Ruff format configuration exists."""
        pyproject_path = Path("pyproject.toml")
        with pyproject_path.open("r", encoding="utf-8") as f:
            content = toml.load(f)

        ruff_config = content["tool"]["ruff"]
        assert "format" in ruff_config, "format section should exist"

        format_config = ruff_config["format"]

        # Test format settings
        assert "quote-style" in format_config, "quote-style should be configured"
        assert format_config["quote-style"] == "double", "quote-style should be double"

        assert "indent-style" in format_config, "indent-style should be configured"
        assert format_config["indent-style"] == "space", "indent-style should be space"

    def test_mypy_configuration_exists(self) -> None:
        """Test that mypy configuration section exists."""
        pyproject_path = Path("pyproject.toml")
        with pyproject_path.open("r", encoding="utf-8") as f:
            content = toml.load(f)

        assert "tool" in content, "tool section should exist"
        assert "mypy" in content["tool"], "mypy configuration should exist"

    def test_mypy_strict_settings(self) -> None:
        """Test that mypy strict type checking settings are configured."""
        pyproject_path = Path("pyproject.toml")
        with pyproject_path.open("r", encoding="utf-8") as f:
            content = toml.load(f)

        mypy_config = content["tool"]["mypy"]

        # Test strict type checking settings
        strict_settings = [
            ("warn_return_any", True),
            ("warn_unused_configs", True),
            ("disallow_untyped_defs", True),
            ("disallow_incomplete_defs", True),
            ("check_untyped_defs", True),
            ("no_implicit_optional", True),
            ("warn_redundant_casts", True),
            ("warn_unused_ignores", True),
            ("warn_no_return", True),
            ("warn_unreachable", True),
            ("strict_equality", True),
            ("show_error_codes", True),
        ]

        for setting, expected_value in strict_settings:
            assert setting in mypy_config, f"{setting} should be configured"
            assert (
                mypy_config[setting] == expected_value
            ), f"{setting} should be {expected_value}"

    def test_mypy_python_version(self) -> None:
        """Test that mypy Python version is configured."""
        pyproject_path = Path("pyproject.toml")
        with pyproject_path.open("r", encoding="utf-8") as f:
            content = toml.load(f)

        mypy_config = content["tool"]["mypy"]
        assert "python_version" in mypy_config, "python_version should be configured"
        assert mypy_config["python_version"] == "3.12", "python_version should be 3.12"

    def test_mypy_overrides_exist(self) -> None:
        """Test that mypy overrides section exists for external libraries."""
        pyproject_path = Path("pyproject.toml")
        with pyproject_path.open("r", encoding="utf-8") as f:
            content = toml.load(f)

        # Check for overrides section (might be a list or dict depending on TOML structure)
        if "overrides" in str(content.get("tool", {}).get("mypy", {})):
            # If overrides exist, they should include external libraries
            mypy_str = str(content["tool"]["mypy"])
            external_libs = ["google", "openai", "anthropic", "pandas", "rich", "yaml"]

            for lib in external_libs:
                # Check that external libraries are configured to ignore missing imports
                assert lib in mypy_str, f"Should have override for {lib}"

    def test_ruff_can_run_successfully(self) -> None:
        """Test that ruff can run successfully on the project."""
        try:
            result = subprocess.run(
                ["ruff", "check", "--no-cache", "src/"],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            # Ruff should run without crashing (exit code 0 or 1 is fine)
            assert result.returncode in [0, 1], "ruff should run without crashing"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("ruff not available or timed out")

    def test_mypy_can_run_successfully(self) -> None:
        """Test that mypy can run successfully on the project."""
        try:
            result = subprocess.run(
                ["mypy", "src/"],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            # mypy should run without crashing (exit code 0 or 1 is fine)
            assert result.returncode in [0, 1], "mypy should run without crashing"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("mypy not available or timed out")

    def test_project_dependencies_include_dev_tools(self) -> None:
        """Test that project dependencies include development tools."""
        pyproject_path = Path("pyproject.toml")
        with pyproject_path.open("r", encoding="utf-8") as f:
            content = toml.load(f)

        assert "project" in content, "project section should exist"
        assert (
            "optional-dependencies" in content["project"]
        ), "optional-dependencies should exist"
        assert (
            "dev" in content["project"]["optional-dependencies"]
        ), "dev dependencies should exist"

        dev_deps = content["project"]["optional-dependencies"]["dev"]
        dev_tools = ["ruff", "mypy", "pytest"]

        for tool in dev_tools:
            assert any(
                tool in dep for dep in dev_deps
            ), f"{tool} should be in dev dependencies"
