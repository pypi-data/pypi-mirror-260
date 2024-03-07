from typing import Dict, NamedTuple

from autokit import PlatformData


class ToolConfig(NamedTuple):
    """
    A class to represent the configuration for a tool.

    Attributes
    ----------
    tool_name : str
        The name of the tool.
    python : bool
        Whether the tool should be executed by the Python interpreter or treated as an executable.
    platform_data : Dict[str, PlatformData]
        The platform data for the tool.
    """
    tool_name: str
    python: bool
    platform_data: Dict[str, PlatformData]

