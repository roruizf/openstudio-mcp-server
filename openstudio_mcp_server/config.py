"""
Configuration management for OpenStudio MCP Server.

Handles paths, environment variables, and server settings.
"""

import os
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import platform


@dataclass
class OpenStudioConfig:
    """OpenStudio installation and configuration settings."""

    version: str = "3.7.0"
    installation_dir: Optional[str] = None
    sdk_path: Optional[str] = None
    weather_data_dir: Optional[str] = None
    default_weather_file: str = "USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"
    example_files_dir: Optional[str] = None

    def __post_init__(self):
        """Auto-detect OpenStudio installation if not specified."""
        if not self.installation_dir:
            self.installation_dir = self._detect_openstudio_installation()

        if not self.sdk_path and self.installation_dir:
            self.sdk_path = os.path.join(self.installation_dir, "lib")

    def _detect_openstudio_installation(self) -> str:
        """Detect OpenStudio installation directory."""
        # Check environment variable first
        env_path = os.getenv("OPENSTUDIO_PATH")
        if env_path and os.path.exists(env_path):
            return env_path

        # Platform-specific default paths
        system = platform.system()
        possible_paths = []

        if system == "Linux":
            possible_paths = [
                f"/usr/local/openstudio-{self.version}",
                "/usr/local/openstudio",
                "/app/software/OpenStudio",  # Docker container path
            ]
        elif system == "Darwin":  # macOS
            possible_paths = [
                f"/Applications/OpenStudio-{self.version}",
                "/Applications/OpenStudio",
            ]
        elif system == "Windows":
            possible_paths = [
                f"C:\\openstudio-{self.version}",
                "C:\\openstudio",
                f"C:\\Program Files\\OpenStudio-{self.version}",
            ]

        # Return first existing path
        for path in possible_paths:
            if os.path.exists(path):
                return path

        # Default fallback
        return f"/usr/local/openstudio-{self.version}"


@dataclass
class PathConfig:
    """File system paths for the MCP server."""

    workspace_root: str = "/workspace"
    sample_files_path: Optional[str] = None
    temp_dir: str = "/tmp"
    output_dir: Optional[str] = None
    logs_dir: Optional[str] = None

    def __post_init__(self):
        """Set default paths based on workspace root."""
        # Detect workspace root if running outside Docker
        if not os.path.exists(self.workspace_root):
            # Try current working directory's parent (if we're in a subdirectory)
            cwd = os.getcwd()
            if os.path.basename(cwd) == "openstudio-mcp-server":
                self.workspace_root = os.path.dirname(cwd)
            else:
                self.workspace_root = cwd

        if not self.sample_files_path:
            self.sample_files_path = os.path.join(self.workspace_root, "sample_files")

        if not self.output_dir:
            self.output_dir = os.path.join(self.workspace_root, "outputs")

        if not self.logs_dir:
            self.logs_dir = os.path.join(self.workspace_root, "logs")

        # Create directories if they don't exist (ignore permission errors)
        for directory in [self.sample_files_path, self.output_dir, self.logs_dir]:
            try:
                os.makedirs(directory, exist_ok=True)
            except (PermissionError, OSError):
                # If we can't create directories (e.g., in Docker with read-only mount),
                # continue anyway - they might already exist
                pass


@dataclass
class ServerConfig:
    """MCP Server configuration settings."""

    name: str = "openstudio-mcp-server"
    version: str = "0.1.0"
    log_level: str = "INFO"
    simulation_timeout: int = 600  # 10 minutes
    tool_timeout: int = 60  # 1 minute


@dataclass
class Config:
    """Main configuration container."""

    openstudio: OpenStudioConfig = field(default_factory=OpenStudioConfig)
    paths: PathConfig = field(default_factory=PathConfig)
    server: ServerConfig = field(default_factory=ServerConfig)


def setup_logging(config: Config) -> None:
    """Configure logging for the MCP server.

    Args:
        config: Configuration object with logging settings
    """
    log_level = getattr(logging, config.server.log_level.upper(), logging.INFO)

    # Create logs directory if it doesn't exist (ignore permission errors)
    try:
        os.makedirs(config.paths.logs_dir, exist_ok=True)
    except (PermissionError, OSError):
        # Can't create logs directory in Docker, just log to console
        pass

    # Prepare handlers - start with console
    handlers = [logging.StreamHandler()]  # Console output always available

    # Try to add file handlers if we have write permission
    try:
        main_log_file = os.path.join(config.paths.logs_dir, "openstudio_mcp_server.log")
        handlers.append(logging.FileHandler(main_log_file))
    except (PermissionError, OSError):
        # Can't write log files, console only
        pass

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers,
    )

    # Try to add error log handler if we have write permission
    try:
        error_log_file = os.path.join(config.paths.logs_dir, "openstudio_mcp_errors.log")
        error_handler = logging.FileHandler(error_log_file)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logging.getLogger().addHandler(error_handler)
    except (PermissionError, OSError):
        # Can't write error log file, skip it
        pass

    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized at {log_level} level")
    if handlers and len(handlers) > 1:
        logger.info(f"Logging to console and files in {config.paths.logs_dir}")
    else:
        logger.info(f"Logging to console only")


def get_config() -> Config:
    """Get the configuration object.

    Returns:
        Config: Initialized configuration object
    """
    config = Config()
    setup_logging(config)
    return config


def get_configuration_info(config: Config) -> dict:
    """Get configuration information as a dictionary.

    Args:
        config: Configuration object

    Returns:
        Dictionary with configuration details
    """
    return {
        "server": {
            "name": config.server.name,
            "version": config.server.version,
            "log_level": config.server.log_level,
            "simulation_timeout": config.server.simulation_timeout,
            "tool_timeout": config.server.tool_timeout,
        },
        "openstudio": {
            "version": config.openstudio.version,
            "installation_dir": config.openstudio.installation_dir,
            "sdk_path": config.openstudio.sdk_path,
            "default_weather_file": config.openstudio.default_weather_file,
        },
        "paths": {
            "workspace_root": config.paths.workspace_root,
            "sample_files": config.paths.sample_files_path,
            "output_dir": config.paths.output_dir,
            "logs_dir": config.paths.logs_dir,
            "temp_dir": config.paths.temp_dir,
        },
    }
