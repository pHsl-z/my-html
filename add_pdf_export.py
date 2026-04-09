#!/usr/bin/env python3
import re, sys

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# 1. Add PDF export button in the preview dropdown menu
old = '''                            <button class="btn btn-info dropdown-item" onclick="toggleSettingsPanel()" id="settingsBtn">
                                <span class="icon">\u2699\ufe0f</span>
                                \u8bbe\u7f6e
                            </button>
                        </div>'''

new = '''                            <button class="btn btn-info dropdown-item" onclick="toggleSettingsPanel()" id="settingsBtn">
                                <span class="icon">\u2699\ufe0f</span>
                                \u8bbe\u7f6e
                            </button>
                            <button class="btn btn-success dropdown-item" onclick="exportToPdf()" id="pdfBtn">
                                <span class="icon">\ud83d\udcc4</span>
                                \u5bfc\u51faPDF
                            </button>
                        </div>'''

if old in content:
    content = content.replace(old, new)
    changes += 1
    print("OK: Added PDF button to dropdown menu")
else:
    print("ERROR: dropdown menu not found")

# 2. Add PDF button in share panel
old2 = 'onclick="copyAsDataUrl()" style="flex: 1; justify-content: center;">Data URL</button>\n                        </div>'
new2 = 'onclick="copyAsDataUrl()" style="flex: 1; justify-content: center;">Data URL</button>\n                            <button class="btn btn-sm btn-success" onclick="exportToPdf()" style="flex: 1; justify-content: center;">\ud83d\udcc4 PDF</button>\n                        </div>'
if old2 in content:
    content = content.replace(old2, new2)
    changes += 1
    print("OK: Added PDF button to share panel")
else:
    print("ERROR: share panel not found")

# 3. Add exportToPdf function after downloadAsFile
marker = "         function downloadAsFile() {"
idx = content.find(marker)
if idx >= 0:
    brace_count = 0
    end_idx = -1
    for i in range(idx, idx + 2000):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end_idx = i + 1
                break
    if end_idx >= 0:
        pdf_func = '''

         function exportToPdf() {
             const content = htmlEditor.value.trim();
             if (!content) { showToast('\u8bf7\u5148\u8f93\u5165\u5185\u5bb9', 'error'); return; }
             try {
                 const previewDoc = previewFrame.contentDocument || previewFrame.contentWindow.document;
                 if (!previewDoc || !previewDoc.body || !previewDoc.body.innerHTML.trim()) {
                     showToast('\u9884\u89c8\u5185\u5bb9\u4e3a\u7a7a\uff0c\u8bf7\u5148\u8f93\u5165\u5185\u5bb9', 'error');
                     return;
                 }
                 const title = extractTitleFromCode(content) || 'html-page';
                 const pdfFrame = document.createElement('iframe');
                 pdfFrame.style.position = 'fixed';
                 pdfFrame.style.left = '-9999px';
                 pdfFrame.style.top = '-9999px';
                 pdfFrame.style.width = '794px';
                 pdfFrame.style.height = '1123px';
                 document.body.appendChild(pdfFrame);
                 const pdfDoc = pdfFrame.contentDocument;
                 pdfDoc.open();
                 pdfDoc.write('<!DOCTYPE html><html><head><meta charset="UTF-8"><style>@page { size: A4; margin: 15mm 20mm; } body { margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; } * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; } img { max-width: 100% !important; page-break-inside: avoid; } table { page-break-inside: avoid; } h1, h2, h3, h4, h5, h6 { page-break-after: avoid; } p { orphans: 3; widows: 3; }</style></head><body>' + previewDoc.body.innerHTML + '</body></html>');
                 pdfDoc.close();
                 setTimeout(() => {
                     try {
                         pdfFrame.contentWindow.focus();
                         pdfFrame.contentWindow.print();
                         showToast('\u6b63\u5728\u751f\u6210PDF\uff0c\u8bf7\u5728\u6253\u5370\u5bf9\u8bdd\u6846\u4e2d\u9009\u62e9\u201c\u53e6\u5b58\u4e3aPDF\u201d', 'success');
                     } catch (e) {
                         showToast('\u5bfc\u51fa\u5931\u8d25\uff0c\u8bf7\u5c1d\u8bd5\u4f7f\u7528\u6253\u5370\u529f\u80fd', 'error');
                     }
                     setTimeout(() => { document.body.removeChild(pdfFrame); }, 5000);
                 }, 500);
             } catch (error) {
                 printPreview();
                 showToast('\u8bf7\u4f7f\u7528\u6253\u5370\u529f\u80fd\u53e6\u5b58\u4e3aPDF', 'info');
             }
         }'''
        content = content[:end_idx] + pdf_func + content[end_idx:]
        changes += 1
        print("OK: Added exportToPdf function")
    else:
        print("ERROR: could not find end of downloadAsFile")
else:
    print("ERROR: downloadAsFile not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Total changes: {changes}")
