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
TEMP_KEPT=$(mktemp)
TEMP_ORPHAN=$(mktemp)

cleanup() {
    rm -f "$TEMP_REFS" "$TEMP_IMGS" "$TEMP_REFS_SORTED" "$TEMP_IMGS_SORTED" "$TEMP_KEPT" "$TEMP_ORPHAN"
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

# ai coding: 增加按文件名搜索引用的兜底函数，文件名出现在任何非图片文本文件中即视为被引用 2026/11/07: 15:10
# 在仓库所有非图片文件（md、html 等任意文本格式）中按固定字符串查找图片文件名，
# 用于兜底"md 被移动、图片留在原地"导致的相对路径断链场景。
find_name_references() {
    local base=$1
    grep -r -F -I -l \
        --exclude-dir=.git --exclude-dir=.venv --exclude-dir=node_modules \
        --exclude='*.png' --exclude='*.jpg' --exclude='*.jpeg' \
        --exclude='*.gif' --exclude='*.svg' --exclude='*.webp' \
        -- "$base" "$WORKSPACE" 2>/dev/null
}

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
        # ai coding: 分类为"断链引用（保留并输出对照）"和"真孤儿（删除）"，先报告后删除 2026/11/07: 15:10
        # 3.1 分类：路径解析失败的图片，再按文件名兜底搜一遍
        printf '%s\n' "$UNUSED_IMGS" | while IFS= read -r img_path; do
            [ -z "$img_path" ] && continue
            base=$(basename "$img_path")
            if find_name_references "$base" | grep -q .; then
                echo "$img_path" >> "$TEMP_KEPT"
            else
                echo "$img_path" >> "$TEMP_ORPHAN"
            fi
        done

        # 3.2 输出保留清单：图片路径 + 引用它的文件路径
        if [ -s "$TEMP_KEPT" ]; then
            echo "---------------------------------------------"
            echo "🔒 以下图片路径引用已断，但文件名仍在文件中出现，予以保留："
            while IFS= read -r kept_img; do
                [ -z "$kept_img" ] && continue
                echo "图片: $kept_img"
                find_name_references "$(basename "$kept_img")" | while IFS= read -r ref_file; do
                    echo "  ↳ 被引用于: $ref_file"
                done
            done < "$TEMP_KEPT"
            echo "---------------------------------------------"
        fi

        # 3.3 只删除真孤儿（文件名在任何文件中都没出现过）
        if [ -s "$TEMP_ORPHAN" ]; then
            while IFS= read -r img_to_delete; do
                if [ -n "$img_to_delete" ]; then
                    rm -f "$img_to_delete"
                    echo "已删除: $img_to_delete"
                fi
            done < "$TEMP_ORPHAN"
        fi

        deleted_count=$(wc -l < "$TEMP_ORPHAN" | tr -d ' ')
        kept_count=$(wc -l < "$TEMP_KEPT" | tr -d ' ')
        echo "✅ 清理完成！共删除了 $deleted_count 张未使用的图片，保留 $kept_count 张断链引用图片。"
    fi
else
    echo "未发现任何本地图片。"
fi
