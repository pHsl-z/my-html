#!/usr/bin/env python3
import json
with open('/Volumes/web/my-html/templates-data.js', 'r', encoding='utf-8') as f:
    file_content = f.read()

payload = {
    "owner": "pHsl-z",
    "repo": "my-html",
    "branch": "main",
    "files": [
        {"path": "templates-data.js", "content": file_content}
    ],
    "message": "feat: 在数学练习题模板中添加带SVG图像的初中几何题"
}

print(json.dumps(payload, ensure_ascii=False))
