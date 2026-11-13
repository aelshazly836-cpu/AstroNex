from modules.stress_analyzer import analyze_stress_data
from pathlib import Path


TOOLS = {
    "stress_analyzer": {
        "description": "Analyze wearable sensor data for stress-related signals.",
        "function": analyze_stress_data
    }
}


def run_tool(tool_name, **kwargs):
    """Run a registered AstroNex AI tool."""

    tool = TOOLS.get(tool_name)

    if tool is None:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}"
        }

    try:
        return tool["function"](**kwargs)

    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }


def get_available_tools():
    """Return the tools available to the AI Engine."""

    return {
        name: tool["description"]
        for name, tool in TOOLS.items()
    }