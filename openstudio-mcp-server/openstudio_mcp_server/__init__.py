"""OpenStudio MCP Server - A Model Context Protocol server for OpenStudio."""

__version__ = "0.1.0"
__author__ = "Roberto Ruiz"
__email__ = "roruizf@gmail.com"

from openstudio_mcp_server.config import get_config
from openstudio_mcp_server.openstudio_tools import OpenStudioManager

__all__ = ["get_config", "OpenStudioManager"]
