"""
Simple test to verify MCP server can start and list tools
"""
import os
import asyncio
from oncrawl_mcp_server.server import list_tools

# Set API token for testing
os.environ['ONCRAWL_API_TOKEN'] = '04Q56SGGKZVXAZFKUR9JC0Q5GZCOAY1VA6O05POX'

async def test_tools():
    print("Testing MCP server tools...")
    tools = await list_tools()
    print(f"\nFound {len(tools)} tools:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description[:60]}...")
    print("\n✓ Server test passed!")

if __name__ == "__main__":
    asyncio.run(test_tools())
