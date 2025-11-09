# AI Researcher

AI-powered research automation system that leverages multiple LLM providers to streamline research workflows and generate comprehensive insights.

## 🚀 Features

- **Multi-LLM Support**: Integration with OpenAI, Anthropic, and Google Gemini
- **Automated Research**: Streamlined research pipeline with intelligent data collection
- **Configurable Workflows**: Customizable research templates and parameters
- **Data Export**: Multiple output formats (CSV, JSON, Markdown)
- **Quality Assured**: Comprehensive code quality tools and CI/CD pipeline

## 🛠️ Tech Stack

- **Python 3.12+**: Modern Python with type hints
- **LLM Integration**: OpenAI, Anthropic, Google Generative AI
- **Data Processing**: Pandas, YAML, Jinja2
- **CLI Interface**: Rich terminal output with Click
- **Quality Tools**: Ruff, MyPy, Bandit, Pre-commit
- **CI/CD**: GitHub Actions with automated testing

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/ozand/ai-researcher.git
cd ai-researcher

# Install development dependencies
pip install -e .[dev]

# Or install production version
pip install ai-researcher
```

## 🔧 Configuration

Create a `.env` file in the project root:

```env
# LLM Provider Configuration
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Default Settings
DEFAULT_LLM_PROVIDER=gemini
DEFAULT_MODEL=gemini-1.5-flash
```

## 🚀 Quick Start

```bash
# Run with default settings
ai-researcher

# Use specific LLM provider
ai-researcher --provider openai --model gpt-4

# Custom research query
ai-researcher --query "machine learning trends 2024" --output results/
```

## 🧪 Development

```bash
# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run code quality checks
ruff check .
mypy src/
bandit -r src/

# Format code
ruff format .
```

## 📊 Project Structure

```
ai-researcher/
├── src/                    # Source code
│   ├── core/               # Core functionality
│   ├── llm/                # LLM provider integrations
│   ├── data/               # Data processing modules
│   └── utils/              # Utility functions
├── tests/                  # Test suite
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── .github/workflows/       # CI/CD pipeline
├── .taskmaster/           # Task Master configuration
└── docs/                  # Documentation
```

## 🔍 Code Quality

This project maintains high code quality standards:

- **Linting**: Ruff with comprehensive rule set
- **Type Checking**: MyPy with strict type enforcement
- **Security**: Bandit security scanning
- **Testing**: Comprehensive test coverage
- **CI/CD**: Automated GitHub Actions pipeline

## 📈 Status

![CI Status](https://github.com/ozand/ai-researcher/workflows/CI/badge.svg)
![Coverage](https://codecov.io/gh/ozand/ai-researcher/branch/main/graph/badge.svg)
![Code Quality](https://img.shields.io/badge/code%20quality-A%2B-brightgreen)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Task Master AI](https://github.com) for project management and workflow automation
- [OpenAI](https://openai.com) for GPT models
- [Anthropic](https://anthropic.com) for Claude models
- [Google](https://ai.google.dev) for Gemini models

---

**Built with ❤️ using AI-powered development tools**
