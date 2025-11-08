"""
Simple example of using the Content Creation Agent without AgentOS UI.
Run this for quick tests and experiments.
"""

import sys
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load environment variables from parent directory's .env file
env_path = PROJECT_ROOT / ".env"
load_dotenv(env_path)

from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.openrouter import OpenRouter
from agno.tools.mcp import MCPTools


async def create_agent():
    """Create a content creation agent with properly connected MCP tools."""
    # Use the launcher script
    launcher_script = Path(__file__).parent / "launch_mcp.sh"
    
    # Initialize MCP tools
    mcp_tools = MCPTools(
        transport="stdio",
        command=str(launcher_script)
    )
    
    # Connect to MCP server (this is critical!)
    print("🔌 Connecting to MCP server...")
    await mcp_tools.connect()
    print("✅ MCP server connected!")
    
    # Increase timeout for long-running operations like audio generation
    if hasattr(mcp_tools, 'timeout'):
        mcp_tools.timeout = 120
    elif hasattr(mcp_tools, 'session') and hasattr(mcp_tools.session, 'timeout'):
        mcp_tools.session.timeout = 120
    
    # Print available tools for debugging
    if hasattr(mcp_tools, 'functions'):
        funcs = list(mcp_tools.functions) if hasattr(mcp_tools.functions, '__iter__') else []
        print(f"📦 Available MCP tools: {len(funcs)} tools loaded")
        if funcs:
            func_names = [f.replace('_', '', 1) for f in funcs[:5]]
            print(f"   Tools: {', '.join(func_names)}...")
    
    # Try to use OpenRouter first, fall back to Groq if needed
    try:
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        if not openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY not set")
        
        print("🚀 Using OpenRouter for inference (primary)")
        model = OpenRouter(
            id="openai/gpt-4o-mini",  # Known working model - cheap and reliable
            api_key=openrouter_api_key
        )
    except Exception as e:
        print(f"⚠️  OpenRouter unavailable ({str(e)}), falling back to Groq")
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("Neither OPENROUTER_API_KEY nor GROQ_API_KEY is set. Please set at least one.")
        
        print("🚀 Using Groq for inference (backup)")
        model = Groq(id="openai/gpt-oss-20b")
    
    agent = Agent(
        name="Content Creator",
        model=model,
        tools=[mcp_tools],
        markdown=True,
        description="Content creation assistant with trending topic research and voice generation",
        instructions=[
            "ALWAYS use the available MCP tools to answer questions - never make up information",
            "When asked about voices, use the list_all_voices tool to get actual voices from ElevenLabs",
            "When asked about trending topics, use generate_ideas or source-specific tools (generate_reddit_ideas, generate_youtube_ideas, generate_news_ideas)",
            "When asked to create content, use the appropriate generate_complete_content or generate_script tools",
            "Show the user what tools you're using and what data you're getting from them",
            "If a tool returns data, present it to the user clearly"
        ]
    )
    
    return agent, mcp_tools


async def example_1_trending_topics():
    """Example: Get trending topics on a subject."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Research Trending Topics")
    print("="*70 + "\n")
    
    agent, mcp_tools = await create_agent()
    try:
        response = await agent.arun(
            "What are the top 3 trending topics about artificial intelligence on Reddit?"
        )
        print(response.content)
    finally:
        await mcp_tools.close()


async def example_2_generate_script():
    """Example: Generate a script about a topic."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Generate a Script")
    print("="*70 + "\n")
    
    agent, mcp_tools = await create_agent()
    try:
        response = await agent.arun(
            "Create a 30-second script about the latest trends in artificial intelligence. "
            "Research trending topics first, then write an engaging script."
        )
        print(response.content)
    finally:
        await mcp_tools.close()


async def example_3_list_voices():
    """Example: List available voices."""
    print("\n" + "="*70)
    print("EXAMPLE 3: List Available Voices")
    print("="*70 + "\n")
    
    agent, mcp_tools = await create_agent()
    try:
        response = await agent.arun(
            "List all the voices available in my ElevenLabs account."
        )
        print(response.content)
    finally:
        await mcp_tools.close()


async def example_4_complete_workflow():
    """Example: Complete content creation workflow."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Complete Content Creation Workflow")
    print("="*70 + "\n")
    
    agent, mcp_tools = await create_agent()
    try:
        response = await agent.arun(
            "Create a complete content piece about 'AI trends': "
            "1. Research trending topics "
            "2. Generate a 20-second script "
            "3. List available voices so I can choose one"
        )
        print(response.content)
    finally:
        await mcp_tools.close()


async def interactive_mode():
    """Interactive chat mode with the agent."""
    print("\n" + "="*70)
    print("INTERACTIVE MODE - Content Creation Agent")
    print("="*70)
    print("\nCommands:")
    print("  • Type your request and press Enter")
    print("  • Type 'quit' or 'exit' to end")
    print("  • Type 'clear' to start a new conversation")
    print("\nExamples:")
    print("  - 'Research trending AI topics'")
    print("  - 'Generate a 30-second script about machine learning'")
    print("  - 'List my available voices'")
    print("  - 'Create content about climate change with my narrator voice'")
    print("="*70 + "\n")
    
    agent, mcp_tools = await create_agent()
    
    try:
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit']:
                    print("\n👋 Goodbye!")
                    break
                
                if user_input.lower() == 'clear':
                    await mcp_tools.close()
                    agent, mcp_tools = await create_agent()  # Create fresh agent
                    print("\n🔄 Conversation cleared. Starting fresh!\n")
                    continue
                
                print("\n🤖 Agent: ", end="", flush=True)
                response = await agent.arun(user_input)
                
                # Check if response is empty
                if hasattr(response, 'content'):
                    content = str(response.content).strip()
                    if not content:
                        print("(empty response - possible API issue or model not responding)\n")
                    else:
                        print(content + "\n")
                else:
                    print(str(response) + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")
    finally:
        await mcp_tools.close()


async def main():
    """Main menu for examples."""
    print("\n" + "="*70)
    print("CONTENT CREATION AGENT - EXAMPLES")
    print("="*70)
    print("\nChoose an example to run:")
    print("  1. Get trending topics about AI")
    print("  2. Generate a script")
    print("  3. List available voices")
    print("  4. Complete content creation workflow")
    print("  5. Interactive mode (chat with agent)")
    print("  0. Exit")
    print("="*70)
    
    while True:
        try:
            choice = input("\nEnter choice (0-5): ").strip()
            
            if choice == '0':
                print("\n👋 Goodbye!")
                break
            elif choice == '1':
                await example_1_trending_topics()
            elif choice == '2':
                await example_2_generate_script()
            elif choice == '3':
                await example_3_list_voices()
            elif choice == '4':
                await example_4_complete_workflow()
            elif choice == '5':
                await interactive_mode()
            else:
                print("❌ Invalid choice. Please enter 0-5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())

