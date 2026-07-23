"""
Hermes AI OS — MCPs Package

Model Context Protocol adapters that abstract data sources.
Each MCP connector exposes a uniform interface for fetching
job listings from different career platforms.
"""

from mcps.gateway import MCPGateway

__all__ = ["MCPGateway"]
