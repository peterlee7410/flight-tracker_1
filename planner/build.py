"""重建旅程產生器：
- planner/index.html        GitHub Pages 版（完整 HTML 文件）
- planner/artifact.html     Claude Artifact 版（不含 <html><head>，發佈時由平台包外框）
用法：python planner/build.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
tpl = (HERE / "src" / "template.html").read_text(encoding="utf-8")
example = (HERE / "src" / "example.json").read_text(encoding="utf-8").replace("</", "<\\/")
body = tpl.replace("__EXAMPLE__", example)
(HERE / "artifact.html").write_text(body, encoding="utf-8")
head = ('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style></head><body>')
(HERE / "index.html").write_text(head + body + "</body></html>", encoding="utf-8")
print("built planner/index.html and planner/artifact.html")
