#!/bin/bash

set -u

# 获取当前工作区目录
WORKSPACE=$(pwd -P)
echo "正在扫描目录: $WORKSPACE"

# 创建临时文件来存储路径
TEMP_REFS=$(mktemp)
TEMP_IMGS=$(mktemp)
TEMP_REFS_SORTED="${TEMP_REFS}.sorted"
TEMP_IMGS_SORTED="${TEMP_IMGS}.sorted"

cleanup() {
    rm -f "$TEMP_REFS" "$TEMP_IMGS" "$TEMP_REFS_SORTED" "$TEMP_IMGS_SORTED"
}
trap cleanup EXIT HUP INT TERM

# macOS 自带的 realpath 不支持 GNU realpath 的 -m 参数。
# 引用的图片本来就必须存在，因此通过进入其父目录来规范化绝对路径。
normalize_existing_path() {
    local path=$1
    local dir
    local filename

    [ -e "$path" ] || return 1
    dir=$(dirname "$path")
    filename=$(basename "$path")
    (
        cd -P "$dir" 2>/dev/null || exit 1
        printf '%s/%s\n' "$PWD" "$filename"
    )
}

record_reference() {
    local md_dir=$1
    local url=$2
    local url_decoded
    local img_path

    # 排除网络图片、协议相对 URL 和 Base64 数据。
    case "$url" in
        http://*|https://*|//*|data:*) return ;;
    esac

    # 去除 Markdown 的可选尖括号、查询参数和锚点。
    url=${url#<}
    url=${url%>}
    url=${url%%\?*}
    url=${url%%\#*}

    # URL 解码（例如 %20）。这是 Bash 3.2（macOS 默认版本）支持的写法。
    url_decoded=$(printf '%b' "${url//%/\\x}")
    if img_path=$(normalize_existing_path "$md_dir/$url_decoded"); then
        printf '%s\n' "$img_path" >> "$TEMP_REFS"
    fi
}

# 1. 查找所有的图片文件（排除 .venv, .git, node_modules 等目录）
find "$WORKSPACE" \
    -type d \( -name ".venv" -o -name ".git" -o -name "node_modules" \) -prune -o \
    -type f \( \
        -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" -o \
        -iname "*.gif" -o -iname "*.svg" -o -iname "*.webp" \
    \) -print | while IFS= read -r img; do
    normalize_existing_path "$img" >> "$TEMP_IMGS"
done

# 2. 查找所有的 Markdown 文件并提取图片链接
find "$WORKSPACE" \
    -type d \( -name ".venv" -o -name ".git" -o -name "node_modules" \) -prune -o \
    -type f -name "*.md" -print | while IFS= read -r md_file; do
    md_dir=$(dirname "$md_file")

    # macOS 的 grep 不支持 -P；Perl 是 macOS 自带工具，可同时解析 Markdown
    # 图片和 HTML img 标签。每行输出一个本地图片 URL。
    perl -ne '
        while (/!\[[^]]*\]\(\s*(<[^>]+>|[^[:space:])]+)(?:\s+[^)]*)?\)/g) {
            print "$1\n";
        }
        while (/<img\b[^>]*\bsrc\s*=\s*(["\x27])([^"\x27]+)\1/gi) {
            print "$2\n";
        }
    ' "$md_file" | while IFS= read -r url; do
        record_reference "$md_dir" "$url"
    done
done

# 3. 对比列表并删除未引用的图片
if [ -s "$TEMP_IMGS" ]; then
    # 排序和去重
    sort -u "$TEMP_IMGS" > "$TEMP_IMGS_SORTED"
    touch "$TEMP_REFS"
    sort -u "$TEMP_REFS" > "$TEMP_REFS_SORTED"
    
    # 找出存在于系统但未被引用的图片
    # comm -23 比较两个已排序的文件，输出只在第一个文件中的行
    UNUSED_IMGS=$(comm -23 "$TEMP_IMGS_SORTED" "$TEMP_REFS_SORTED")
    
    if [ -z "$UNUSED_IMGS" ]; then
        echo "🎉 没有发现未使用的图片。"
    else
        printf '%s\n' "$UNUSED_IMGS" | while IFS= read -r img_to_delete; do
            if [ -n "$img_to_delete" ]; then
                rm -f "$img_to_delete"
                echo "已删除: $img_to_delete"
            fi
        done
        # 由于在管道中修改变量，这里通过再次计算行数来显示正确的数量
        final_count=$(printf '%s\n' "$UNUSED_IMGS" | wc -l | tr -d ' ')
        echo "✅ 清理完成！共删除了 $final_count 张未使用的图片。"
    fi
else
    echo "未发现任何本地图片。"
fi
