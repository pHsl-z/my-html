#!/usr/bin/env python3
import sys
import json

# Read the templates-data.js file
with open('/Volumes/web/my-html/templates-data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Create the payload structure
payload = {
    "owner": "pHsl-z",
    "repo": "my-html",
    "branch": "main",
    "files": [
        {
            "path": "templates-data.js",
            "content": content
        }
    ],
    "message": "feat: 在数学练习题模板中添加带SVG图像的初中几何题"
}

# Output the JSON (but we'll use MCP tool instead)
print(f"File size: {len(content)} bytes")
print("Ready to push via MCP")
