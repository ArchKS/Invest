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
# find . -type f -name "*.md" | while IFS= read -r md_file; do
#     if [[ "$md_file" == *"$README_FILE" ]]; then
#         continue
#     fi

#     # 没有 CreateTime → 插入头部
#     if ! grep -q "^${CREATE_KEY}" "${md_file}"; then
#         echo "✅ 插入头部：$md_file"
#         echo -e "$HEADER_CONTENT" | cat - "${md_file}" > temp_file && mv temp_file "${md_file}"
#     fi

#     # Git 检测变更 → 更新 LastUpdate
#     if git status --porcelain "${md_file}" | grep -q .; then
#         echo "✅ 更新时间：$md_file"
#         sed -i.bak "s|^${UPDATE_KEY}.*|${UPDATE_KEY} ${INPUT_DATE}|" "${md_file}"
#         rm -f "${md_file}.bak"
#     fi
# done

# ====================== 生成 README：目录结构保留 + 同目录内按文件名排序 ======================
echo ""
echo "📚 生成 README.md 目录结构…"

cat > "$README_FILE" << EOF
# 文档目录
自动生成 | 同目录按文件名排序

> 仓库地址： https://github.com/ArchKS/invest
> Typora插件： https://github.com/obgnail/typora_plugin
EOF

# ai coding: 改为收集 目录|文件名|路径，不再读取文件内的 LastUpdate 时间 2026/11/07: 14:59
# 收集所有文件信息：目录|文件名|路径
tmp=$(mktemp)
find . -type f -name "*.md" | grep -v "$README_FILE" | while IFS= read -r f; do
    dir=$(dirname "$f" | sed 's/^.\///')
    name=$(basename "$f")
    path="$f"
    echo "$dir|$name|$path" >> "$tmp"
done

echo "✅ 文件信息收集完成，开始生成目录结构…"

# ai coding: 排序键由时间改为 目录+文件名，输出条目不再带日期前缀 2026/11/07: 14:59
# 按目录分组、同目录内按文件名排序
sort -t '|' -k1,1 -k2,2 "$tmp" | while IFS='|' read -r dir name path; do
    relpath=${path#./}
    if [[ "$relpath" =~ ^书单/阅读笔记/ ]]; then
        :  # 匹配到则跳过，不处理
    else
        if [ "$dir" = "." ]; then
            echo "[$name]($relpath)" >> "$README_FILE"
            echo "" >> "$README_FILE"
        else
            if [ "$last_dir" != "$dir" ]; then
                echo -e "\n## $dir\n" >> "$README_FILE"
                last_dir="$dir"
            fi
            echo "- [$name]($relpath)" >> "$README_FILE"
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