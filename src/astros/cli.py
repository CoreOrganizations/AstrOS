"""
AstrOS Command Line Interface
"""
import asyncio
import click
from astros.core.agent import AstrOSAgent


@click.group()
def cli():
    """AstrOS Command Line Interface"""
    pass


@cli.command()
@click.option('--config', default=None, help='Configuration file path')
def agent(config):
    """Start the AstrOS agent"""
    agent = AstrOSAgent(config)
    asyncio.run(agent.run())


@cli.command()
@click.argument('command')
def send(command):
    """Send a command to running AstrOS agent"""
    # This will be implemented when we add IPC
    click.echo(f"Sending command: {command}")
    click.echo("IPC not implemented yet - use 'astros interactive' instead")


@cli.command()
def interactive():
    """Start interactive mode"""
    async def interactive_loop():
        agent = AstrOSAgent()
        await agent.initialize()
        
        print("🚀 AstrOS Interactive Mode - Stage 1")
        print("Available commands: hello, status, help, system info, quit")
        print("Type 'quit' to exit")
        print("-" * 50)
        
        while True:
            try:
                command = input("astros> ")
                if command.lower().strip() in ['quit', 'exit']:
                    break
                
                if not command.strip():
                    continue
                
                response = await agent.process_command(command)
                print(f"Response: {response['message']}")
                print()
                
            except KeyboardInterrupt:
                print("\nShutting down...")
                break
            except Exception as e:
                print(f"Error: {e}")
        
        await agent.shutdown()
        print("AstrOS Agent stopped.")
    
    asyncio.run(interactive_loop())


@cli.command()
def status():
    """Show AstrOS status"""
    print("🚀 AstrOS Status")
    print("================")
    print("Version: 0.1.0 (Stage 1)")
    print("Status: Development")
    print("Components: Core Agent, System Integration")
    print("\nUse 'astros interactive' to start the agent")


def main():
    cli()


if __name__ == "__main__":
    main()