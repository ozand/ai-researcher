"""Configuration management for AI Researcher."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv  # type: ignore[import-not-found]


@dataclass
class LLMConfig:
    """Configuration for LLM providers."""

    provider: str = "gemini"
    model: str = "gemini-1.5-flash"
    api_key: str | None = None
    base_url: str | None = None
    max_tokens: int = 8192
    temperature: float = 0.7
    timeout: int = 30


@dataclass
class DataConfig:
    """Configuration for data handling."""

    mindmap_csv_path: str = "data/mindmap.csv"
    output_dir: str = "output"
    cache_dir: str = ".cache"
    max_file_size_mb: int = 100


@dataclass
class EngineConfig:
    """Configuration for research engine."""

    max_recursion_depth: int = 5
    concurrent_queries: int = 3
    session_timeout: int = 3600
    auto_save_interval: int = 300


@dataclass
class Config:
    """Main configuration class."""

    llm: LLMConfig = field(default_factory=LLMConfig)
    data: DataConfig = field(default_factory=DataConfig)
    engine: EngineConfig = field(default_factory=EngineConfig)

    # Mode settings
    mode: str = "semi-manual"  # "automatic", "semi-manual", "manual"
    debug: bool = False
    log_level: str = "INFO"


class ConfigManager:
    """Manages configuration loading and validation."""

    def __init__(self, config_path: str | None = None):
        self.config_path = config_path or ".taskmaster/config.yaml"
        self.config = Config()
        self._load_environment()
        self._load_config_file()
        self._validate_config()

    def _load_environment(self) -> None:
        """Load environment variables from .env file."""
        # Try to load .env from project root and .taskmaster directory
        env_paths = [Path(".env"), Path(".taskmaster/.env"), Path("../.env")]

        for env_path in env_paths:
            if env_path.exists():
                load_dotenv(env_path)
                break

    def _load_config_file(self) -> None:
        """Load configuration from YAML file."""
        config_file = Path(self.config_path)
        if config_file.exists():
            try:
                with config_file.open("r", encoding="utf-8") as f:
                    config_data = yaml.safe_load(f)
                    if config_data:
                        self._update_config_from_dict(config_data)
            except yaml.YAMLError as e:
                raise ValueError(
                    f"Invalid YAML in config file {config_file}: {e}"
                ) from e
            except Exception as e:
                raise ValueError(f"Error loading config file {config_file}: {e}") from e

    def _update_config_from_dict(self, config_data: dict[str, Any]) -> None:
        """Update config object from dictionary."""
        if "llm" in config_data:
            llm_data = config_data["llm"]
            for key, value in llm_data.items():
                if hasattr(self.config.llm, key):
                    setattr(self.config.llm, key, value)

        if "data" in config_data:
            data_data = config_data["data"]
            for key, value in data_data.items():
                if hasattr(self.config.data, key):
                    setattr(self.config.data, key, value)

        if "engine" in config_data:
            engine_data = config_data["engine"]
            for key, value in engine_data.items():
                if hasattr(self.config.engine, key):
                    setattr(self.config.engine, key, value)

        # Update root level settings
        for key in ["mode", "debug", "log_level"]:
            if key in config_data:
                setattr(self.config, key, config_data[key])

    def _validate_config(self) -> None:
        """Validate configuration settings."""
        # Validate LLM config
        if self.config.llm.provider not in [
            "gemini",
            "openai",
            "anthropic",
            "perplexity",
        ]:
            raise ValueError(f"Unsupported LLM provider: {self.config.llm.provider}")

        MAX_TEMPERATURE = 2
        if (
            self.config.llm.temperature < 0
            or self.config.llm.temperature > MAX_TEMPERATURE
        ):
            raise ValueError("LLM temperature must be between 0 and 2")

        if self.config.llm.max_tokens <= 0:
            raise ValueError("LLM max_tokens must be positive")

        # Validate data config
        if self.config.data.max_file_size_mb <= 0:
            raise ValueError("Max file size must be positive")

        # Validate engine config
        if self.config.engine.max_recursion_depth <= 0:
            raise ValueError("Max recursion depth must be positive")

        if self.config.engine.concurrent_queries <= 0:
            raise ValueError("Concurrent queries must be positive")

        # Validate mode
        if self.config.mode not in ["automatic", "semi-manual", "manual"]:
            raise ValueError(f"Invalid mode: {self.config.mode}")

        # Validate log level
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.config.log_level not in valid_log_levels:
            raise ValueError(f"Invalid log level: {self.config.log_level}")

    def get_api_key(self, provider: str) -> str | None:
        """Get API key for specified provider."""
        key_mapping = {
            "gemini": "GOOGLE_API_KEY",
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "perplexity": "PERPLEXITY_API_KEY",
        }

        env_key = key_mapping.get(provider)
        if env_key:
            return os.getenv(env_key)

        return None

    def get_llm_config(self, provider: str | None = None) -> LLMConfig:
        """Get LLM configuration for specified provider."""
        if provider is None:
            provider = self.config.llm.provider

        return LLMConfig(
            provider=provider,
            model=self.config.llm.model,
            api_key=self.get_api_key(provider),
            base_url=self.config.llm.base_url,
            max_tokens=self.config.llm.max_tokens,
            temperature=self.config.llm.temperature,
            timeout=self.config.llm.timeout,
        )

    def ensure_directories(self) -> None:
        """Ensure required directories exist."""
        directories = [
            self.config.data.output_dir,
            self.config.data.cache_dir,
            Path(self.config.data.mindmap_csv_path).parent,
        ]

        for directory in directories:
            Path(str(directory)).mkdir(parents=True, exist_ok=True)

    def save_config(self, path: str | None = None) -> None:
        """Save current configuration to YAML file."""
        save_path = path or self.config_path

        config_dict = {
            "llm": {
                "provider": self.config.llm.provider,
                "model": self.config.llm.model,
                "base_url": self.config.llm.base_url,
                "max_tokens": self.config.llm.max_tokens,
                "temperature": self.config.llm.temperature,
                "timeout": self.config.llm.timeout,
            },
            "data": {
                "mindmap_csv_path": self.config.data.mindmap_csv_path,
                "output_dir": self.config.data.output_dir,
                "cache_dir": self.config.data.cache_dir,
                "max_file_size_mb": self.config.data.max_file_size_mb,
            },
            "engine": {
                "max_recursion_depth": self.config.engine.max_recursion_depth,
                "concurrent_queries": self.config.engine.concurrent_queries,
                "session_timeout": self.config.engine.session_timeout,
                "auto_save_interval": self.config.engine.auto_save_interval,
            },
            "mode": self.config.mode,
            "debug": self.config.debug,
            "log_level": self.config.log_level,
        }

        # Remove None values and API keys from saved config
        def clean_dict(d: Any) -> Any:
            if isinstance(d, dict):
                return {
                    k: clean_dict(v)
                    for k, v in d.items()
                    if v is not None and "api_key" not in k
                }
            return d

        cleaned_dict = clean_dict(config_dict)

        with Path(save_path).open("w", encoding="utf-8") as f:
            yaml.dump(cleaned_dict, f, default_flow_style=False, indent=2)


# Global configuration instance
config_manager = ConfigManager()
config = config_manager.config
