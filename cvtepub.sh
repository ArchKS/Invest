#!/usr/bin/env bash
set -euo pipefail
# ./cvtepub.sh --table-as-svg  ./医药/亚盛/ -o 亚盛.epub

usage() {
  cat <<'EOF'
Usage:
  cvtepub [options] SOURCE_DIR [OUTPUT.epub|OUTPUT.azw3|OUTPUT.pdf]

Convert Markdown and HTML files under SOURCE_DIR into one ebook/document.

Options:
  -o, --output FILE     Output path (.epub, .azw3, or .pdf)
  -t, --title TITLE     Book title (default: source directory name)
  --table-as-svg        Render Markdown pipe tables as SVG images
  --keep-build          Keep the temporary build directory and print its path
  -h, --help            Show this help

Rules:
  - First-level directories become H1, second-level directories become H2, etc.
  - File names also become headings one level below their containing directory.
  - Markdown/HTML headings inside files are shifted below the file-name heading.
    Example: SOURCE_DIR/一级目录/a.md "# Title" becomes "### Title".
  - Relative images/media referenced by Markdown or HTML are resolved from their
    original file directories where possible.
EOF
}

die() {
  printf 'cvtepub: %s\n' "$*" >&2
  exit 1
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "missing dependency: $1"
}

find_ebook_convert() {
  if command -v ebook-convert >/dev/null 2>&1; then
    command -v ebook-convert
    return 0
  fi
  if [ -x /Applications/Calibre.app/Contents/MacOS/ebook-convert ]; then
    printf '%s\n' /Applications/Calibre.app/Contents/MacOS/ebook-convert
    return 0
  fi
  return 1
}

find_chrome() {
  for cmd in google-chrome chrome chromium chromium-browser; do
    if command -v "$cmd" >/dev/null 2>&1; then
      command -v "$cmd"
      return 0
    fi
  done
  for app in \
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "/Applications/Chromium.app/Contents/MacOS/Chromium" \
    "$HOME/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "$HOME/Applications/Chromium.app/Contents/MacOS/Chromium"
  do
    if [ -x "$app" ]; then
      printf '%s\n' "$app"
      return 0
    fi
  done
  return 1
}

title=""
output=""
keep_build=0
table_as_svg=0
args=()

while [ "$#" -gt 0 ]; do
  case "$1" in
    -o|--output)
      [ "$#" -ge 2 ] || die "$1 requires a value"
      output=$2
      shift 2
      ;;
    -t|--title)
      [ "$#" -ge 2 ] || die "$1 requires a value"
      title=$2
      shift 2
      ;;
    --keep-build)
      keep_build=1
      shift
      ;;
    --table-as-svg)
      table_as_svg=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      while [ "$#" -gt 0 ]; do
        args+=("$1")
        shift
      done
      ;;
    -*)
      die "unknown option: $1"
      ;;
    *)
      args+=("$1")
      shift
      ;;
  esac
done

[ "${#args[@]}" -ge 1 ] || { usage >&2; exit 2; }
[ "${#args[@]}" -le 2 ] || die "too many positional arguments"

src=${args[0]}
[ -d "$src" ] || die "source is not a directory: $src"

if [ -n "${args[1]:-}" ]; then
  [ -z "$output" ] || die "set output either as positional argument or --output, not both"
  output=${args[1]}
fi

need_cmd python3
need_cmd pandoc

src_abs=$(python3 -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$src")
book_name=$(basename "$src_abs")
[ -n "$title" ] || title=$book_name

if [ -z "$output" ]; then
  output="$(pwd)/${book_name}.epub"
else
  output=$(python3 -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$output")
fi

output_ext=${output##*.}
output_ext=$(printf '%s' "$output_ext" | tr '[:upper:]' '[:lower:]')
case "$output_ext" in
  epub|azw3|pdf) ;;
  *) die "unsupported output format: .$output_ext (supported: .epub, .azw3, .pdf)" ;;
esac

final_output=$output

build_dir=$(mktemp -d "${TMPDIR:-/tmp}/cvtepub.XXXXXX")
if [ "$keep_build" -eq 0 ]; then
  trap 'rm -rf "$build_dir"' EXIT
fi

if [ "$output_ext" = "azw3" ]; then
  ebook_convert=$(find_ebook_convert) || die "missing dependency for AZW3 output: ebook-convert (install Calibre: brew install --cask calibre)"
  output="$build_dir/${book_name}.epub"
elif [ "$output_ext" = "pdf" ]; then
  chrome_bin=$(find_chrome) || die "missing dependency for PDF output: Chrome or Chromium (install Chrome, or run: brew install --cask google-chrome)"
fi

book_md="$build_dir/book.md"
meta_yaml="$build_dir/metadata.yml"
epub_css="$build_dir/epub.css"
resource_paths="$build_dir/resource-paths.txt"
table_svg_dir="$build_dir/table-svg"

python3 - "$src_abs" "$title" "$book_md" "$meta_yaml" "$resource_paths" "$table_as_svg" "$table_svg_dir" <<'PY'
import html
import os
import re
import subprocess
import sys
import unicodedata

src, title, book_md, meta_yaml, resource_paths_file, table_as_svg, table_svg_dir = sys.argv[1:8]
table_as_svg = table_as_svg == "1"
TEXT_EXTS = {".md", ".markdown", ".html", ".htm"}
SKIP_DIRS = {".git", ".hg", ".svn", "node_modules", "__pycache__"}
SKIP_FILES = {".DS_Store"}
table_svg_count = 0

def sort_key(name):
    return [int(p) if p.isdigit() else unicodedata.normalize("NFKD", p).casefold()
            for p in re.split(r"(\d+)", name)]

def is_text_file(name):
    return os.path.splitext(name)[1].lower() in TEXT_EXTS and name not in SKIP_FILES

def visible_dir(name):
    return name not in SKIP_DIRS and not name.startswith(".")

def visible_file(name):
    return name not in SKIP_FILES and not name.startswith(".")

def rel_parts(path):
    rel = os.path.relpath(path, src)
    if rel == ".":
        return []
    return rel.split(os.sep)

def contains_text(path):
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if visible_dir(d)]
        if any(visible_file(f) and is_text_file(f) for f in files):
            return True
    return False

def esc_heading(text):
    return text.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")

def title_from_file(path):
    return os.path.splitext(os.path.basename(path))[0]

def shift_markdown_headings(text, offset):
    if offset <= 0:
        return text

    out = []
    lines = text.splitlines()
    in_fence = False
    fence_re = re.compile(r"^ {0,3}(```+|~~~+)")
    atx_re = re.compile(r"^( {0,3})(#{1,6})([ \t]+.*)$")

    i = 0
    while i < len(lines):
        line = lines[i]
        if fence_re.match(line):
            in_fence = not in_fence
            out.append(line)
            i += 1
            continue

        if not in_fence:
            m = atx_re.match(line)
            if m:
                level = min(6, len(m.group(2)) + offset)
                out.append(f"{m.group(1)}{'#' * level}{m.group(3)}")
                i += 1
                continue

            if i + 1 < len(lines) and line.strip() and re.match(r"^ {0,3}(=+|-+)\s*$", lines[i + 1]):
                level = 1 if lines[i + 1].lstrip().startswith("=") else 2
                level = min(6, level + offset)
                out.append(f"{'#' * level} {line.strip()}")
                i += 2
                continue

        out.append(line)
        i += 1

    return "\n".join(out) + ("\n" if text.endswith("\n") else "")

def strip_front_matter(text):
    lines = text.splitlines(True)
    if not lines or lines[0].strip() not in {"---", "..."}:
        return text
    for i in range(1, min(len(lines), 200)):
        if lines[i].strip() in {"---", "..."}:
            return "".join(lines[i + 1:]).lstrip("\n")
    return text

def rewrite_markdown_media(text, file_dir):
    def repl_md(m):
        bang, label, target = m.group(1), m.group(2), m.group(3).strip()
        if bang != "!":
            return m.group(0)
        new_target = normalize_target(target, file_dir)
        return f"![{label}]({new_target})"

    def repl_html(m):
        attr, quote, target = m.group(1), m.group(2), m.group(3)
        return f'{attr}{quote}{normalize_target(target, file_dir)}{quote}'

    text = re.sub(r"(!?)\[([^\]]*)\]\(([^)]+)\)", repl_md, text)
    return re.sub(r"((?:src|poster)\s*=\s*)(['\"])([^'\"]+)\2", repl_html, text, flags=re.I)

def namespace_footnotes(text, prefix):
    def_pat = re.compile(r"(^[ \t]{0,3})\[\^([^\]\n]+)\]:", re.M)
    ref_pat = re.compile(r"\[\^([^\]\n]+)\](?!:)")
    labels = {}
    def_seen = {}
    ref_seen = {}

    for m in def_pat.finditer(text):
        label = m.group(2)
        labels.setdefault(label, [])
        labels[label].append(f"{prefix}{label}-{len(labels[label]) + 1}")

    if not labels:
        return text

    def rewrite_def(m):
        label = m.group(2)
        def_seen[label] = def_seen.get(label, 0) + 1
        return f"{m.group(1)}[^{labels[label][def_seen[label] - 1]}]:"

    def rewrite_ref(m):
        label = m.group(1)
        if label.startswith(prefix) or label not in labels:
            return m.group(0)
        ref_seen[label] = ref_seen.get(label, 0) + 1
        idx = min(ref_seen[label] - 1, len(labels[label]) - 1)
        return f"[^{labels[label][idx]}]"

    text = def_pat.sub(rewrite_def, text)
    return ref_pat.sub(rewrite_ref, text)

def normalize_tex_command_spacing(text):
    math_commands = (
        "to", "times", "approx", "cdot", "le", "ge", "lt", "gt",
        "sim", "in", "notin", "subset", "supset", "rightarrow",
        "leftarrow", "Rightarrow", "Leftarrow",
    )
    pattern = r"\\(" + "|".join(re.escape(cmd) for cmd in math_commands) + r")(?=[^\s\\{}_^$])"
    return re.sub(pattern, r"\\\1 ", text)

def display_width(text):
    width = 0
    for ch in text:
        width += 2 if unicodedata.east_asian_width(ch) in {"F", "W"} else 1
    return width

def split_pipe_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]

    cells = []
    cur = []
    escaped = False
    for ch in line:
        if escaped:
            cur.append(ch)
            escaped = False
        elif ch == "\\":
            cur.append(ch)
            escaped = True
        elif ch == "|":
            cells.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    cells.append("".join(cur).strip())
    return cells

def is_pipe_table_separator(line):
    if "|" not in line:
        return False
    cells = split_pipe_row(line)
    return bool(cells) and all(re.match(r"^:?-{3,}:?$", c.strip()) for c in cells)

def clean_table_cell(text):
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"[*_~]{1,3}", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()

def wrap_display_text(text, limit):
    text = clean_table_cell(text)
    if not text:
        return [""]
    lines = []
    for raw_line in text.splitlines():
        raw_line = raw_line.strip()
        if not raw_line:
            lines.append("")
            continue
        cur = ""
        cur_width = 0
        for ch in raw_line:
            ch_width = display_width(ch)
            if cur and cur_width + ch_width > limit:
                lines.append(cur)
                cur = ch
                cur_width = ch_width
            else:
                cur += ch
                cur_width += ch_width
        if cur:
            lines.append(cur)
    return lines or [""]

def svg_text_lines(text_lines, x, y, font_size, line_height, weight="400"):
    out = []
    for idx, line in enumerate(text_lines):
        out.append(
            f'<text x="{x}" y="{y + idx * line_height}" '
            f'font-size="{font_size}" font-weight="{weight}" '
            f'font-family="-apple-system,BlinkMacSystemFont,PingFang SC,Hiragino Sans GB,Microsoft YaHei,sans-serif" '
            f'fill="#111">{html.escape(line)}</text>'
        )
    return "\n".join(out)

def render_table_svg(rows):
    global table_svg_count
    table_svg_count += 1
    os.makedirs(table_svg_dir, exist_ok=True)

    max_cols = max(len(row) for row in rows)
    rows = [row + [""] * (max_cols - len(row)) for row in rows]
    font_size = 14
    line_height = 20
    pad_x = 10
    pad_y = 9
    min_col = 8
    max_col = 24
    char_px = 8

    col_units = []
    for col in range(max_cols):
        values = [clean_table_cell(row[col]) for row in rows]
        longest = max([display_width(v) for v in values] + [min_col])
        col_units.append(max(min_col, min(max_col, longest)))

    col_widths = [units * char_px + pad_x * 2 for units in col_units]
    wrapped = []
    row_heights = []
    for row in rows:
        wrapped_row = []
        max_lines = 1
        for col, cell in enumerate(row):
            lines = wrap_display_text(cell, col_units[col])
            wrapped_row.append(lines)
            max_lines = max(max_lines, len(lines))
        wrapped.append(wrapped_row)
        row_heights.append(max_lines * line_height + pad_y * 2)

    width = sum(col_widths) + 1
    height = sum(row_heights) + 1
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]

    y = 0
    for r, row in enumerate(wrapped):
        x = 0
        bg = "#f6f8fa" if r == 0 else ("#fbfbfb" if r % 2 == 0 else "#fff")
        for c, lines in enumerate(row):
            w = col_widths[c]
            h = row_heights[r]
            parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}" stroke="#d0d7de"/>')
            parts.append(svg_text_lines(lines, x + pad_x, y + pad_y + font_size, font_size, line_height, "600" if r == 0 else "400"))
            x += w
        y += row_heights[r]
    parts.append("</svg>")

    name = f"table-{table_svg_count:05d}.svg"
    path = os.path.join(table_svg_dir, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    return f"![](table-svg/{name})"

def pipe_tables_to_svg(text):
    if not table_as_svg:
        return text

    out = []
    lines = text.splitlines()
    in_fence = False
    fence_re = re.compile(r"^ {0,3}(```+|~~~+)")
    i = 0
    while i < len(lines):
        line = lines[i]
        if fence_re.match(line):
            in_fence = not in_fence
            out.append(line)
            i += 1
            continue

        if not in_fence and i + 1 < len(lines) and "|" in line and is_pipe_table_separator(lines[i + 1]):
            table_lines = [line, lines[i + 1]]
            i += 2
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                table_lines.append(lines[i])
                i += 1
            rows = [split_pipe_row(table_lines[0])] + [split_pipe_row(row) for row in table_lines[2:]]
            out.append(render_table_svg(rows))
            continue

        out.append(line)
        i += 1

    return "\n".join(out) + ("\n" if text.endswith("\n") else "")

def normalize_target(target, file_dir):
    raw = target.strip()
    if not raw or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", raw) or raw.startswith("#"):
        return target
    if raw.startswith("<") and raw.endswith(">"):
        raw = raw[1:-1]
        wrapped = True
    else:
        wrapped = False
    if raw.startswith("/"):
        return target

    path_part, suffix = raw, ""
    for sep in ("#", "?"):
        if sep in path_part:
            path_part, rest = path_part.split(sep, 1)
            suffix = sep + rest
            break

    abs_target = os.path.normpath(os.path.join(file_dir, path_part))
    if not os.path.exists(abs_target):
        return target
    rel = os.path.relpath(abs_target, src).replace(os.sep, "/")
    out = rel + suffix
    return f"<{out}>" if wrapped or any(c.isspace() for c in out) else out

def yaml_quote(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'

def html_to_markdown(path):
    result = subprocess.run(
        ["pandoc", "--from", "html", "--to", "markdown+pipe_tables+grid_tables+multiline_tables+raw_html", "--wrap=none", path],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout

resource_paths = {src, os.path.dirname(book_md)}
file_index = 0
with open(book_md, "w", encoding="utf-8") as out:
    for root, dirs, files in os.walk(src):
        dirs[:] = sorted([d for d in dirs if visible_dir(d)], key=sort_key)
        files = sorted([f for f in files if visible_file(f) and is_text_file(f)], key=sort_key)

        parts = rel_parts(root)
        if parts and (files or any(contains_text(os.path.join(root, d)) for d in dirs)):
            level = min(6, len(parts))
            out.write(f"\n\n{'#' * level} {esc_heading(parts[-1])}\n\n")

        for name in files:
            path = os.path.join(root, name)
            file_index += 1
            footnote_prefix = f"cvtepub-{file_index}-"
            ext = os.path.splitext(name)[1].lower()
            dir_depth = len(parts)
            file_heading_level = min(6, dir_depth + 1)
            content_heading_offset = dir_depth + 1
            resource_paths.add(root)

            if ext in {".html", ".htm"}:
                text = html_to_markdown(path)
                text = rewrite_markdown_media(text, root)
                text = namespace_footnotes(text, footnote_prefix)
                text = normalize_tex_command_spacing(text)
                text = pipe_tables_to_svg(text)
                out.write(f"\n\n{'#' * file_heading_level} {esc_heading(title_from_file(path))}\n\n")
                out.write(f"\n\n<!-- cvtepub-file: {os.path.relpath(path, src)} -->\n\n")
                out.write(shift_markdown_headings(text, content_heading_offset))
                out.write("\n")
                continue

            with open(path, "r", encoding="utf-8", errors="replace") as f:
                text = f.read()
            text = strip_front_matter(text)
            text = rewrite_markdown_media(text, root)
            text = namespace_footnotes(text, footnote_prefix)
            text = normalize_tex_command_spacing(text)
            text = pipe_tables_to_svg(text)
            out.write(f"\n\n{'#' * file_heading_level} {esc_heading(title_from_file(path))}\n\n")
            out.write(f"\n\n<!-- cvtepub-file: {os.path.relpath(path, src)} -->\n\n")
            out.write(shift_markdown_headings(text, content_heading_offset))
            out.write("\n")

with open(meta_yaml, "w", encoding="utf-8") as f:
    f.write("---\n")
    f.write(f"title: {yaml_quote(title)}\n")
    f.write("lang: zh-CN\n")
    f.write("---\n")

with open(resource_paths_file, "w", encoding="utf-8") as f:
    for path in sorted(resource_paths, key=sort_key):
        f.write(path + "\n")
PY

resource_path=$(paste -sd: "$resource_paths")

cat > "$epub_css" <<'CSS'
@page {
  size: A4;
  margin: 16mm 14mm;
}

body {
  line-height: 1.65;
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  color: #111;
}

img,
svg,
video {
  max-width: 100%;
  height: auto;
}

table {
  border-collapse: collapse;
  width: 100%;
  max-width: 100%;
  margin: 1em 0;
  font-size: 0.86em;
}

th,
td {
  border: 1px solid #d0d7de;
  padding: 0.35em 0.55em;
  vertical-align: top;
  overflow-wrap: anywhere;
  word-break: break-word;
}

th {
  background: #f6f8fa;
  font-weight: 600;
}

tr:nth-child(even) {
  background: #fbfbfb;
}
CSS

if [ "$output_ext" = "pdf" ]; then
  html_output="$build_dir/book.html"
  mkdir -p "$(dirname "$final_output")"
  pandoc "$meta_yaml" "$book_md" \
    --from markdown+pipe_tables+grid_tables+multiline_tables+raw_html+yaml_metadata_block \
    --to html5 \
    --resource-path="$resource_path" \
    --css "$epub_css" \
    --toc --toc-depth=6 \
    --standalone \
    --output "$html_output"
  python3 - "$html_output" "$src_abs" <<'PY'
import pathlib
import re
import sys

html_path = pathlib.Path(sys.argv[1])
base_uri = pathlib.Path(sys.argv[2]).as_uri().rstrip("/") + "/"
text = html_path.read_text(encoding="utf-8")
base_tag = f'<base href="{base_uri}">'
if "<base " not in text.lower():
    text = re.sub(r"(<head[^>]*>)", r"\1\n" + base_tag, text, count=1, flags=re.I)
html_path.write_text(text, encoding="utf-8")
PY
  "$chrome_bin" \
    --headless \
    --disable-gpu \
    --no-sandbox \
    --allow-file-access-from-files \
    --print-to-pdf="$final_output" \
    "file://$html_output" >/dev/null 2>&1
  printf 'PDF written: %s\n' "$final_output"
else
  mkdir -p "$(dirname "$output")"
  pandoc "$meta_yaml" "$book_md" \
    --from markdown+pipe_tables+grid_tables+multiline_tables+raw_html+yaml_metadata_block \
    --to epub3 \
    --resource-path="$resource_path" \
    --css "$epub_css" \
    --toc --toc-depth=6 \
    --standalone \
    --output "$output"

  python3 - "$output" <<'PY'
import os
import re
import sys
import tempfile
import zipfile

epub = sys.argv[1]
table_style = "border-collapse:collapse;width:100%;max-width:100%;font-size:0.86em;margin:1em 0;"
cell_style = "border:1px solid #d0d7de;padding:0.35em 0.55em;vertical-align:top;word-break:break-word;"
head_style = cell_style + "background:#f6f8fa;font-weight:600;"

def add_style(tag, style):
    pat = re.compile(rf"<{tag}(\s[^>]*)?>", re.I)

    def repl(m):
        attrs = m.group(1) or ""
        sm = re.search(r"""style=(['"])(.*?)\1""", attrs, re.I)
        if sm:
            quote = sm.group(1)
            merged = sm.group(2).rstrip(";") + ";" + style
            attrs = attrs[:sm.start()] + f"style={quote}{merged}{quote}" + attrs[sm.end():]
            return f"<{tag}{attrs}>"
        return f'<{tag}{attrs} style="{style}">'

    return pat, repl

rules = [add_style("table", table_style), add_style("th", head_style), add_style("td", cell_style)]
fd, tmp = tempfile.mkstemp(suffix=".epub", dir=os.path.dirname(epub) or None)
os.close(fd)

try:
    with zipfile.ZipFile(epub, "r") as zin, zipfile.ZipFile(tmp, "w") as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.lower().endswith((".xhtml", ".html")):
                text = data.decode("utf-8")
                for pat, repl in rules:
                    text = pat.sub(repl, text)
                data = text.encode("utf-8")
            zout.writestr(item, data)
    os.replace(tmp, epub)
except Exception:
    try:
        os.unlink(tmp)
    except OSError:
        pass
    raise
PY

  if [ "$output_ext" = "azw3" ]; then
    mkdir -p "$(dirname "$final_output")"
    "$ebook_convert" "$output" "$final_output" >/dev/null
    printf 'AZW3 written: %s\n' "$final_output"
  else
    printf 'EPUB written: %s\n' "$final_output"
  fi
fi
if [ "$keep_build" -eq 1 ]; then
  printf 'Build directory kept: %s\n' "$build_dir"
fi
