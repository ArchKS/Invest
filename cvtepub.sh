#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  cvtepub [options] SOURCE_DIR [OUTPUT.epub]

Convert Markdown and HTML files under SOURCE_DIR into one EPUB.

Options:
  -o, --output FILE     EPUB output path
  -t, --title TITLE     Book title (default: source directory name)
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

title=""
output=""
keep_build=0
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

build_dir=$(mktemp -d "${TMPDIR:-/tmp}/cvtepub.XXXXXX")
if [ "$keep_build" -eq 0 ]; then
  trap 'rm -rf "$build_dir"' EXIT
fi

book_md="$build_dir/book.md"
meta_yaml="$build_dir/metadata.yml"
epub_css="$build_dir/epub.css"
resource_paths="$build_dir/resource-paths.txt"

python3 - "$src_abs" "$title" "$book_md" "$meta_yaml" "$resource_paths" <<'PY'
import os
import re
import subprocess
import sys
import unicodedata

src, title, book_md, meta_yaml, resource_paths_file = sys.argv[1:6]
TEXT_EXTS = {".md", ".markdown", ".html", ".htm"}
SKIP_DIRS = {".git", ".hg", ".svn", "node_modules", "__pycache__"}
SKIP_FILES = {".DS_Store"}

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

resource_paths = {src}
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
body {
  line-height: 1.65;
}

table {
  border-collapse: collapse;
  display: block;
  overflow-x: auto;
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

mkdir -p "$(dirname "$output")"
pandoc "$meta_yaml" "$book_md" \
  --from markdown+pipe_tables+grid_tables+multiline_tables+raw_html+yaml_metadata_block \
  --to epub3 \
  --resource-path="$resource_path" \
  --css "$epub_css" \
  --toc --toc-depth=6 \
  --standalone \
  --output "$output"

printf 'EPUB written: %s\n' "$output"
if [ "$keep_build" -eq 1 ]; then
  printf 'Build directory kept: %s\n' "$build_dir"
fi
