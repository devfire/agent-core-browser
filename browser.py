from boto3.session import Session
from bedrock_agentcore.tools.browser_client import BrowserClient
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from browser_use import Agent as BrowserUseAgent
from browser_use.browser.session import BrowserSession
from browser_use.browser import BrowserProfile
from browser_use.llm import ChatAnthropicBedrock
# from langchain_aws import ChatBedrockConverse
from rich.console import Console
from contextlib import suppress
import asyncio

from strands import Agent as StrandsAgent, tool
import strands.tools

console = Console()

boto_session = Session()
region = boto_session.region_name

client = BrowserClient(region)
client.start()

# Extract ws_url and headers
ws_url, headers = client.generate_ws_headers()

app = BedrockAgentCoreApp()

@tool
async def run_browser_task(browser_session: BrowserSession, bedrock_chat: ChatAnthropicBedrock, task: str) -> None:
    """
    Run a browser automation task using browser_use

    Args:
        browser_session: Existing browser session to reuse
        bedrock_chat: Bedrock chat model instance
        task: Natural language task for the agent
    """
    try:
        # Show task execution
        console.print(f"\n[bold blue]🤖 Executing task:[/bold blue] {task}")

        # Create and run the agent
        browser_use_agent = BrowserUseAgent(
            task=task,
            llm=bedrock_chat,
            browser_session=browser_session
        )

        # Run with progress indicator
        with console.status("[bold green]Running browser automation...[/bold green]", spinner="dots"):
            await browser_use_agent.run()

        console.print(
            "[bold green]✅ Task completed successfully![/bold green]")

    except Exception as e:
        console.print(
            f"[bold red]❌ Error during task execution:[/bold red] {str(e)}")
        import traceback
        if console.is_terminal:
            traceback.print_exc()


async def run_strands_task(task: str):
    """
    Run a strands agent task
    """
    console.print(f"\n[bold blue]🤖 Executing Strands task:[/bold blue] {task}")
    strands_agent = StrandsAgent(
        model="us.anthropic.claude-sonnet-4-20250514-v1:0",
        tools=[calculator, current_time, run_browser_task],
        system_prompt="You are a helpful assistant."
    )
    # Run the synchronous agent call in a separate thread
    response = await asyncio.to_thread(strands_agent, task)
    console.print(
        "[bold green]✅ Strands Task completed successfully![/bold green]")
    console.print(f"[bold cyan]Response:[/bold cyan] {response.message}")


async def main():
    """
    Main function to initialize and run the browser task
    """
    # Create persistent browser session and model
    browser_session = None

    try:
        # Create browser profile with headers
        browser_profile = BrowserProfile(
            headers=headers,
            timeout=1500000,  # 150 seconds timeout
        )

        # Create a browser session with CDP URL and keep_alive=True for persistence
        browser_session = BrowserSession(
            cdp_url=ws_url,
            browser_profile=browser_profile,
            keep_alive=True  # Keep browser alive between tasks
        )

        # Initialize the browser session
        console.print("[cyan]🔄 Initializing browser session...[/cyan]")
        await browser_session.start()

        llm = ChatAnthropicBedrock(
            model="us.anthropic.claude-sonnet-4-20250514-v1:0",
            aws_region='us-east-1'  # Use the region from boto3 session
        )
        console.print(
            "[green]✅ Browser session initialized and ready for tasks[/green]\n")

        # Modify the task to run other tasks
        task = "Search for a coffee maker on amazon.com and extract details of the first one"

        await run_browser_task(browser_session, llm, task)

        strands_task = "What is the current time and what is 24 * 7?"
        await run_strands_task(strands_task)

    finally:
        # Close the browser session
        if browser_session:
            console.print("\n[yellow]🔌 Closing browser session...[/yellow]")
            with suppress(Exception):
                await browser_session.close()
            console.print("[green]✅ Browser session closed[/green]")

    client.stop()  # Stop the browser client
    console.print("[green]✅ Browser client stopped[/green]")

if __name__ == "__main__":
    # Run the main function with asyncio
    asyncio.run(main())
