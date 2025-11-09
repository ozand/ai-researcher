"""Tests for configuration management."""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest  # type: ignore[import-not-found]
import yaml

from src.core.config import Config, ConfigManager, DataConfig, EngineConfig, LLMConfig


class TestConfigManager:
    """Test cases for ConfigManager class."""

    def test_default_configuration(self):
        """Test that default configuration is valid."""
        config_manager = ConfigManager()
        config = config_manager.config

        assert isinstance(config, Config)
        assert config.llm.provider == "gemini"
        assert config.mode == "semi-manual"
        assert config.debug is False
        assert config.log_level == "INFO"

    def test_load_config_from_yaml(self):
        """Test loading configuration from YAML file."""
        config_data = {
            "llm": {"provider": "openai", "model": "gpt-4", "temperature": 0.5},
            "mode": "automatic",
            "debug": True,
            "log_level": "DEBUG",
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = f.name

        try:
            config_manager = ConfigManager(temp_path)
            config = config_manager.config

            assert config.llm.provider == "openai"
            assert config.llm.model == "gpt-4"
            assert config.llm.temperature == 0.5
            assert config.mode == "automatic"
            assert config.debug is True
            assert config.log_level == "DEBUG"
        finally:
            Path(temp_path).unlink()

    def test_invalid_yaml_raises_error(self):
        """Test that invalid YAML raises ValueError."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("invalid: yaml: content: [")
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="Invalid YAML"):
                ConfigManager(temp_path)
        finally:
            Path(temp_path).unlink()

    def test_invalid_llm_provider(self):
        """Test validation of invalid LLM provider."""
        config_data = {"llm": {"provider": "invalid_provider"}}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="Unsupported LLM provider"):
                ConfigManager(temp_path)
        finally:
            Path(temp_path).unlink()

    def test_invalid_temperature_range(self):
        """Test validation of temperature range."""
        config_data = {"llm": {"temperature": 3.0}}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="temperature must be between 0 and 2"):
                ConfigManager(temp_path)
        finally:
            Path(temp_path).unlink()

    def test_invalid_mode(self):
        """Test validation of invalid mode."""
        config_data = {"mode": "invalid_mode"}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="Invalid mode"):
                ConfigManager(temp_path)
        finally:
            Path(temp_path).unlink()

    def test_get_api_key(self):
        """Test getting API keys for different providers."""
        config_manager = ConfigManager()

        with patch.dict(
            os.environ,
            {
                "GOOGLE_API_KEY": "test_gemini_key",
                "OPENAI_API_KEY": "test_openai_key",
                "ANTHROPIC_API_KEY": "test_anthropic_key",
            },
        ):
            assert config_manager.get_api_key("gemini") == "test_gemini_key"
            assert config_manager.get_api_key("openai") == "test_openai_key"
            assert config_manager.get_api_key("anthropic") == "test_anthropic_key"
            assert config_manager.get_api_key("perplexity") is None
            assert config_manager.get_api_key("invalid") is None

    def test_get_llm_config(self):
        """Test getting LLM configuration."""
        config_manager = ConfigManager()

        with patch.dict(os.environ, {"GOOGLE_API_KEY": "test_key"}):
            llm_config = config_manager.get_llm_config("gemini")

            assert isinstance(llm_config, LLMConfig)
            assert llm_config.provider == "gemini"
            assert llm_config.api_key == "test_key"
            assert llm_config.model == config_manager.config.llm.model

    def test_ensure_directories(self):
        """Test directory creation."""
        config_manager = ConfigManager()

        with tempfile.TemporaryDirectory() as temp_dir:
            config_manager.config.data.output_dir = str(Path(temp_dir) / "output")
            config_manager.config.data.cache_dir = str(Path(temp_dir) / "cache")
            config_manager.config.data.mindmap_csv_path = str(
                Path(temp_dir) / "data" / "test.csv"
            )

            config_manager.ensure_directories()

            assert Path(config_manager.config.data.output_dir).exists()
            assert Path(config_manager.config.data.cache_dir).exists()
            assert Path(config_manager.config.data.mindmap_csv_path).parent.exists()

    def test_save_config(self):
        """Test saving configuration to file."""
        config_manager = ConfigManager()
        config_manager.config.mode = "automatic"
        config_manager.config.debug = True

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            temp_path = f.name

        try:
            config_manager.save_config(temp_path)

            # Load and verify saved config
            with Path(temp_path).open("r") as f:
                saved_data = yaml.safe_load(f)

            assert saved_data["mode"] == "automatic"
            assert saved_data["debug"] is True
            # API keys should not be saved
            assert "api_key" not in str(saved_data)
        finally:
            Path(temp_path).unlink()


class TestConfigDataclasses:
    """Test cases for configuration dataclasses."""

    def test_llm_config_defaults(self):
        """Test LLMConfig default values."""
        config = LLMConfig()

        assert config.provider == "gemini"
        assert config.model == "gemini-1.5-flash"
        assert config.api_key is None
        assert config.max_tokens == 8192
        assert config.temperature == 0.7
        assert config.timeout == 30

    def test_data_config_defaults(self):
        """Test DataConfig default values."""
        config = DataConfig()

        assert config.mindmap_csv_path == "data/mindmap.csv"
        assert config.output_dir == "output"
        assert config.cache_dir == ".cache"
        assert config.max_file_size_mb == 100

    def test_engine_config_defaults(self):
        """Test EngineConfig default values."""
        config = EngineConfig()

        assert config.max_recursion_depth == 5
        assert config.concurrent_queries == 3
        assert config.session_timeout == 3600
        assert config.auto_save_interval == 300
