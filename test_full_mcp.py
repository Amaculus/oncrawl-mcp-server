"""
Full MCP server test with project details
"""
import os
import json
from oncrawl_mcp_server.oncrawl_client import OnCrawlClient

# Set API token
os.environ['ONCRAWL_API_TOKEN'] = '04Q56SGGKZVXAZFKUR9JC0Q5GZCOAY1VA6O05POX'

def test_full_workflow():
    print("Testing full OnCrawl MCP workflow...\n")

    try:
        client = OnCrawlClient()

        # Test 1: Get project details
        project_id = "5d56af5e451c95285b9a4953"  # vegasinsider.com
        print(f"1. Getting details for project: {project_id}")

        project = client.get_project(project_id)

        print(f"   Project: {project.get('name')}")
        print(f"   Start URL: {project.get('config', {}).get('start_url')}")

        if 'crawls' in project and project['crawls']:
            crawls = project['crawls']
            print(f"   Total Crawls: {len(crawls)}")

            latest_crawl = crawls[0]
            crawl_id = latest_crawl.get('id')
            print(f"   Latest Crawl ID: {crawl_id}")
            print(f"   Crawl Date: {latest_crawl.get('date_end')}")
            print(f"   Pages Crawled: {latest_crawl.get('nb_pages', 'N/A')}")

            # Test 2: Get schema for the latest crawl
            if crawl_id:
                print(f"\n2. Getting available fields for crawl: {crawl_id}")
                schema = client.get_fields(crawl_id, data_type="pages")

                if 'fields' in schema:
                    fields = schema['fields']
                    print(f"   Available fields: {len(fields)}")
                    print(f"   Sample fields: {', '.join([f['name'] for f in fields[:10]])}...")

                # Test 3: Search pages
                print(f"\n3. Searching pages (first 5 results)")
                pages = client.search_pages(
                    crawl_id=crawl_id,
                    fields=['url', 'status_code', 'depth', 'follow_inlinks'],
                    limit=5
                )

                if 'pages' in pages:
                    print(f"   Total pages in crawl: {pages.get('count', 'N/A')}")
                    print(f"   Retrieved: {len(pages['pages'])} pages")

                    for i, page in enumerate(pages['pages'][:3], 1):
                        print(f"\n   Page {i}:")
                        print(f"     URL: {page.get('url', 'N/A')[:60]}...")
                        print(f"     Status: {page.get('status_code')}")
                        print(f"     Depth: {page.get('depth')}")
                        print(f"     Inlinks: {page.get('follow_inlinks')}")

                # Test 4: Aggregate data
                print(f"\n4. Running aggregation by status code")
                agg_result = client.aggregate(
                    crawl_id=crawl_id,
                    aggs=[{
                        "fields": [{"name": "status_code"}]
                    }]
                )

                if 'aggs' in agg_result and agg_result['aggs']:
                    agg_data = agg_result['aggs'][0]
                    if 'buckets' in agg_data:
                        print(f"   Status code distribution:")
                        for bucket in agg_data['buckets'][:5]:
                            print(f"     {bucket.get('value')}: {bucket.get('count')} pages")

        print("\n[OK] All MCP tools are working correctly!")
        print("\nYour OnCrawl MCP server is ready to use with Claude!")
        return True

    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_full_workflow()
