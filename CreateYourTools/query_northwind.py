#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
"""
Read-only SQL query tool for northwind.db

Usage:
    uv run query_northwind.py "SELECT * FROM customers LIMIT 5"
    uv run query_northwind.py "SELECT COUNT(*) FROM orders"
"""

import sqlite3
import sys
from pathlib import Path

def execute_readonly_query(db_path: str, query: str):
    """
    Execute a read-only SQL query against the database.

    Args:
        db_path: Path to the SQLite database
        query: SQL query to execute
    """
    # Open database in read-only mode using URI
    uri = f"file:{db_path}?mode=ro"

    try:
        conn = sqlite3.connect(uri, uri=True)
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchmany(10)  # Limit to maximum 10 rows

        if not rows:
            print("Query executed successfully. No results returned.")
            return

        # Get column names
        columns = [description[0] for description in cursor.description]

        # Calculate column widths
        col_widths = [len(col) for col in columns]
        for row in rows:
            for i, value in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(value)))

        # Print header
        header = " | ".join(col.ljust(width) for col, width in zip(columns, col_widths))
        separator = "-+-".join("-" * width for width in col_widths)
        print(header)
        print(separator)

        # Print rows
        for row in rows:
            print(" | ".join(str(value).ljust(width) for value, width in zip(row, col_widths)))

        print(f"\n{len(rows)} row(s) returned")

    except sqlite3.OperationalError as e:
        if "readonly database" in str(e).lower() or "attempt to write" in str(e).lower():
            print(f"Error: Operation not allowed. Database is read-only.", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"Database error: {e}", file=sys.stderr)
            sys.exit(1)
    except sqlite3.Error as e:
        print(f"SQL error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run query_northwind.py \"SQL QUERY\"", file=sys.stderr)
        print("\nExample:")
        print('    uv run query_northwind.py "SELECT * FROM customers LIMIT 5"')
        sys.exit(1)

    # Find the database
    db_path = Path("northwind.db")
    query = sys.argv[1]
    execute_readonly_query(str(db_path.resolve()), query)


if __name__ == "__main__":
    main()
