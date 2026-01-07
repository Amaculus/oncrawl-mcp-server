"""
Test OnCrawl API connection with real workspace
"""
import os
import asyncio
from oncrawl_mcp_server.oncrawl_client import OnCrawlClient

# Set API token
os.environ['ONCRAWL_API_TOKEN'] = '04Q56SGGKZVXAZFKUR9JC0Q5GZCOAY1VA6O05POX'

async def test_workspace():
    print("Testing OnCrawl API connection...")

    try:
        client = OnCrawlClient()
        print(f"[OK] Client initialized with token: {client.api_token[:10]}...")

        # Test listing projects
        workspace_id = "5c015889451c956baf7ab7a9"
        print(f"\nFetching projects from workspace: {workspace_id}")

        result = client.list_projects(workspace_id, limit=10)

        if 'projects' in result:
            projects = result['projects']
            print(f"\n[OK] Successfully retrieved {len(projects)} projects:")

            for i, project in enumerate(projects[:5], 1):
                print(f"\n  {i}. {project.get('name', 'Unnamed')}")
                print(f"     ID: {project.get('id')}")
                print(f"     Start URL: {project.get('config', {}).get('start_url', 'N/A')}")

                if 'crawls' in project and project['crawls']:
                    latest_crawl = project['crawls'][0]
                    print(f"     Latest Crawl: {latest_crawl.get('id')}")
                    print(f"     Crawl Date: {latest_crawl.get('date_end', 'N/A')}")

            if len(projects) > 5:
                print(f"\n  ... and {len(projects) - 5} more projects")

            print("\n[OK] MCP server is ready to use!")
            return True
        else:
            print(f"\nUnexpected response format: {result}")
            return False

    except Exception as e:
        print(f"\n[ERROR] {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_workspace())
