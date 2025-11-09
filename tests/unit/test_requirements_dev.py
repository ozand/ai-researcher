"""Tests for requirements-dev.txt configuration."""

from pathlib import Path


class TestRequirementsDev:
    """Test suite for requirements-dev.txt."""

    def test_requirements_dev_exists(self) -> None:
        """Test that requirements-dev.txt exists in project root."""
        requirements_path = Path("requirements-dev.txt")
        assert (
            requirements_path.exists()
        ), "requirements-dev.txt should exist in project root"

    def test_requirements_dev_is_readable(self) -> None:
        """Test that requirements-dev.txt is readable."""
        requirements_path = Path("requirements-dev.txt")
        with requirements_path.open("r", encoding="utf-8") as f:
            content = f.read()
        assert isinstance(
            content, str
        ), "requirements-dev.txt should be readable as text"

    def test_requirements_dev_contains_dev_tools(self) -> None:
        """Test that requirements-dev.txt contains essential development tools."""
        requirements_path = Path("requirements-dev.txt")
        with requirements_path.open("r", encoding="utf-8") as f:
            content = f.read()

        # Check for essential development tools
        required_tools = ["pytest", "ruff", "mypy", "pre-commit"]

        for tool in required_tools:
            assert (
                tool in content.lower()
            ), f"requirements-dev.txt should contain {tool}"

    def test_requirements_dev_contains_type_stubs(self) -> None:
        """Test that requirements-dev.txt contains type stubs."""
        requirements_path = Path("requirements-dev.txt")
        with requirements_path.open("r", encoding="utf-8") as f:
            content = f.read()

        # Check for type stubs
        type_stubs = ["types-requests", "types-toml", "types-pyyaml"]

        for stub in type_stubs:
            assert (
                stub in content.lower()
            ), f"requirements-dev.txt should contain {stub}"

    def test_requirements_dev_contains_coverage_tools(self) -> None:
        """Test that requirements-dev.txt contains coverage tools."""
        requirements_path = Path("requirements-dev.txt")
        with requirements_path.open("r", encoding="utf-8") as f:
            content = f.read()

        # Check for coverage tools
        coverage_tools = ["pytest-cov"]

        for tool in coverage_tools:
            assert (
                tool in content.lower()
            ), f"requirements-dev.txt should contain {tool}"

    def test_requirements_dev_has_proper_format(self) -> None:
        """Test that requirements-dev.txt follows proper format."""
        requirements_path = Path("requirements-dev.txt")
        with requirements_path.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        # Each line should be non-empty or a comment
        for i, line in enumerate(lines, 1):
            stripped_line = line.strip()
            if stripped_line:  # Non-empty line
                if stripped_line.startswith("#"):
                    # Comment lines are fine
                    continue
                # Should look like a package specification
                assert any(
                    char in stripped_line for char in ["<", ">", "=", "==", "~="]
                ), f"Line {i} should have version specifier: {stripped_line}"

    def test_requirements_dev_no_duplicates(self) -> None:
        """Test that requirements-dev.txt has no duplicate packages."""
        requirements_path = Path("requirements-dev.txt")
        with requirements_path.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        # Extract package names (before any version specifiers)
        packages = []
        for line in lines:
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith("#"):
                # Extract package name before version specifiers
                package_name = (
                    stripped_line.split(">=")[0]
                    .split("==")[0]
                    .split("<")[0]
                    .split(">")[0]
                    .split("~=")[0]
                    .strip()
                )
                packages.append(package_name.lower())

        # Check for duplicates
        assert len(packages) == len(
            set(packages)
        ), f"requirements-dev.txt should not have duplicate packages: {packages}"

    def test_requirements_dev_matches_pyproject_dev_deps(self) -> None:
        """Test that requirements-dev.txt matches pyproject.toml dev dependencies."""
        requirements_path = Path("requirements-dev.txt")
        pyproject_path = Path("pyproject.toml")

        # Read requirements-dev.txt
        with requirements_path.open("r", encoding="utf-8") as f:
            req_content = f.read()

        # Read pyproject.toml dev dependencies
        import toml

        with pyproject_path.open("r", encoding="utf-8") as f:
            pyproject_content = toml.load(f)

        dev_deps = (
            pyproject_content.get("project", {})
            .get("optional-dependencies", {})
            .get("dev", [])
        )

        # Check that all dev dependencies are represented in requirements-dev.txt
        for dep in dev_deps:
            # Extract package name from dependency specification
            dep_name = (
                dep.split(">=")[0]
                .split("==")[0]
                .split("<")[0]
                .split(">")[0]
                .split("~=")[0]
                .strip()
            )
            assert (
                dep_name.lower() in req_content.lower()
            ), f"requirements-dev.txt should contain {dep_name} from pyproject.toml"

    def test_requirements_dev_is_sorted_alphabetically(self) -> None:
        """Test that requirements-dev.txt is sorted alphabetically."""
        requirements_path = Path("requirements-dev.txt")
        with requirements_path.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        # Extract package names in order
        packages = []
        for line in lines:
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith("#"):
                package_name = (
                    stripped_line.split(">=")[0]
                    .split("==")[0]
                    .split("<")[0]
                    .split(">")[0]
                    .split("~=")[0]
                    .strip()
                )
                packages.append(package_name.lower())

        # Check if sorted
        sorted_packages = sorted(packages)
        assert (
            packages == sorted_packages
        ), f"requirements-dev.txt should be sorted alphabetically. Got: {packages}, Expected: {sorted_packages}"

    def test_requirements_dev_has_header_comment(self) -> None:
        """Test that requirements-dev.txt has a descriptive header comment."""
        requirements_path = Path("requirements-dev.txt")
        with requirements_path.open("r", encoding="utf-8") as f:
            first_line = f.readline().strip()

        assert first_line.startswith(
            "#"
        ), "requirements-dev.txt should start with a comment header"
        assert any(
            keyword in first_line.lower()
            for keyword in ["development", "dev", "dependencies"]
        ), "Header should mention development dependencies"
