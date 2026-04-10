#!/usr/bin/env python3
# -*- coding: utf-8 -*-
with open('index.html', 'r') as f:
    content = f.read()

def remove_function(content, start_marker, max_len=5000):
    idx = content.find(start_marker)
    if idx < 0:
        return content, False
    brace_count = 0
    end_idx = -1
    for i in range(idx, min(idx + max_len, len(content))):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end_idx = i + 1
                break
    if end_idx >= 0:
        return content[:idx] + content[end_idx:], True
    return content, False

changes = 0
content, ok = remove_function(content, '        // 显示GitHub Pages配置对话框\n        function showGitHubPagesConfig()', 5000)
if ok: changes += 1; print('OK: showGitHubPagesConfig removed')
else: print('SKIP: showGitHubPagesConfig not found')

# Also remove share-history CSS that's no longer needed
# And remove shareBaseUrl-related settings if any dead code

with open('index.html', 'w') as f:
    f.write(content)
print(f'Total: {changes} functions removed')
