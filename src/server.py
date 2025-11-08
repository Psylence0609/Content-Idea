"""Main MCP server for Content Creation tools."""

import asyncio
import json
from typing import Any
from concurrent.futures import ThreadPoolExecutor
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

from .tools.ideas import (
    generate_ideas,
    generate_reddit_ideas,
    generate_youtube_ideas,
    generate_news_ideas
)
from .tools.script import generate_script, generate_script_from_ideas, generate_complete_script
from .config import config


# Initialize the MCP server
app = Server("content-mcp-server")

# Thread pool executor for running synchronous blocking operations (like PRAW)
# This prevents blocking the async event loop and eliminates PRAW warnings
_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="mcp-worker")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return [
        Tool(
            name="generate_ideas",
            description=(
                "Generate content ideas by aggregating trending topics from multiple sources "
                "(Reddit, YouTube, and Google News). Returns structured data with trending topics "
                "and metadata from all sources."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic or event to search for (e.g., 'AI', 'Trump', 'climate change')"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results per source (default: 10)",
                        "default": 10
                    }
                },
                "required": ["topic"]
            }
        ),
        Tool(
            name="generate_reddit_ideas",
            description=(
                "Generate content ideas from Reddit only. Search for trending posts "
                "in specific subreddits or across all of Reddit."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic to search for"
                    },
                    "subreddit": {
                        "type": "string",
                        "description": "Target subreddit (default: 'all')",
                        "default": "all"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 10)",
                        "default": 10
                    }
                },
                "required": ["topic"]
            }
        ),
        Tool(
            name="generate_youtube_ideas",
            description=(
                "Generate content ideas from YouTube only. Search for trending videos "
                "related to a topic with various sort options."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic to search for"
                    },
                    "order": {
                        "type": "string",
                        "description": "Sort order: 'viewCount', 'relevance', 'date', or 'rating' (default: 'viewCount')",
                        "enum": ["viewCount", "relevance", "date", "rating"],
                        "default": "viewCount"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 10)",
                        "default": 10
                    }
                },
                "required": ["topic"]
            }
        ),
        Tool(
            name="generate_news_ideas",
            description=(
                "Generate content ideas from Google News only. Search for recent news articles "
                "related to a topic using RSS feeds."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic to search for"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 10)",
                        "default": 10
                    }
                },
                "required": ["topic"]
            }
        ),
        Tool(
            name="generate_script",
            description=(
                "Generate a monologue script based on a topic using OpenRouter or Groq. "
                "The script will be tailored to the specified duration and style. "
                "Automatically falls back to alternative provider if primary fails."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The main topic or subject for the script"
                    },
                    "duration_seconds": {
                        "type": "integer",
                        "description": "Target duration of the script in seconds"
                    },
                    "model": {
                        "type": "string",
                        "description": "Model to use (default: from config based on provider)",
                        "default": None
                    },
                    "style": {
                        "type": "string",
                        "description": "Style/tone of the script (default: 'informative and engaging')",
                        "default": "informative and engaging"
                    },
                    "trending_info": {
                        "type": "string",
                        "description": "Optional context from trending data to incorporate",
                        "default": None
                    },
                    "provider": {
                        "type": "string",
                        "description": f"Inference provider: 'openrouter' or 'groq' (default: {config.inference_provider})",
                        "enum": ["openrouter", "groq"],
                        "default": None
                    }
                },
                "required": ["topic", "duration_seconds"]
            }
        ),
        Tool(
            name="generate_script_from_ideas",
            description=(
                "Generate a script based on aggregated ideas data from generate_ideas(). "
                "This tool automatically incorporates trending information from multiple sources. "
                "Uses OpenRouter or Groq with automatic fallback."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "ideas_data": {
                        "type": "object",
                        "description": "Output from generate_ideas() function"
                    },
                    "duration_seconds": {
                        "type": "integer",
                        "description": "Target duration of the script in seconds"
                    },
                    "model": {
                        "type": "string",
                        "description": "Model to use (default: from config based on provider)",
                        "default": None
                    },
                    "style": {
                        "type": "string",
                        "description": "Style/tone of the script (default: 'informative and engaging')",
                        "default": "informative and engaging"
                    },
                    "provider": {
                        "type": "string",
                        "description": f"Inference provider: 'openrouter' or 'groq' (default: {config.inference_provider})",
                        "enum": ["openrouter", "groq"],
                        "default": None
                    }
                },
                "required": ["ideas_data", "duration_seconds"]
            }
        ),
        Tool(
            name="generate_complete_script",
            description=(
                "Generate a complete script in one step: automatically fetches trending topics "
                "from Reddit, YouTube, and Google News, then generates a script incorporating that information. "
                "Perfect for agents - no need to orchestrate multiple tool calls. "
                "This is the recommended tool for generating scripts from a topic."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic to research and create a script about (e.g., 'AI', 'climate change')"
                    },
                    "duration_seconds": {
                        "type": "integer",
                        "description": "Target duration of the script in seconds"
                    },
                    "provider": {
                        "type": "string",
                        "description": f"Inference provider: 'openrouter' or 'groq' (default: {config.inference_provider})",
                        "enum": ["openrouter", "groq"],
                        "default": None
                    },
                    "style": {
                        "type": "string",
                        "description": "Style/tone of the script (default: 'informative and engaging')",
                        "default": "informative and engaging"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of items to fetch per source (default: 3)",
                        "default": 3
                    },
                    "model": {
                        "type": "string",
                        "description": "Model to use (default: from config based on provider)",
                        "default": None
                    }
                },
                "required": ["topic", "duration_seconds"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool execution."""
    try:
        # Run synchronous tool functions in a thread pool to avoid blocking
        # and prevent PRAW warnings about async environments
        loop = asyncio.get_event_loop()
        
        if name == "generate_ideas":
            result = await loop.run_in_executor(
                _executor,
                lambda: generate_ideas(
                    topic=arguments["topic"],
                    limit=arguments.get("limit", 10)
                )
            )
        
        elif name == "generate_reddit_ideas":
            result = await loop.run_in_executor(
                _executor,
                lambda: generate_reddit_ideas(
                    topic=arguments["topic"],
                    subreddit=arguments.get("subreddit", "all"),
                    limit=arguments.get("limit", 10)
                )
            )
        
        elif name == "generate_youtube_ideas":
            result = await loop.run_in_executor(
                _executor,
                lambda: generate_youtube_ideas(
                    topic=arguments["topic"],
                    order=arguments.get("order", "viewCount"),
                    limit=arguments.get("limit", 10)
                )
            )
        
        elif name == "generate_news_ideas":
            result = await loop.run_in_executor(
                _executor,
                lambda: generate_news_ideas(
                    topic=arguments["topic"],
                    limit=arguments.get("limit", 10)
                )
            )
        
        elif name == "generate_script":
            # Script generation may involve API calls, run in executor
            result = await loop.run_in_executor(
                _executor,
                lambda: generate_script(
                    topic=arguments["topic"],
                    duration_seconds=arguments["duration_seconds"],
                    model=arguments.get("model"),
                    style=arguments.get("style", "informative and engaging"),
                    trending_info=arguments.get("trending_info"),
                    provider=arguments.get("provider")
                )
            )
        
        elif name == "generate_script_from_ideas":
            result = await loop.run_in_executor(
                _executor,
                lambda: generate_script_from_ideas(
                    ideas_data=arguments["ideas_data"],
                    duration_seconds=arguments["duration_seconds"],
                    model=arguments.get("model"),
                    style=arguments.get("style", "informative and engaging"),
                    provider=arguments.get("provider")
                )
            )
        
        elif name == "generate_complete_script":
            result = await loop.run_in_executor(
                _executor,
                lambda: generate_complete_script(
                    topic=arguments["topic"],
                    duration_seconds=arguments["duration_seconds"],
                    provider=arguments.get("provider"),
                    style=arguments.get("style", "informative and engaging"),
                    limit=arguments.get("limit", 3),
                    model=arguments.get("model")
                )
            )
        
        else:
            raise ValueError(f"Unknown tool: {name}")
        
        # Return the result as JSON
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, default=str)
        )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({
                "error": str(e),
                "tool": name
            }, indent=2)
        )]


async def main():
    """Run the MCP server."""
    # Check configuration
    missing_configs = config.get_missing_configs()
    if missing_configs:
        print(f"Warning: Missing configuration for: {', '.join(missing_configs)}")
        print("Some tools may not work without proper API keys.")
        print("Please check your .env file or environment variables.\n")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

