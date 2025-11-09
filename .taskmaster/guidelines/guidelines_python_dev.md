# Оптимизированная структура документации с YAML метаданными

## Структура файлов

```
guidelines/
├── index.md                       # Навигационный индекс
├── 00-core-principles.md
├── 01-project-structure.md
├── 02-code-quality.md
├── 03-testing-strategy.md
└── roocode/
    ├── tool-usage-protocol.md
    └── agent-capabilities.md
```

---

## index.md

```yaml
---
title: "Python Project Guidelines Index"
version: "2.0.0"
last_updated: "2025-10-19"
purpose: "Navigation hub for AI agents"
priority: critical
agent_usage: "Read this first to understand guideline structure"
---
```

```markdown
# Python Project Guidelines - Navigation Index

## 📋 Quick Reference for AI Agents

### Document Priority Levels
- **🔴 Critical** - Must read for every task
- **🟡 Contextual** - Read when relevant to task type
- **🔵 Reference** - Consult when needed

---

## Universal Guidelines (Apply to all Python projects)

| Document | Priority | When to Use | Key Topics |
|----------|----------|-------------|------------|
| [00-core-principles.md](#00) | 🔴 Critical | Always | DRY, SOLID, architecture patterns |
| [01-project-structure.md](#01) | 🔴 Critical | Project setup, file organization | Directory layout, src/tests separation |
| [02-code-quality.md](#02) | 🟡 Contextual | Code changes, refactoring | Ruff, mypy, pre-commit hooks |
| [03-testing-strategy.md](#03) | 🟡 Contextual | Writing/running tests | Unit, integration, E2E testing |

## RooCode-Specific Guidelines

| Document | Priority | When to Use | Key Topics |
|----------|----------|-------------|------------|
| [roocode/tool-usage-protocol.md](#tool) | 🔴 Critical | Any RooCode operation | Prefer specialized tools over execute_command |
| [roocode/agent-capabilities.md](#agents) | 🔵 Reference | Task delegation | Agent roles and capabilities |

---

## Task-Based Navigation

### "I need to set up a new project"
→ Read: `00-core-principles.md`, `01-project-structure.md`, `02-code-quality.md`

### "I need to write/modify code"
→ Read: `00-core-principles.md`, `02-code-quality.md`
→ **RooCode users:** `roocode/tool-usage-protocol.md`

### "I need to write tests"
→ Read: `03-testing-strategy.md`, `01-project-structure.md` (test directory layout)

### "I need to refactor existing code"
→ Read: `00-core-principles.md`, `02-code-quality.md` (refactoring process)

### "I need to read/write files" (RooCode)
→ Read: `roocode/tool-usage-protocol.md` (Section 2: equivalency table)

### "I need to delegate a task" (RooCode)
→ Read: `roocode/agent-capabilities.md`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-10-19 | Complete restructure, eliminated duplicates |
| 1.0.0 | - | Initial fragmented structure (6 files) |
```

---

## 00-core-principles.md

```yaml
---
title: "Core Software Design Principles"
version: "2.0.0"
category: "architecture"
priority: critical
applies_to: ["all_projects"]
agent_usage: "Read before any design or implementation task"
keywords: ["DRY", "SOLID", "architecture", "design_patterns", "abstractions"]
related_docs: ["01-project-structure.md", "02-code-quality.md"]
---
```

```markdown
# Core Software Design Principles

> Universal principles for any software project. These are non-negotiable fundamentals.

## Universal Principles

### DRY (Don't Repeat Yourself)
- Eliminate duplicated logic across the codebase
- Extract shared utilities into reusable functions/classes
- Apply to code, tests, documentation, and configuration

### Single Responsibility Principle (SRP)
- One module/class/function = one reason to change
- Each component should do one thing well
- Easier to test, maintain, and understand

### Separation of Concerns
- Each module handles one type of responsibility
- Business logic ≠ data access ≠ presentation ≠ infrastructure
- Example: separate API routes, business logic, and database queries

### YAGNI & KISS
- **YAGNI (You Ain't Gonna Need It):** Build only what's needed now
- **KISS (Keep It Simple, Stupid):** Choose the simplest solution that works
- Avoid premature optimization and over-engineering

---

## Architecture Guidelines

### Dependency Inversion Principle
- High-level modules depend on abstractions, not concrete implementations
- Use interfaces/protocols to define contracts
- Example: depend on `PaymentProcessor` interface, not `StripePayment` class

### Import Strategy
- **Absolute imports only** - forbid relative imports
```python
# ✅ Good
from src.my_project.payments import process_payment

# ❌ Bad
from ..payments import process_payment
```

### Clear Boundaries
- Keep core business logic independent from:
  - I/O operations (file, network, database)
  - UI/presentation layer
  - Framework-specific code
  - External services
- This enables easier testing and framework migration

### Low Coupling, High Cohesion
- **Low coupling:** Minimize dependencies between modules
- **High cohesion:** Keep related functionality together
- Modules should be independently deployable and testable

---

## Code Organization Principles

### Explicit Over Implicit
- Code should be self-documenting
- Clear variable and function names
- Avoid "magic" values and hidden assumptions

### Determinism
- Prefer pure functions for business logic
- Same input → same output (no hidden state)
- Side effects isolated to boundaries (I/O layer)

### Idempotency
- Critical operations should be safely repeatable
- Examples: API calls, database migrations, deployments
- Use unique identifiers to prevent duplicate processing

---

## When to Apply These Principles

| Principle | Apply When | Skip When |
|-----------|-----------|-----------|
| DRY | Logic repeated 2+ times | Single use, prototype code |
| SRP | Module becoming complex | Trivial scripts (<50 lines) |
| Abstraction | Multiple implementations needed | Only one implementation will ever exist |
| Idempotency | Network/IO operations | Pure computation |

---

## Anti-Patterns to Avoid

- ❌ God objects (classes that do everything)
- ❌ Circular dependencies between modules
- ❌ Tight coupling to frameworks
- ❌ Business logic in controllers/views
- ❌ Hidden global state
- ❌ Copy-paste programming
```

---

## 01-project-structure.md

```yaml
---
title: "Project Structure & Organization"
version: "2.0.0"
category: "project_setup"
priority: critical
applies_to: ["all_projects"]
agent_usage: "Reference when setting up projects or organizing code"
keywords: ["directory_structure", "organization", "src", "tests", "scripts"]
related_docs: ["00-core-principles.md", "03-testing-strategy.md"]
---
```

```markdown
# Project Structure & Organization

> Standard layout for Python projects with clear separation of concerns

## Standard Directory Layout

```
project_name/
├── src/
│   └── project_name/           # Production code only
│       ├── __init__.py
│       ├── payments/
│       │   ├── __init__.py
│       │   ├── processor.py
│       │   └── models.py
│       └── search/
│           ├── __init__.py
│           └── engine.py
├── tests/
│   ├── unit/                   # Fast, isolated tests
│   │   ├── payments/
│   │   └── search/
│   ├── integration/            # Component interaction tests
│   └── e2e/                    # End-to-end user journeys
├── scripts/
│   ├── development/            # Engineering automation
│   │   ├── README.md
│   │   ├── utils.py
│   │   ├── migrate_db.py
│   │   └── reorganize_modules.py
│   └── archive/                # Deprecated scripts
├── docs/                       # Project documentation
├── pyproject.toml              # Project metadata & dependencies
├── .gitignore
├── .pre-commit-config.yaml
└── README.md
```

---

## Directory Rules

### src/ - Production Code Only

**Purpose:** Contains only application code that will be deployed to production

**Rules:**
- No temporary scripts, experiments, or one-off utilities
- No migration scripts or data processing scripts
- No test fixtures or test utilities
- Ensures CI/CD builds exclude auxiliary files

**Structure:**
- Mirror business domains/features as subdirectories
- Each subdirectory is a Python package (`__init__.py`)
- Use absolute imports: `from src.project_name.payments import ...`

---

### tests/ - Test Code

**Purpose:** All test code, mirroring src/ structure

**Subdirectories:**

#### tests/unit/
- Fast, isolated component tests
- No external dependencies (DB, network, filesystem)
- Mirror src/ structure exactly
```
src/project_name/payments/processor.py
→ tests/unit/payments/test_processor.py
```

#### tests/integration/
- Test component interactions
- May use database, external APIs, filesystem
- Example: API endpoint tests, database query tests

#### tests/e2e/
- Critical user journey validation
- Uses Playwright for browser automation
- Page Object Model structure
- See Testing Strategy section below for details

---

### scripts/development/ - Engineering Automation

**Purpose:** All non-production scripts (migrations, fixes, bulk operations)

**Rules:**
1. **Name clearly:** `reorganize_modules.py`, `migrate_imports.py`, `seed_test_data.py`
2. **Document in code:**
   - Module-level docstring explaining purpose
   - CLI argument documentation
   - Usage examples
3. **Create README.md** in `scripts/development/` listing all scripts
4. **Use Python modules,** not bash one-liners:
```python
# ✅ Good - scripts/development/migrate_db.py
def main():
    parser = argparse.ArgumentParser()
    # ... proper CLI interface

if __name__ == "__main__":
    main()
```

5. **Extract reusable logic** into `scripts/development/utils.py`
6. **Archive when done:** Move obsolete scripts to `scripts/archive/`

**Never put in scripts/:**
- Production application code
- Reusable business logic
- Tests

---

## Dependency Management

### Using uv (Recommended)

```bash
# Initialize new project
uv init project_name

# Add runtime dependency
uv add requests

# Add development dependency
uv add --dev pytest pytest-cov

# Synchronize environment
uv sync
```

### pyproject.toml Structure

```toml
[project]
name = "project_name"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.31.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

---

## Version Control (.gitignore)

**Always exclude:**

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual environments
.venv/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp

# Testing
.pytest_cache/
.coverage
htmlcov/

# Build artifacts
dist/
build/
*.egg-info/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
```

---

## Initialization Checklist

When starting a new project:

- [ ] Run `uv init project_name`
- [ ] Create src/project_name/ structure
- [ ] Create tests/ with unit/integration/e2e subdirs
- [ ] Create scripts/development/ with README.md
- [ ] Add .gitignore
- [ ] Configure Ruff and pre-commit (see 02-code-quality.md)
- [ ] Write initial README.md
- [ ] Initialize git repository
```

---

## 02-code-quality.md

```yaml
---
title: "Code Quality & Automation"
version: "2.0.0"
category: "quality_assurance"
priority: contextual
applies_to: ["all_projects"]
agent_usage: "Reference when writing code, setting up CI, or refactoring"
keywords: ["ruff", "mypy", "pre-commit", "linting", "formatting", "maintenance"]
related_docs: ["00-core-principles.md", "01-project-structure.md"]
---
```

```markdown
# Code Quality & Automation

> Automated tools and processes to maintain code quality

## Linting & Formatting with Ruff

### Configuration (pyproject.toml)

```toml
[tool.ruff]
line-length = 88                    # Standard Python convention (Black compatible)
target-version = "py311"

# Rule selection
select = [
    "F",      # Pyflakes
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "I",      # isort (import sorting)
    "UP",     # pyupgrade (modern Python idioms)
    "B",      # flake8-bugbear
    "BLE",    # flake8-blind-except
]

ignore = [
    "E501",   # Line too long (handled by formatter)
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.ruff.lint.isort]
known-first-party = ["src"]
```

### Usage

```bash
# Check and fix issues
ruff check . --fix

# Format code
ruff format .

# Check only (CI mode)
ruff check . --no-fix
```

---

## Type Checking with mypy

### Configuration (pyproject.toml)

```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true

# Per-module options
[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

### Usage

```bash
# Type check entire project
mypy src/

# Type check specific module
mypy src/project_name/payments/
```

---

## Pre-commit Hooks

### Setup

1. **Install pre-commit:**
```bash
uv add --dev pre-commit
```

2. **Create .pre-commit-config.yaml:**

```yaml
repos:
  # Ruff - linting and formatting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  # Type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
        args: [--strict]

  # Standard checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: [--maxkb=500]
      - id: check-merge-conflict

  # Custom project validators (optional)
  - repo: local
    hooks:
      - id: validate-kb
        name: Validate Knowledge Base
        entry: python scripts/development/validate_kb.py
        language: python
        types: [markdown]
        pass_filenames: false
```

3. **Install hooks:**
```bash
pre-commit install
```

4. **Run manually (optional):**
```bash
# Run on all files
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files
```

---

## Maintenance Tasks

### Dead Code Detection & Removal

```bash
# Find unused imports and variables
ruff check . --select F401,F841 --fix

# Find unused functions (manual review needed)
ruff check . --select F401,F821,F841
```

### Dependency Audits

```bash
# Check for outdated packages
uv pip list --outdated

# Security vulnerability check (use pip-audit)
uv add --dev pip-audit
uv run pip-audit
```

### Update All Dependencies

```bash
# Update to latest compatible versions
uv sync --upgrade
```

---

## Refactoring Process

Follow this systematic approach when refactoring:

1. **Isolate change:** Focus on one small improvement
2. **Run tests:** Ensure all tests pass before starting
3. **Make change:** Implement the refactoring
4. **Run tests again:** Verify nothing broke
5. **Commit:** Create atomic commit with clear message
6. **Repeat:** Continue with next small step

### Example Workflow

```bash
# 1. Ensure clean state
uv run pytest

# 2. Make small change (e.g., rename function)
# ... edit code ...

# 3. Auto-fix code quality
ruff check . --fix
ruff format .

# 4. Verify with tests
uv run pytest

# 5. Commit
git add .
git commit -m "refactor: rename process_payment to execute_payment"

# 6. Continue with next change
```

---

## Script Execution Protocol

**MANDATORY:** After running ANY script or command, always:

1. **Capture output:** Both stdout and stderr
2. **Analyze results:**
   - ✅ What succeeded?
   - ❌ What failed?
   - ⚠️  What warnings appeared?
3. **Decide next action:**
   - If errors: investigate and fix
   - If warnings: evaluate severity
   - Use `ask_followup_question` when uncertain
4. **Never ignore warnings** - they often indicate real issues

### Example Analysis

```bash
$ ruff check . --fix

# Output analysis:
# ✅ Fixed 15 issues automatically
# ⚠️  Warning: Unused import in src/payments/processor.py
# ❌ Error: Undefined name 'process_paymen' in src/api/routes.py

# Action: Fix typo in routes.py, remove unused import
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Quality Checks

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v1

      - name: Install dependencies
        run: uv sync

      - name: Lint
        run: uv run ruff check . --no-fix

      - name: Format check
        run: uv run ruff format --check .

      - name: Type check
        run: uv run mypy src/

      - name: Run tests
        run: uv run pytest --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## Quality Metrics

### Minimum Standards

| Metric | Target | Tool |
|--------|--------|------|
| Code coverage | ≥80% | pytest-cov |
| Type coverage | 100% | mypy --strict |
| Linting issues | 0 | ruff |
| Cyclomatic complexity | ≤10 per function | ruff (CCR rules) |

### When to Measure

- **Every commit:** via pre-commit hooks
- **Every PR:** via CI pipeline
- **Weekly:** full project audit
- **Before release:** comprehensive quality review
```

---

## 03-testing-strategy.md

```yaml
---
title: "Testing Strategy"
version: "2.0.0"
category: "quality_assurance"
priority: contextual
applies_to: ["all_projects"]
agent_usage: "Reference when writing tests or setting up test infrastructure"
keywords: ["testing", "pytest", "playwright", "unit", "integration", "e2e", "coverage"]
related_docs: ["01-project-structure.md", "02-code-quality.md"]
---
```

```markdown
# Testing Strategy

> Comprehensive testing approach from unit to end-to-end

## Testing Pyramid

```
        /\
       /  \
      / E2E \    ← Few, slow, critical journeys
     /-------\
    /  INTEG  \  ← Moderate, component interactions
   /-----------\
  /    UNIT     \ ← Many, fast, isolated tests
 /_______________\
```

### Philosophy

- **Unit tests:** Many, fast, test individual components
- **Integration tests:** Moderate, test component interactions
- **E2E tests:** Few, slow, validate critical user journeys
- **Avoid exhaustive E2E testing** - save it for critical paths

---

## Unit Testing

### Purpose
- Test individual functions/classes in isolation
- No external dependencies (DB, network, filesystem)
- Fast execution (milliseconds per test)

### Location & Structure
```
tests/unit/
├── payments/
│   ├── test_processor.py
│   └── test_models.py
└── search/
    └── test_engine.py
```

Mirror `src/` structure exactly.

### Example

```python
# src/project_name/payments/processor.py
def calculate_fee(amount: float, rate: float) -> float:
    """Calculate processing fee."""
    if amount < 0:
        raise ValueError("Amount must be positive")
    return amount * rate


# tests/unit/payments/test_processor.py
import pytest
from src.project_name.payments.processor import calculate_fee


def test_calculate_fee_positive_amount():
    assert calculate_fee(100.0, 0.03) == 3.0


def test_calculate_fee_zero_amount():
    assert calculate_fee(0.0, 0.03) == 0.0


def test_calculate_fee_negative_amount_raises():
    with pytest.raises(ValueError, match="Amount must be positive"):
        calculate_fee(-100.0, 0.03)
```

### Best Practices

1. **One assert per test** (when possible)
2. **Clear test names:** `test_<action>_<condition>_<expected_outcome>()`
3. **AAA pattern:** Arrange, Act, Assert
4. **Use fixtures** for common setup
5. **Mock external dependencies:**

```python
from unittest.mock import Mock, patch

@patch('src.project_name.payments.processor.stripe_api')
def test_process_payment_calls_stripe(mock_stripe):
    mock_stripe.charge.return_value = {"id": "ch_123"}

    result = process_payment(100.0, "tok_visa")

    mock_stripe.charge.assert_called_once_with(
        amount=10000,
        source="tok_visa"
    )
```

---

## Integration Testing

### Purpose
- Test component interactions
- Verify API contracts
- Test database operations
- Test external service integrations

### Location
```
tests/integration/
├── test_api_routes.py
├── test_database.py
└── test_external_services.py
```

### Example: API Endpoint Test

```python
import pytest
from fastapi.testclient import TestClient
from src.project_name.api import app

client = TestClient(app)


def test_create_payment_success():
    response = client.post("/payments", json={
        "amount": 100.0,
        "currency": "USD",
        "token": "tok_visa"
    })

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "succeeded"
    assert "id" in data


def test_create_payment_invalid_token():
    response = client.post("/payments", json={
        "amount": 100.0,
        "currency": "USD",
        "token": "invalid"
    })

    assert response.status_code == 400
    assert "Invalid token" in response.json()["detail"]
```

### Database Testing

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="function")
def db_session():
    """Create isolated test database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    Base.metadata.drop_all(engine)


def test_create_user(db_session):
    user = User(email="test@example.com", name="Test User")
    db_session.add(user)
    db_session.commit()

    saved_user = db_session.query(User).filter_by(email="test@example.com").first()
    assert saved_user is not None
    assert saved_user.name == "Test User"
```

---

## E2E Testing with Playwright

### Setup

```bash
# Install dependencies
uv add --dev pytest pytest-playwright

# Install browser binaries
uv run playwright install
```

### Directory Structure

```
tests/e2e/
├── pages/                  # Page Object Model
│   ├── __init__.py
│   ├── base_page.py
│   ├── login_page.py
│   ├── checkout_page.py
│   └── dashboard_page.py
├── data/                   # Test data
│   ├── users.json
│   └── products.json
├── conftest.py             # Shared fixtures
├── test_authentication.py
└── test_checkout_flow.py
```

### Page Object Model

```python
# tests/e2e/pages/base_page.py
class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate_to(self, url: str):
        self.page.goto(url)

    def wait_for_selector(self, selector: str):
        self.page.wait_for_selector(selector)


# tests/e2e/pages/login_page.py
from .base_page import BasePage

class LoginPage(BasePage):
    # Selectors
    EMAIL_INPUT = '[data-testid="email"]'
    PASSWORD_INPUT = '[data-testid="password"]'
    LOGIN_BUTTON = '[data-testid="login-btn"]'
    ERROR_MESSAGE = '[data-testid="error"]'

    def login(self, email: str, password: str):
        self.page.fill(self.EMAIL_INPUT, email)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        return self.page.text_content(self.ERROR_MESSAGE)
```

### E2E Test Example

```python
# tests/e2e/test_authentication.py
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


def test_login_with_valid_credentials_succeeds(page: Page):
    """User can log in with valid email and password."""
    login_page = LoginPage(page)

    # Navigate to login
    login_page.navigate_to("https://app.example.com/login")

    # Perform login
    login_page.login("user@example.com", "correct_password")

    # Verify redirect to dashboard
    expect(page).to_have_url("https://app.example.com/dashboard")
    expect(page.locator('[data-testid="user-menu"]')).to_be_visible()


def test_login_with_invalid_credentials_shows_error(page: Page):
    """User sees error message with invalid credentials."""
    login_page = LoginPage(page)

    login_page.navigate_to("https://app.example.com/login")
    login_page.login("user@example.com", "wrong_password")

    # Verify error message
    error = login_page.get_error_message()
    assert "Invalid email or password" in error
```

### Data Isolation

**CRITICAL:** Each test must create its own data

```python
# ❌ Bad - relies on shared data
def test_user_can_checkout():
    # Assumes user "test@example.com" exists
    login("test@example.com", "password123")
    # ...


# ✅ Good - creates own test data
@pytest.fixture
def test_user(api_client):
    """Create isolated test user via API."""
    user = api_client.create_user({
        "email": f"test_{uuid.uuid4()}@example.com",
        "password": "Test123!"
    })
    yield user
    api_client.delete_user(user.id)


def test_user_can_checkout(page: Page, test_user):
    login_page = LoginPage(page)
    login_page.login(test_user.email, "Test123!")
    # ...
```

### Selector Priority

1. **User-facing attributes** (best):
```python
page.click('role=button[name="Submit"]')
page.fill('label=Email', 'user@example.com')
```

2. **Test IDs** (good):
```python
page.click('[data-testid="submit-btn"]')
```

3. **Stable attributes** (acceptable):
```python
page.click('[aria-label="Close dialog"]')
```

4. **Avoid** (brittle):
```python
page.click('.btn-primary.mt-4')  # ❌ CSS classes
page.click('//div[3]/button[2]')  # ❌ XPath by position
```

### No Hardcoded Waits

```python
# ❌ Bad - fixed delay
import time
page.click('[data-testid="submit"]')
time.sleep(5)  # Hope it loads in 5 seconds
page.click('[data-testid="confirm"]')


# ✅ Good - wait for specific condition
page.click('[data-testid="submit"]')
expect(page.locator('[data-testid="confirm"]')).to_be_visible()
page.click('[data-testid="confirm"]')


# ✅ Good - Playwright auto-waits
page.click('[data-testid="submit"]')
page.click('[data-testid="confirm"]')  # Auto-waits for element
```

---

## Test Execution

### Run All Tests

```bash
# All tests
uv run pytest

# Specific test type
uv run pytest tests/unit/
uv run pytest tests/integration/
uv run pytest tests/e2e/
```

### Run with Coverage

```bash
# Generate coverage report
uv run pytest --cov=src --cov-report=html --cov-report=term

# Enforce minimum coverage
uv run pytest --cov=src --cov-fail-under=80
```

### Run Specific Tests

```bash
# By file
uv run pytest tests/unit/payments/test_processor.py

# By test name
uv run pytest tests/unit/ -k "test_calculate_fee"

# By marker
uv run pytest -m slow
```

### E2E with Tracing

```bash
# Enable tracing for debugging
uv run pytest tests/e2e/ --tracing on

# Open trace viewer
uv run playwright show-trace trace.zip
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Test Suite

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v1
      - run: uv sync
      - run: uv run pytest tests/unit/ --cov=src

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpass
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v1
      - run: uv sync
      - run: uv run pytest tests/integration/

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v1
      - run: uv sync
      - run: uv run playwright install --with-deps
      - run: uv run pytest tests/e2e/ --tracing on

      - name: Upload artifacts on failure
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-traces
          path: test-results/
```

---

## Coverage Requirements

| Test Type | Coverage Target | Why |
|-----------|----------------|-----|
| Unit | ≥80% | Core business logic must be tested |
| Integration | ≥60% | Key integrations verified |
| E2E | Critical paths only | Full user journeys for essential features |

### Measuring Coverage

```bash
# Generate HTML report
uv run pytest --cov=src --cov-report=html
open htmlcov/index.html

# Show missing lines
uv run pytest --cov=src --cov-report=term-missing

# XML report (for CI tools)
uv run pytest --cov=src --cov-report=xml
```

---

## Debugging Failed Tests

### Playwright Trace Viewer

```bash
# Run with tracing
uv run pytest tests/e2e/ --tracing on

# Open specific trace
uv run playwright show-trace test-results/test-login-chromium/trace.zip
```

**Trace includes:**
- Screenshots at each step
- Network activity
- Console logs
- Action timeline

### pytest Debugging

```bash
# Show print statements
uv run pytest -s

# Drop into debugger on failure
uv run pytest --pdb

# Show local variables on failure
uv run pytest -l

# Verbose output
uv run pytest -vv
```

---

## Flaky Test Management

**Flaky test:** Passes and fails intermittently without code changes

### Prevention

1. **Avoid race conditions:** Use explicit waits
2. **Isolate test data:** Each test creates own data
3. **Reset state:** Clean up after each test
4. **Avoid external dependencies:** Use mocks/stubs

### Detection

```bash
# Run tests multiple times
uv run pytest tests/ --count=10
```

### Resolution

1. **Investigate:** Use trace viewer to find root cause
2. **Fix immediately:** Flaky tests erode confidence
3. **Quarantine if needed:** Mark with `@pytest.mark.skip` temporarily
4. **Remove if unfixable:** Better no test than flaky test

---

## Test Maintenance

### Regular Tasks

- **Weekly:** Review and fix flaky tests
- **Monthly:** Update test data and fixtures
- **Per release:** Audit E2E test coverage of new features
- **Quarterly:** Refactor test utilities and helpers

### When to Delete Tests

- Test for removed feature
- Redundant coverage (testing same thing multiple ways)
- Unmaintainable or consistently flaky
- Testing framework internals (not your code)
```

---

## roocode/tool-usage-protocol.md

```yaml
---
title: "RooCode Tool Usage Protocol"
version: "2.0.0"
category: "roocode_specific"
priority: critical
applies_to: ["roocode_users"]
agent_usage: "MUST read before ANY file operation in RooCode environment"
keywords: ["roocode", "tools", "file_operations", "execute_command", "read_file", "write_to_file"]
related_docs: ["roocode/agent-capabilities.md"]
---
```

```markdown
# RooCode Tool Usage Protocol

> **MANDATE:** Always prefer specialized RooCode tools over execute_command

---

## 1. The Golden Rule

**You MUST always prefer specialized RooCode tools** (`read_file`, `list_files`, `write_to_file`, etc.) over the general-purpose `execute_command` tool.

**Use `execute_command` ONLY for:**
- Running scripts and processes
- Git operations
- Package installation
- Tasks with no specialized tool equivalent

---

## 2. Tool Equivalency Table

| ❌ Instead of this command | ✅ Use this RooCode tool | Why |
|---------------------------|------------------------|-----|
| `cat`, `head`, `tail`, `less` | `read_file` | Returns content with line numbers, supports partial reads, safer |
| `ls`, `find`, `tree` | `list_files` | Recursive, respects `.gitignore`/`.rooignore`, better formatting |
| `echo "..." >`, `>>` | `write_to_file` | **Interactive diff approval** prevents accidents |
| `touch`, `mkdir` | `write_to_file` | Auto-creates files and directories |
| `sed`, `awk` | `search_and_replace` or `apply_diff` | Powerful regex support + interactive approval |
| `grep`, `rg` | `search_files` or `codebase_search` | Fast, provides context, semantic search |
| `mv`, `cp`, `rm` | `execute_command` + confirmation | **Exception:** No specialized tools yet. MUST request user confirmation via `ask_followup_question` before executing |

---

## 3. Detailed Tool Usage

### Reading Files

```python
# ✅ Correct
<read_file>
  <path>src/project_name/payments/processor.py</path>
</read_file>

# ❌ Wrong
<execute_command>
  <command>cat src/project_name/payments/processor.py</command>
</execute_command>
```

**Benefits:**
- Line numbers for easy reference
- Partial reading of large files
- Consistent formatting

---

### Listing Files

```python
# ✅ Correct
<list_files>
  <path>src/project_name</path>
  <recursive>true</recursive>
</list_files>

# ❌ Wrong
<execute_command>
  <command>ls -R src/project_name</command>
</execute_command>
```

**Benefits:**
- Respects `.gitignore` and `.rooignore`
- Tree-style visualization
- Filters out irrelevant files

---

### Writing Files

```python
# ✅ Correct
<write_to_file>
  <path>src/project_name/api/routes.py</path>
  <content>
def health_check():
    return {"status": "healthy"}
  </content>
</write_to_file>

# ❌ Wrong
<execute_command>
  <command>echo 'def health_check():' > src/project_name/api/routes.py</command>
</execute_command>
```

**Benefits:**
- **Interactive diff view** - user approves changes
- Auto-creates parent directories
- Prevents accidental overwrites

---

### Searching Code

```python
# ✅ Correct - keyword search
<search_files>
  <query>process_payment</query>
  <path>src/project_name</path>
</search_files>

# ✅ Correct - semantic search
<codebase_search>
  <query>how do we handle failed payments?</query>
</codebase_search>

# ❌ Wrong
<execute_command>
  <command>grep -r "process_payment" src/</command>
</execute_command>
```

**Benefits:**
- `search_files`: Fast ripgrep, provides context
- `codebase_search`: Understands meaning, not just keywords

---

### Search and Replace

```python
# ✅ Correct
<search_and_replace>
  <path>src/project_name/payments/processor.py</path>
  <search>old_function_name</search>
  <replace>new_function_name</replace>
</search_and_replace>

# ❌ Wrong
<execute_command>
  <command>sed -i 's/old_function_name/new_function_name/g' src/project_name/payments/processor.py</command>
</execute_command>
```

**Benefits:**
- Regex support
- Interactive approval
- Shows context of changes

---

## 4. When execute_command IS Justified

### ✅ Appropriate Uses

#### Package Management
```bash
uv add requests
npm install lodash
pip install --upgrade pip
```

#### Running Scripts
```bash
uv run pytest
npm run dev
python scripts/development/migrate_db.py
```

#### Git Operations
```bash
git status
git commit -m "feat: add payment processing"
git push origin main
```

#### Build Tools
```bash
npm run build
uv run mypy src/
ruff check . --fix
```

---

### ❌ Inappropriate Uses (Use Specialized Tools)

```bash
# ❌ Don't use execute_command for these:
cat src/main.py              # Use read_file
ls src/                      # Use list_files
echo "code" > file.py        # Use write_to_file
grep "pattern" src/          # Use search_files
sed 's/old/new/' file.py     # Use search_and_replace
```

---

## 5. File System Operations (Special Case)

**For `mv`, `cp`, `rm` operations:**

1. **Always request confirmation first:**

```python
<ask_followup_question>
  <question>
I need to delete the file `old_config.json`. This action is permanent.
Should I proceed?
  </question>
</ask_followup_question>
```

2. **Only after confirmation, execute:**

```python
<execute_command>
  <command>rm old_config.json</command>
</execute_command>
```

**Why:** No specialized tools exist yet, but these are destructive operations.

---

## 6. Decision Tree

```
Need to perform file operation?
│
├─ Reading file content?
│  └─ Use read_file
│
├─ Listing directory?
│  └─ Use list_files
│
├─ Writing/creating file?
│  └─ Use write_to_file
│
├─ Searching code?
│  ├─ Keyword search? → Use search_files
│  └─ Semantic search? → Use codebase_search
│
├─ Modifying file content?
│  └─ Use search_and_replace or apply_diff
│
├─ Moving/copying/deleting files?
│  ├─ Ask confirmation via ask_followup_question
│  └─ Then use execute_command
│
└─ Running scripts, installing packages, git operations?
   └─ Use execute_command
```

---

## 7. Rationale

### Why This Protocol Exists

1. **Reliability:** Specialized tools have structured output
2. **Safety:** Interactive diff approval prevents accidents
3. **Integration:** Better integrated with RooCode environment
4. **User Experience:** Clearer intent, better error messages
5. **Auditability:** Tool usage is tracked and logged

### Performance Comparison

| Operation | execute_command | Specialized Tool | Winner |
|-----------|----------------|------------------|--------|
| Read file | ~50ms | ~30ms | Specialized |
| List files (recursive) | ~200ms | ~100ms | Specialized |
| Search code | ~150ms | ~80ms | Specialized |
| Write file | ~40ms | ~60ms + approval | execute_command (but less safe) |

**Conclusion:** Specialized tools are faster AND safer in most cases.

---

## 8. Common Mistakes

### Mistake 1: Using cat for file reading

```python
# ❌ Wrong
<execute_command>
  <command>cat src/main.py</command>
</execute_command>

# ✅ Correct
<read_file>
  <path>src/main.py</path>
</read_file>
```

### Mistake 2: Using echo for file writing

```python
# ❌ Wrong
<execute_command>
  <command>echo "print('hello')" > test.py</command>
</execute_command>

# ✅ Correct
<write_to_file>
  <path>test.py</path>
  <content>print('hello')</content>
</write_to_file>
```

### Mistake 3: Using grep for code search

```python
# ❌ Wrong
<execute_command>
  <command>grep -r "payment" src/</command>
</execute_command>

# ✅ Correct
<search_files>
  <query>payment</query>
  <path>src</path>
</search_files>
```

---

## 9. Quick Reference

**Always use specialized tools for:**
- 📖 Reading files
- 📝 Writing files
- 📂 Listing directories
- 🔍 Searching code
- ✏️  Modifying files

**Use execute_command only for:**
- 📦 Package management
- 🏃 Running scripts
- 🔄 Git operations
- 🔧 Build tools
- 🗑️  File system operations (with confirmation)

---

**Remember:** When in doubt, check this protocol. Using the wrong tool will reduce efficiency and may cause errors.
```

---

## roocode/agent-capabilities.md

```yaml
---
title: "RooCode Agent Capabilities"
version: "2.0.0"
category: "roocode_specific"
priority: reference
applies_to: ["roocode_users"]
agent_usage: "Reference when delegating tasks or choosing which agent to invoke"
keywords: ["agents", "delegation", "orchestrator", "architect", "code", "debug"]
related_docs: ["roocode/tool-usage-protocol.md"]
---
```

```markdown
# RooCode Agent Capabilities Handbook

> Single source of truth for agent roles, capabilities, and delegation decisions

---

## 1. Philosophy

This document defines:
- What each AI agent specializes in
- When to use each agent
- How agents should collaborate

**Source:** Derived from RooCode system prompts (`roo_code_mode.md`)

---

## 2. Agent Directory

### 🪃 Orchestrator

**Role:** Strategic coordinator for complex multi-step projects

**Specializes in:**
- Breaking down large tasks into subtasks
- Coordinating work between specialized agents
- Managing workflow and dependencies
- High-level project planning

**Use when:**
- Task requires multiple specialists
- Complex, multi-phase project
- Need to coordinate dependencies between subtasks
- Managing a feature that touches multiple systems

**Does NOT:**
- Write code directly (delegates to Code agent)
- Debug issues (delegates to Debug agent)
- Research codebase alone (delegates to Project Research)

**Example tasks:**
- "Build a complete payment processing system"
- "Migrate authentication from JWT to OAuth"
- "Refactor the entire API layer"

---

### 🗿️ Architect

**Role:** Technical leader focused on planning and design

**Specializes in:**
- Information gathering and analysis
- Creating detailed implementation plans
- Technical specifications and design documents
- Breaking down complex problems

**Use when:**
- Need to design before implementing
- Planning system architecture
- Creating technical specifications
- Analyzing trade-offs between approaches

**Output:** Detailed `implementation-plan` document

**Does NOT:**
- Implement code (delegates to Code agent)
- Make code changes during planning phase

**Example tasks:**
- "Design a caching layer for the API"
- "Create an implementation plan for real-time notifications"
- "Analyze and propose solution for performance bottleneck"

---

### 💻 Code

**Role:** Highly skilled software engineer

**Specializes in:**
- Writing new code
- Modifying existing code
- Refactoring and optimization
- Implementing features from specifications
- Code reviews and improvements

**Use when:**
- Need to write code
- Implementing features
- Refactoring existing code
- Making any code changes

**Does NOT:**
- Plan architecture (Architect does this)
- Debug complex issues (Debug agent better suited)
- Research codebase structure (Project Research better)

**Example tasks:**
- "Implement the payment processor class"
- "Add validation to the user registration endpoint"
- "Refactor the database query for better performance"

---

### 🪲 Debug

**Role:** Expert in systematic problem diagnosis

**Specializes in:**
- Investigating errors and exceptions
- Diagnosing performance issues
- Troubleshooting bugs
- Root cause analysis
- Creating reproduction steps

**Use when:**
- Something is broken
- Errors or exceptions occurring
- Unexpected behavior
- Performance problems
- Need to understand why code fails

**Does NOT:**
- Implement new features (Code agent does this)
- Write initial code (Code agent better)

**Example tasks:**
- "Why is the payment endpoint returning 500 errors?"
- "Investigate why tests are failing in CI"
- "Find the cause of memory leak in the background worker"

---

### ❓ Ask

**Role:** Knowledgeable technical assistant

**Specializes in:**
- Answering technical questions
- Providing explanations
- Clarifying concepts
- Documentation lookup
- Knowledge sharing

**Use when:**
- Need information or explanation
- Understanding how something works
- Learning about technologies or patterns
- Clarifying documentation

**Does NOT:**
- Make code changes (read-only)
- Implement features
- Debug issues

**Example tasks:**
- "Explain how dependency injection works"
- "What's the difference between async/await and promises?"
- "How should I structure my test fixtures?"

---

### 🔬 Project Research

**Role:** Detail-oriented codebase analyst

**Specializes in:**
- Examining project structure
- Analyzing file dependencies
- Understanding existing implementations
- Mapping architecture
- Finding patterns in code

**Use when:**
- Need to understand codebase structure
- Analyzing existing architecture
- Finding how features are currently implemented
- Mapping dependencies
- Before making large changes

**Does NOT:**
- Make code changes
- Implement features

**Example tasks:**
- "Map out how authentication currently works"
- "Find all places where the User model is used"
- "Analyze the project structure and dependencies"

---

### 📝 User Story Creator

**Role:** Agile requirements specialist

**Specializes in:**
- Creating user stories
- Defining acceptance criteria
- Breaking down requirements
- Clarifying feature scope
- Writing clear specifications

**Use when:**
- Need to create user stories
- Breaking down large features
- Defining acceptance criteria
- Clarifying requirements

**Output:** Well-formed user stories with acceptance criteria

**Does NOT:**
- Implement features
- Write technical specifications (Architect does this)

**Example tasks:**
- "Create user stories for the checkout flow"
- "Break down the 'user profile' epic into stories"
- "Define acceptance criteria for payment processing"

---

### ✍️ Documentation Writer

**Role:** Technical documentation expert

**Specializes in:**
- Creating technical documentation
- Writing API documentation
- Creating user guides
- Updating README files
- Documenting architecture

**Use when:**
- Need to create documentation
- Update existing docs
- Write API specifications
- Create user guides
- Document architecture decisions

**Does NOT:**
- Write code
- Implement features

**Example tasks:**
- "Create API documentation for the payment endpoints"
- "Update the README with new setup instructions"
- "Document the authentication flow"

---

## 3. Agent Selection Decision Tree

```
What type of task?
│
├─ Complex multi-step project?
│  └─ Use Orchestrator (will delegate to others)
│
├─ Need to plan/design before building?
│  └─ Use Architect → then Code for implementation
│
├─ Need to write/modify code?
│  └─ Use Code
│
├─ Something is broken?
│  └─ Use Debug
│
├─ Need to understand existing code?
│  └─ Use Project Research
│
├─ Need to answer a question?
│  └─ Use Ask
│
├─ Need to create user stories?
│  └─ Use User Story Creator
│
└─ Need to write documentation?
   └─ Use Documentation Writer
```

---

## 4. Common Agent Combinations

### New Feature Development
1. **Architect:** Design and plan
2. **Code:** Implement
3. **Documentation Writer:** Document

### Bug Investigation and Fix
1. **Debug:** Find root cause
2. **Code:** Implement fix
3. **Code:** Add test to prevent regression

### Large Refactoring
1. **Orchestrator:** Break down into phases
2. **Project Research:** Analyze current structure
3. **Architect:** Design new structure
4. **Code:** Implement changes incrementally

### New Project Setup
1. **Orchestrator:** Coordinate overall setup
2. **Architect:** Design architecture
3. **Code:** Implement base structure
4. **Documentation Writer:** Create README and docs

---

## 5. Delegation Examples

### Example 1: "Build a payment system"

**Orchestrator thinks:**
1. This is complex, multi-step → I should coordinate
2. Need design first → Delegate to Architect
3. Architect creates plan
4. Need implementation → Delegate to Code
5. Need docs → Delegate to Documentation Writer

### Example 2: "The login endpoint is broken"

**Orchestrator thinks:**
1. Something is broken → Delegate to Debug
2. Debug finds issue: missing validation
3. Need code fix → Delegate to Code
4. Code implements fix + test

### Example 3: "How does our caching work?"

**Orchestrator thinks:**
1. Question about existing code → Delegate to Ask or Project Research
2. If just explanation → Ask
3. If need deep analysis → Project Research

---

## 6. Agent Limitations

| Agent | Cannot Do | Instead Use |
|-------|-----------|-------------|
| Orchestrator | Write code directly | Code agent |
| Architect | Implement during planning | Code agent (after plan) |
| Code | Plan architecture | Architect agent |
| Debug | Implement new features | Code agent |
| Ask | Make any changes | Code/Debug agents |
| Project Research | Modify code | Code agent |
| User Story Creator | Write technical specs | Architect agent |
| Documentation Writer | Implement features | Code agent |

---

## 7. Best Practices for Task Delegation

### Do:
- ✅ Use Orchestrator for complex tasks needing coordination
- ✅ Plan with Architect before big implementations
- ✅ Use Project Research before large refactorings
- ✅ Delegate bugs to Debug agent first
- ✅ Let each agent focus on their specialty

### Don't:
- ❌ Ask Code agent to design architecture
- ❌ Ask Debug agent to implement new features
- ❌ Skip Architect for complex system changes
- ❌ Use Ask agent when you need changes made

---

## 8. Quick Reference

**Need to build something complex?** → Orchestrator

**Need a plan first?** → Architect

**Need code written?** → Code

**Something broken?** → Debug

**Need to understand existing code?** → Project Research

**Just have a question?** → Ask

**Need user stories?** → User Story Creator

**Need documentation?** → Documentation Writer

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-10-19 | Added YAML frontmatter, improved structure |
| 1.0.0 | - | Initial version |
```

---

## Summary of YAML Metadata Benefits

### For AI Agents:

1. **Quick filtering:** Check `priority` to know if must-read
2. **Context awareness:** `applies_to` indicates relevance
3. **Smart navigation:** `related_docs` for deep dives
4. **Task matching:** `keywords` help find right document
5. **Version tracking:** Know if information is current
6. **Purpose clarity:** `agent_usage` explains when to read

### Metadata Fields Explained:

- **title:** Human-readable document name
- **version:** Semantic versioning for tracking changes
- **category:** Type of content (architecture, testing, etc.)
- **priority:** critical | contextual | reference
- **applies_to:** all_projects | roocode_users
- **agent_usage:** When and why to read this document
- **keywords:** Searchable terms for quick lookup
- **related_docs:** Cross-references to other guidelines
