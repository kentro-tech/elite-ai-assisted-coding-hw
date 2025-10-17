#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "mcp>=1.17.0",
# ]
# ///

"""
EZ-MCP: A Simple, Complete MCP Server Example

This is a comprehensive example of a Model Context Protocol (MCP) server implemented
using the Anthropic MCP Python SDK. It demonstrates all major MCP functionality:

1. **Resources**: Static and dynamic data sources that provide context to LLMs
2. **Tools**: Functions that LLMs can call to perform actions or computations
3. **Prompts**: Reusable templates for LLM interactions
4. **Server Management**: Proper lifecycle handling and configuration

## How to Run This Server

### Option 1: Direct execution with uv (Recommended)
```bash
uv run ez-mcp.py
```

### Option 2: Development mode with MCP Inspector
```bash
uv run mcp dev ez-mcp.py
```

### Option 3: Install in MCP Client
```bash
uv run mcp install ez-mcp.py
```

## MCP Client Configuration

To use this server with an MCP Client, add this configuration to your
`mcp.json` file:

```json
{
  "mcpServers": {
    "ez-mcp": {
      "command": "uv",
      "args": ["run", "/path/to/ez-mcp.py"],
      "env": {
        "GREETING_PREFIX": "Hello"
      }
    }
  }
}
```

Replace `/path/to/ez-mcp.py` with the actual path to this file.

## How to Modify and Enhance This Server

This server is designed to be easily extensible. Here are common modifications:

### Adding New Tools
```python
@mcp.tool()
def my_new_tool(param1: str, param2: int) -> str:
    "Description of what this tool does"
    # Your implementation here
    return f"Result: {param1} x {param2}"
```

### Adding New Resources
```python
@mcp.resource("my-data://{category}")
def get_my_data(category: str) -> str:
    "Dynamic resource based on category"
    # Your implementation here
    return f"Data for {category}"
```

### Adding New Prompts
```python
@mcp.prompt()
def my_prompt_template(task: str) -> str:
    "Custom prompt template"
    return f"Please help me with: {task}\n\nProvide a detailed response."
```

### Adding Database Integration
```python
from contextlib import asynccontextmanager
import sqlite3

@asynccontextmanager
async def app_lifespan(server):
    # Initialize database connection
    db = sqlite3.connect("data.db")
    try:
        yield {"db": db}
    finally:
        db.close()

# Pass lifespan to server
mcp = FastMCP("Enhanced Server", lifespan=app_lifespan)
```

### Adding External API Integration
```python
import httpx

@mcp.tool()
async def fetch_external_data(url: str) -> str:
    "Fetch data from external API"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text
```

### Environment Variables
Use environment variables for configuration:
```python
import os

API_KEY = os.getenv("API_KEY", "default-key")
DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"
```

### Error Handling
Add proper error handling to your tools:
```python
@mcp.tool()
def safe_division(a: float, b: float) -> float:
    "Safely divide two numbers"
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

### Adding Dependencies
To add new dependencies, modify the script metadata at the top:
```python
# dependencies = [
#   "mcp>=1.17.0",
#   "httpx",      # For HTTP requests
#   "pandas",     # For data manipulation
#   "pillow",     # For image processing
# ]
```

Then run `uv run ez-mcp.py` and uv will automatically install the new dependencies.

## Architecture Notes

- **FastMCP**: High-level server interface that handles protocol details
- **Decorators**: Use @mcp.tool(), @mcp.resource(), @mcp.prompt() to register functions
- **Type Hints**: Use proper type hints for better development experience
- **Async Support**: Tools and resources can be async functions for I/O operations
- **Context Access**: Use the Context parameter to access server capabilities

For more advanced use cases, see the MCP Python SDK documentation at:
https://github.com/modelcontextprotocol/python-sdk
"""

import os
import json
import datetime
import sqlite3
from pathlib import Path
from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP
from contextlib import asynccontextmanager
import sqlite3

# Database path
db_path = Path(__file__).parent / "northwind.db"

# ================================================================================
# DB INTEGRATION WITH LIFESPAN
# ================================================================================

@asynccontextmanager
async def app_lifespan(server):
    # Initialize database connection
    db = sqlite3.connect(db_path)
    try:
        yield {"db": db}
    finally:
        db.close()

# Create the MCP server with lifespan
mcp = FastMCP(
    name="EZ-MCP Demo Server",
    dependencies=["mcp>=1.17.0"],
    lifespan=app_lifespan
)

# ================================================================================
# RESOURCE: Server information
# ================================================================================

@mcp.resource("server://info")
def get_server_info() -> str:
    """Get information about this MCP server"""
    greeting_prefix = os.getenv("GREETING_PREFIX", "Hello")
    info = {
        "name": "EZ-MCP Demo Server",
        "version": "1.0.0",
        "description": "A simple MCP server demonstrating basic functionality",
        "features": ["hello tool", "greeting prompt", "server info resource"],
        "author": "EZ-MCP",
        "status": "running",
        "greeting_prefix": greeting_prefix,
        "sample_greeting": f"{greeting_prefix}, World!"
    }
    return json.dumps(info, indent=2)

@mcp.resource("server://schema")
def get_northwind_schema() -> str:
    """Get the actual schema from the Northwind database"""
    # Get the database path    
    if not db_path.exists():
        return json.dumps({"error": f"Database not found at {db_path}"}, indent=2)
    
    # Connect to the database in read-only mode
    uri = f"file:{db_path}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    
    try:
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' 
            ORDER BY name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        # Build schema dictionary with columns for each table
        schema = {}
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in cursor.fetchall()]  # row[1] is the column name
            schema[table] = columns
        
        return json.dumps(schema, indent=2)
    
    except sqlite3.Error as e:
        return json.dumps({"error": f"Database error: {e}"}, indent=2)
    
    finally:
        conn.close()


# ================================================================================
# TOOL: Hello someone
# ================================================================================
 
@mcp.tool()
def hello_someone(name: str) -> str:
    """Say hello to someone"""
    if not name.strip():
        return "Error: Please provide a name"
    
    name = name.strip()
    greeting_prefix = os.getenv("GREETING_PREFIX", "Hello")
    return f"{greeting_prefix}, {name}! Nice to meet you!"


# ================================================================================
# TOOL: Query Northwind Database
# ================================================================================

@mcp.tool()
def query_northwind(sql_query: str) -> str:
    """Execute a read-only SQL query on the Northwind database.  
    
    Use this tool to explore the database and answer any questions about the data.
    
    Args:
        sql_query: The SQL query to execute (SELECT statements only)
    
    Returns:
        JSON string with query results including columns and rows
    """
    if not db_path.exists():
        return json.dumps({"error": f"Database not found at {db_path}"}, indent=2)
    
    # Basic validation - only allow SELECT statements
    query_upper = sql_query.strip().upper()
    if not query_upper.startswith("SELECT"):
        return json.dumps({
            "error": "Only SELECT queries are allowed for read-only access"
        }, indent=2)
    
    # Connect to the database in read-only mode
    uri = f"file:{db_path}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        
        # Get column names
        columns = [description[0] for description in cursor.description]

        max_rows = 10  # Limit to first 10 rows for safety
        rows = cursor.fetchmany(max_rows)
        
        # Convert to list of dictionaries for easy JSON serialization
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))
        
        return json.dumps({
            "columns": columns,
            "rows": results,
            "row_count": len(results),
            "note": f"Limited to first {max_rows} rows" if len(results) == max_rows else None
        }, indent=2, default=str)
    
    except sqlite3.Error as e:
        return json.dumps({"error": f"Database error: {e}"}, indent=2)
    
    finally:
        conn.close()


# ================================================================================
# PROMPT: Simple greeting template
# ================================================================================

@mcp.prompt()
def get_statistics(sql_query: str) -> str:
    """Generate a statistics report for a SQL query"""
    return f"""Please run and provide information about the following sql query with the `query_northwind` tool:

{sql_query}

The report should include:
- Total number of rows returned
- Column names and their data types
- Sample data from the first few rows"""


# ================================================================================
# DB INTEGRATION WITH LIFESPAN
# ================================================================================

@asynccontextmanager
async def app_lifespan(server):
    # Initialize database connection
    db = sqlite3.connect(db_path)
    try:
        yield {"db": db}
    finally:
        db.close()

# Pass lifespan to server
mcp = FastMCP("Enhanced Server", lifespan=app_lifespan)

# ================================================================================
# SERVER STARTUP
# ================================================================================

def main():
    """Main function to run the server"""
    print("🚀 Starting EZ-MCP Demo Server...")
    print("📖 Simple MCP server with:")
    print("   • 2 Resources: Server info, Northwind schema")
    print("   • 2 Tools: Hello someone, Query Northwind") 
    print("   • 1 Prompt: Greeting template")
    print("")
    print("🔧 Configuration:")
    print(f"   • Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"   • Greeting prefix: {os.getenv('GREETING_PREFIX', 'Welcome')}")
    print("")
    print("📡 Server running on stdio transport...")
    print("   Use 'uv run mcp dev ez-mcp.py' to open the MCP Inspector")
    print("   Or configure this server in your MCP Client")
    print("")
    
    # Run the server
    mcp.run()


if __name__ == "__main__":
    main()