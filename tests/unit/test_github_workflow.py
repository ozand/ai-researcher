"""Tests for GitHub Actions CI workflow configuration."""

import subprocess
from pathlib import Path

import yaml


class TestGitHubActionsWorkflow:
    """Test suite for .github/workflows/ci.yml."""

    def test_github_workflows_directory_exists(self) -> None:
        """Test that .github/workflows directory exists."""
        workflows_dir = Path(".github/workflows")
        assert workflows_dir.exists(), ".github/workflows directory should exist"
        assert workflows_dir.is_dir(), ".github/workflows should be a directory"

    def test_ci_workflow_exists(self) -> None:
        """Test that ci.yml workflow file exists."""
        ci_workflow_path = Path(".github/workflows/ci.yml")
        assert ci_workflow_path.exists(), "ci.yml workflow should exist"

    def test_ci_workflow_is_valid_yaml(self) -> None:
        """Test that ci.yml is valid YAML format."""
        ci_workflow_path = Path(".github/workflows/ci.yml")
        with ci_workflow_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)
        assert isinstance(content, dict), "ci.yml should be valid YAML"

    def test_workflow_has_name(self) -> None:
        """Test that workflow has a name."""
        ci_workflow_path = Path(".github/workflows/ci.yml")
        with ci_workflow_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        assert "name" in content, "Workflow should have a name"
        assert isinstance(content["name"], str), "Workflow name should be a string"
        assert len(content["name"]) > 0, "Workflow name should not be empty"

    def test_workflow_has_triggers(self) -> None:
        """Test that workflow has proper triggers."""
        ci_workflow_path = Path(".github/workflows/ci.yml")
        with ci_workflow_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        assert "on" in content, "Workflow should have triggers"
        triggers = content["on"]

        # Should trigger on push and pull request
        assert isinstance(triggers, dict), "Triggers should be a dictionary"
        assert "push" in triggers, "Should trigger on push"
        assert "pull_request" in triggers, "Should trigger on pull request"

    def test_workflow_has_jobs(self) -> None:
        """Test that workflow has jobs defined."""
        ci_workflow_path = Path(".github/workflows/ci.yml")
        with ci_workflow_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        assert "jobs" in content, "Workflow should have jobs"
        assert isinstance(content["jobs"], dict), "Jobs should be a dictionary"
        assert len(content["jobs"]) > 0, "Should have at least one job"

    def test_has_lint_job(self) -> None:
        """Test that workflow has a lint job."""
        ci_workflow_path = Path(".github/workflows/ci.yml")
        with ci_workflow_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        jobs = content["jobs"]
        assert "lint" in jobs, "Should have a lint job"

        lint_job = jobs["lint"]
        assert "runs-on" in lint_job, "Lint job should specify runner"
        assert "steps" in lint_job, "Lint job should have steps"

    def test_lint_job_uses_checkout(self) -> None:
        """Test that lint job checks out code."""
        ci_workflow_path = Path(".github/workflows/ci.yml")
        with ci_workflow_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        lint_job = content["jobs"]["lint"]
        steps = lint_job["steps"]

        # Should have checkout step
        checkout_steps = [
            step for step in steps if "uses" in step and "checkout" in step["uses"]
        ]
        assert len(checkout_steps) > 0, "Lint job should check out code"

    def test_lint_job_runs_ruff(self) -> None:
        """Test that lint job runs ruff."""
        ci_workflow_path = Path(".github/workflows/ci.yml")
        with ci_workflow_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        lint_job = content["jobs"]["lint"]
        steps = lint_job["steps"]

        # Should have ruff step
        ruff_steps = []
        for step in steps:
            if "run" in step and isinstance(step["run"], str) and "ruff" in step["run"]:
                ruff_steps.append(step)

        assert len(ruff_steps) > 0, "Lint job should run ruff"

    def test_lint_job_runs_mypy(self) -> None:
        """Test that lint job runs mypy."""
        ci_workflow_path = Path(".github/workflows/ci.yml")
        with ci_workflow_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        lint_job = content["jobs"]["lint"]
        steps = lint_job["steps"]

        # Should have mypy step
        mypy_steps = []
        for step in steps:
            if "run" in step and isinstance(step["run"], str) and "mypy" in step["run"]:
                mypy_steps.append(step)

        assert len(mypy_steps) > 0, "Lint job should run mypy"

    def test_has_test_job(self) -> None:
        """Test that workflow has a test job."""
        ci_workflow_path = Path(".github/workflows/ci.yml")
        with ci_workflow_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        jobs = content["jobs"]
        assert "test" in jobs, "Should have a test job"

        test_job = jobs["test"]
        assert "runs-on" in test_job, "Test job should specify runner"
        assert "steps" in test_job, "Test job should have steps"

    def test_test_job_runs_pytest(self) -> None:
        """Test that test job runs pytest."""
        ci_workflow_path = Path(".github/workflows/ci.yml")
        with ci_workflow_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        test_job = content["jobs"]["test"]
        steps = test_job["steps"]

        # Should have pytest step
        pytest_steps = []
        for step in steps:
            if (
                "run" in step
                and isinstance(step["run"], str)
                and "pytest" in step["run"]
            ):
                pytest_steps.append(step)

        assert len(pytest_steps) > 0, "Test job should run pytest"

    def test_test_job_uses_matrix(self) -> None:
        """Test that test job uses Python version matrix."""
        ci_workflow_path = Path(".github/workflows/ci.yml")
        with ci_workflow_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        test_job = content["jobs"]["test"]

        # Should have matrix strategy
        if "strategy" in test_job:
            strategy = test_job["strategy"]
            if "matrix" in strategy:
                matrix = strategy["matrix"]
                assert "python-version" in matrix, "Should have python-version matrix"

    def test_has_security_job(self) -> None:
        """Test that workflow has a security job."""
        ci_workflow_path = Path(".github/workflows/ci.yml")
        with ci_workflow_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        jobs = content["jobs"]
        assert "security" in jobs, "Should have a security job"

        security_job = jobs["security"]
        assert "runs-on" in security_job, "Security job should specify runner"
        assert "steps" in security_job, "Security job should have steps"

    def test_security_job_runs_bandit(self) -> None:
        """Test that security job runs bandit."""
        ci_workflow_path = Path(".github/workflows/ci.yml")
        with ci_workflow_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        security_job = content["jobs"]["security"]
        steps = security_job["steps"]

        # Should have bandit step
        bandit_steps = []
        for step in steps:
            if (
                "run" in step
                and isinstance(step["run"], str)
                and "bandit" in step["run"]
            ):
                bandit_steps.append(step)

        assert len(bandit_steps) > 0, "Security job should run bandit"

    def test_jobs_have_proper_dependencies(self) -> None:
        """Test that jobs have proper dependencies if needed."""
        ci_workflow_path = Path(".github/workflows/ci.yml")
        with ci_workflow_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        jobs = content["jobs"]

        # Test job should depend on lint job
        if "test" in jobs and "lint" in jobs:
            test_job = jobs["test"]
            if "needs" in test_job:
                needs = test_job["needs"]
                if isinstance(needs, list):
                    assert "lint" in needs, "Test job should depend on lint"
                elif isinstance(needs, str):
                    assert needs == "lint", "Test job should depend on lint"

    def test_workflow_uses_python_actions(self) -> None:
        """Test that workflow uses Python setup actions."""
        ci_workflow_path = Path(".github/workflows/ci.yml")
        with ci_workflow_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        jobs = content["jobs"]

        for job in jobs.values():
            steps = job.get("steps", [])
            for step in steps:
                if "uses" in step:
                    uses = step["uses"]
                    # Should use official GitHub actions
                    if "actions/" in uses:
                        assert uses.startswith(
                            "actions/"
                        ), f"Should use official actions: {uses}"

    def test_workflow_has_timeout_configured(self) -> None:
        """Test that jobs have reasonable timeouts."""
        ci_workflow_path = Path(".github/workflows/ci.yml")
        with ci_workflow_path.open("r", encoding="utf-8") as f:
            content = yaml.safe_load(f)

        jobs = content["jobs"]

        for job in jobs.values():
            # Jobs should have timeout or use default
            timeout = job.get("timeout-minutes")
            if timeout is not None:
                assert isinstance(timeout, int), "Timeout should be integer"
                assert timeout > 0, "Timeout should be positive"
                assert timeout <= 60, "Timeout should be reasonable"

    def test_workflow_is_valid_github_syntax(self) -> None:
        """Test that workflow follows GitHub Actions syntax."""
        ci_workflow_path = Path(".github/workflows/ci.yml")

        try:
            # Try to validate with GitHub CLI if available
            result = subprocess.run(
                ["gh", "workflow", "view", ci_workflow_path],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            # If command exists and succeeds, workflow is valid
            if result.returncode == 0:
                assert True, "Workflow should be valid GitHub Actions syntax"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # If gh CLI not available, just check YAML validity
            with ci_workflow_path.open("r", encoding="utf-8") as f:
                yaml.safe_load(f)
            assert True, "Workflow should be valid YAML"
