# OnCrawl MCP Server

MCP server that exposes OnCrawl's API for use with Claude Code and Claude Desktop. Designed for exploratory SEO analysis - lets Claude query raw crawl data, build hypotheses, and investigate anomalies.

## Features

- **Raw data access**: Query pages, links, clusters, structured data with flexible OQL
- **Schema discovery**: Claude can learn what fields are available before querying  
- **Aggregations**: Group/count by any dimension for pattern detection
- **Full exports**: No 10k limit when you need complete datasets

## Prerequisites

- Python 3.11+
- OnCrawl account with API access
- OnCrawl API token (from your OnCrawl settings)

## Installation

### 1. Clone/Download

```bash
git clone <this-repo>
cd oncrawl-mcp
```

Or just download the files to a folder.

### 2. Create Virtual Environment

```bash
# Using uv (recommended)
uv venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows

# Or standard Python
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
# Using uv
uv pip install -r requirements.txt

# Or pip
pip install -r requirements.txt
```

### 4. Get Your OnCrawl API Token

1. Log into OnCrawl
2. Go to Settings → API
3. Create a new token with `projects:read` scope
4. Copy the token

### 5. Find Your Workspace ID

Your workspace ID is in the OnCrawl URL when you're logged in:
```
https://app.oncrawl.com/workspaces/{WORKSPACE_ID}/projects
```

## Configuration

### For Claude Code

Add to your Claude Code MCP config:

```bash
claude mcp add oncrawl
```

Then edit the config or add manually:

```json
{
  "mcpServers": {
    "oncrawl": {
      "command": "/FULL/PATH/TO/oncrawl-mcp/.venv/bin/python",
      "args": ["-m", "oncrawl_mcp_server.server"],
      "env": {
        "ONCRAWL_API_TOKEN": "your-api-token-here"
      }
    }
  }
}
```

### For Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (Mac) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "oncrawl": {
      "command": "/FULL/PATH/TO/oncrawl-mcp/.venv/bin/python",
      "args": ["-m", "oncrawl_mcp_server.server"],
      "env": {
        "ONCRAWL_API_TOKEN": "your-api-token-here"
      }
    }
  }
}
```

**Important**: Replace paths with actual full paths on your system.

### Combining with GSC MCP

If you also have the GSC MCP server:

```json
{
  "mcpServers": {
    "oncrawl": {
      "command": "/path/to/oncrawl-mcp/.venv/bin/python",
      "args": ["/path/to/oncrawl-mcp/server.py"],
      "env": {
        "ONCRAWL_API_TOKEN": "your-oncrawl-token"
      }
    },
    "gsc": {
      "command": "/path/to/mcp-gsc/.venv/bin/python",
      "args": ["/path/to/mcp-gsc/gsc_server.py"],
      "env": {
        "GSC_OAUTH_CLIENT_SECRETS_FILE": "/path/to/client_secrets.json"
      }
    }
  }
}
```

## Available Tools

| Tool | Purpose |
|------|---------|
| `oncrawl_list_projects` | List all projects in a workspace |
| `oncrawl_get_project` | Get project details including crawl IDs |
| `oncrawl_get_schema` | **Call first** - discover available fields |
| `oncrawl_search_pages` | Query pages with OQL filtering |
| `oncrawl_search_links` | Query the internal link graph |
| `oncrawl_aggregate` | Group/count by dimensions |
| `oncrawl_export_pages` | Full export without 10k limit |
| `oncrawl_search_clusters` | Find duplicate content clusters |
| `oncrawl_search_structured_data` | Audit schema markup |

## Usage Examples

### Basic Exploration

```
"List my OnCrawl projects in workspace abc123"

"Get the schema for crawl xyz789 - what fields can I query?"

"Show me all pages at depth > 5 with fewer than 3 inlinks"
```

### Detective Work

```
"I want you to act as a senior SEO analyst. Start by understanding the site structure 
for crawl xyz789, then look for anomalies - weird URL patterns, orphan page clusters, 
unusual linking patterns. Investigate anything that seems off."
```

### Combined with GSC

```
"Find all pages in OnCrawl that have zero internal links, then check GSC to see 
if any of them are actually getting impressions. If they are, that's a problem."
```

## OQL Query Reference

### Basic Filters

```json
// Equals
{"field": ["status_code", "equals", 200]}

// Contains
{"field": ["url", "contains", "/blog/"]}

// Starts with
{"field": ["urlpath", "startswith", "/products/"]}

// Less than
{"field": ["depth", "lt", "3"]}

// Has value / no value
{"field": ["canonical", "has_no_value", ""]}
```

### Combining Filters

```json
// AND
{
  "and": [
    {"field": ["status_code", "equals", 200]},
    {"field": ["depth", "gt", "3"]}
  ]
}

// OR
{
  "or": [
    {"field": ["status_code", "equals", 301]},
    {"field": ["status_code", "equals", 404]}
  ]
}
```

### Regex

```json
{"field": ["urlpath", "startswith", "/blog/[0-9]{4}/", {"regex": true}]}
```

## Troubleshooting

### "ONCRAWL_API_TOKEN environment variable required"
- Make sure the token is set in the `env` block of your MCP config
- Restart Claude after changing the config

### API errors
- Check your token has `projects:read` scope
- Verify the workspace/project/crawl IDs are correct
- OnCrawl API has rate limits - slow down if hitting 429s

### Tool not appearing in Claude
- Check the full paths in your config are correct
- Make sure the virtual environment has the dependencies installed
- Check Claude's logs for MCP connection errors

## License

MIT
