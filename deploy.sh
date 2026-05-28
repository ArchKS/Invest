#!/bin/bash

# ====================== 配置区 ======================
TIME_FORMAT="%Y-%m-%d %H:%M:%S"
HEADER_SEP="---"
CREATE_KEY="CreateTime:"
UPDATE_KEY="LastUpdate:"
README_FILE="README.md"
# =====================================================

# 1. 获取用户输入日期
INPUT_DATE="$1"
if [ -z "$INPUT_DATE" ]; then
    INPUT_DATE=$(date +"$TIME_FORMAT")
fi

# 2. 获取commit信息
COMMIT_MSG="$2"
if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="Auto commit: $(date +"$TIME_FORMAT")"
fi

HEADER_CONTENT="${HEADER_SEP}
${CREATE_KEY} ${INPUT_DATE}
${UPDATE_KEY} ${INPUT_DATE}
${HEADER_SEP}
"

echo "============================================="
echo "📅 使用时间：$INPUT_DATE"
echo "📝 Commit信息：$COMMIT_MSG"
echo "============================================="

# 3. 递归处理所有 md 文件
find . -type f -name "*.md" | while IFS= read -r md_file; do
    if [[ "$md_file" == *"$README_FILE" ]]; then
        continue
    fi

    # 没有 CreateTime → 插入头部
    if ! grep -q "^${CREATE_KEY}" "${md_file}"; then
        echo "✅ 插入头部：$md_file"
        echo -e "$HEADER_CONTENT" | cat - "${md_file}" > temp_file && mv temp_file "${md_file}"
    fi

    # Git 检测变更 → 更新 LastUpdate
    if git status --porcelain "${md_file}" | grep -q .; then
        echo "✅ 更新时间：$md_file"
        sed -i.bak "s|^${UPDATE_KEY}.*|${UPDATE_KEY} ${INPUT_DATE}|" "${md_file}"
        rm -f "${md_file}.bak"
    fi
done

# ====================== 生成 README：目录结构保留 + 同目录内时间正序 ======================
echo ""
echo "📚 生成 README.md 目录结构…"

cat > "$README_FILE" << EOF
# 文档目录
自动生成 | 同目录按最后更新时间正序（最早→最新）

> 仓库地址： https://github.com/ArchKS/invest
> Typora插件： https://github.com/obgnail/typora_plugin
EOF

# 收集所有文件信息：完整时间|目录|文件名|路径
tmp=$(mktemp)
find . -type f -name "*.md" | grep -v "$README_FILE" | while IFS= read -r f; do
    ts=$(grep "^$UPDATE_KEY" "$f" | head -1 | sed 's/LastUpdate: //')
    dir=$(dirname "$f" | sed 's/^.\///')
    name=$(basename "$f")
    path="$f"
    echo "$ts|$dir|$name|$path" >> "$tmp"
done

echo "✅ 文件信息收集完成，开始生成目录结构…"

# ✅ 正确正序排序（字符串时间）
sort -t '|' -k2,2 -k1,1r "$tmp" | while IFS='|' read -r ts dir name path; do
    [ -z "$ts" ] && continue
    show_date=${ts:0:10}
    relpath=${path#./}
    # echo "$relpath  $path"
    if [[ "$relpath" =~ ^书单/阅读笔记/ ]]; then
        echo "匹配成功"
    else
        # echo "匹配失败"
        if [ "$dir" = "." ]; then
            echo "$show_date  [$name]($relpath)" >> "$README_FILE"
            echo "" >> "$README_FILE"
        else
            if [ "$last_dir" != "$dir" ]; then
                echo -e "\n## $dir\n" >> "$README_FILE"
                last_dir="$dir"
            fi
            echo "- $show_date  [$name]($relpath)" >> "$README_FILE"
        fi
    fi
    
done

rm -f "$tmp"
echo "✅ README.md 生成完成！"
# ======================================================================================

echo ""
echo "============================================="
echo "🚀 Git 提交推送中..."
git add .
git commit -m "$COMMIT_MSG"
git push
echo "✅ 全部执行完成！"
echo "============================================="