#!/usr/bin/env python3
"""Build notes.html from Obsidian markdown theory notes."""
import re, json

VAULT = '/Users/hyunwoo/Documents/FirstBrain/20_Resources/Studies/경영정보시각화'
FILES = [
    ('과목1: 경영정보 일반', f'{VAULT}/필기 - 경영정보 일반.md'),
    ('과목2: 데이터 해석 및 활용', f'{VAULT}/필기 - 데이터 해석 및 활용.md'),
    ('과목3: 경영정보시각화 디자인', f'{VAULT}/필기 - 경영정보시각화 디자인.md'),
]

def strip_frontmatter(text):
    """Remove YAML frontmatter."""
    if text.startswith('---'):
        end = text.find('---', 3)
        if end != -1:
            text = text[end+3:].strip()
    return text

def strip_obsidian(text):
    """Remove Obsidian-specific syntax."""
    # Remove wikilinks: [[text|display]] → display, [[text]] → text
    text = re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', r'\2', text)
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)
    # Remove callout syntax but keep content
    text = re.sub(r'> \[!(tip|note|warning|info|quote|success)\][^\n]*\n', '', text)
    # Remove highlight ==text==
    text = re.sub(r'==([^=]+)==', r'\1', text)
    # Remove mermaid blocks (not renderable)
    text = re.sub(r'```mermaid\n.*?```', '', text, flags=re.DOTALL)
    return text

subjects = []
for title, path in FILES:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = strip_frontmatter(content)
    content = strip_obsidian(content)
    subjects.append((title, content))

# Escape for JS embedding
def js_escape(s):
    return json.dumps(s, ensure_ascii=False)

tabs_html = ''
for i, (title, _) in enumerate(subjects):
    active = ' active' if i == 0 else ''
    tabs_html += f'<div class="tab{active}" onclick="switchTab({i})">{title}</div>\n'

subjects_js = ',\n'.join(f'{{{json.dumps(t[0], ensure_ascii=False)}: {json.dumps(t[1], ensure_ascii=False)}}}' for t in subjects)

html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>경영정보시각화 이론 정리</title>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
:root {{
  --primary: #4F46E5; --primary-light: #818CF8; --bg: #F9FAFB; --card: #fff;
  --text: #111827; --text-light: #6B7280; --border: #E5E7EB;
  --radius: 12px; --shadow: 0 1px 3px rgba(0,0,0,.1);
}}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  background: var(--bg); color: var(--text); line-height: 1.7; }}
.container {{ max-width: 800px; margin: 0 auto; padding: 16px; }}
.header {{ text-align: center; padding: 20px 0 8px; }}
.header h1 {{ font-size: 1.5rem; font-weight: 700; }}
.header .subtitle {{ color: var(--text-light); font-size: .9rem; margin: 4px 0 16px; }}
.back-link {{ display: inline-flex; align-items: center; gap: 4px; color: var(--primary);
  font-weight: 600; text-decoration: none; font-size: .95rem; margin-bottom: 16px; }}
.back-link:hover {{ text-decoration: underline; }}

/* Tabs */
.tabs {{ display: flex; gap: 0; border-bottom: 2px solid var(--border); margin-bottom: 24px; overflow-x: auto; }}
.tab {{ padding: 12px 16px; cursor: pointer; font-weight: 600; font-size: .9rem;
  color: var(--text-light); border-bottom: 3px solid transparent; margin-bottom: -2px;
  white-space: nowrap; transition: all .15s; }}
.tab:hover {{ color: var(--text); }}
.tab.active {{ color: var(--primary); border-bottom-color: var(--primary); }}

/* Markdown content */
.content {{ background: var(--card); border-radius: var(--radius); padding: 24px; box-shadow: var(--shadow); }}
.content h1 {{ font-size: 1.4rem; font-weight: 700; margin: 24px 0 12px; padding-bottom: 8px; border-bottom: 2px solid var(--border); }}
.content h2 {{ font-size: 1.2rem; font-weight: 700; margin: 28px 0 12px; color: var(--primary); }}
.content h3 {{ font-size: 1.05rem; font-weight: 600; margin: 20px 0 8px; }}
.content h4 {{ font-size: .95rem; font-weight: 600; margin: 16px 0 6px; }}
.content p {{ margin: 8px 0; }}
.content ul, .content ol {{ margin: 8px 0 8px 20px; }}
.content li {{ margin: 4px 0; }}
.content table {{ width: 100%; border-collapse: collapse; margin: 12px 0; font-size: .9rem; }}
.content th {{ background: #F3F4F6; font-weight: 600; text-align: left; padding: 10px 12px; border: 1px solid var(--border); }}
.content td {{ padding: 8px 12px; border: 1px solid var(--border); }}
.content tr:hover {{ background: #F9FAFB; }}
.content blockquote {{ border-left: 3px solid var(--primary-light); padding: 8px 16px; margin: 12px 0;
  background: #EEF2FF; border-radius: 0 8px 8px 0; }}
.content code {{ background: #F3F4F6; padding: 2px 6px; border-radius: 4px; font-size: .85rem; }}
.content pre {{ background: #1F2937; color: #F9FAFB; padding: 16px; border-radius: 8px; overflow-x: auto; margin: 12px 0; }}
.content pre code {{ background: transparent; padding: 0; color: inherit; }}
.content strong {{ color: #1F2937; }}
.content hr {{ border: none; border-top: 1px solid var(--border); margin: 24px 0; }}

/* Responsive */
@media (max-width: 480px) {{
  .container {{ padding: 12px; }}
  .content {{ padding: 16px; }}
  .tab {{ padding: 10px 12px; font-size: .8rem; }}
  .content table {{ font-size: .8rem; }}
  .content th, .content td {{ padding: 6px 8px; }}
}}
</style>
</head>
<body>
<div class="container">
  <a href="index.html" class="back-link">← 퀴즈 풀기</a>
  <div class="header">
    <h1>📚 경영정보시각화 이론 정리</h1>
    <p class="subtitle">3과목 핵심 개념 · 빈출 키워드 · 기출 포인트</p>
  </div>

  <div class="tabs" id="tabs">
    {tabs_html}
  </div>

  <div class="content" id="content"></div>
</div>

<script>
const SUBJECTS = [
  {js_escape(subjects[0][1])},
  {js_escape(subjects[1][1])},
  {js_escape(subjects[2][1])}
];

let currentTab = 0;

function switchTab(idx) {{
  currentTab = idx;
  document.querySelectorAll('.tab').forEach((t, i) => {{
    t.classList.toggle('active', i === idx);
  }});
  renderContent();
}}

function renderContent() {{
  const md = SUBJECTS[currentTab];
  document.getElementById('content').innerHTML = marked.parse(md);
  window.scrollTo({{ top: 0 }});
}}

// Initial render
renderContent();
</script>
</body>
</html>'''

with open('notes.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'notes.html generated ({len(html):,} bytes)')
