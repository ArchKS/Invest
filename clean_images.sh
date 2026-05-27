#!/bin/bash

# 获取当前工作区目录
WORKSPACE=$(pwd)
echo "正在扫描目录: $WORKSPACE"

# 创建临时文件来存储路径
TEMP_REFS=$(mktemp)
TEMP_IMGS=$(mktemp)

# 1. 查找所有的图片文件（排除 .venv, .git, node_modules 等目录）
find "$WORKSPACE" -type d \( -name ".venv" -o -name ".git" -o -name "node_modules" \) -prune -o -type f -iregex '.*\.\(png\|jpg\|jpeg\|gif\|svg\|webp\)$' -print | while read -r img; do
    # 转换为绝对路径并规范化
    realpath "$img" >> "$TEMP_IMGS"
done

# 2. 查找所有的 Markdown 文件并提取图片链接
find "$WORKSPACE" -type d \( -name ".venv" -o -name ".git" -o -name "node_modules" \) -prune -o -type f -name "*.md" -print | while read -r md_file; do
    md_dir=$(dirname "$md_file")
    
    # 使用 grep 提取 markdown 图片格式 ![alt](url)
    # \K 丢弃之前匹配的部分
    grep -oP '!\[.*?\]\(\K[^)]+' "$md_file" | while read -r url; do
        # 排除网络图片和 Base64 数据
        if [[ "$url" != http* ]] && [[ "$url" != data:* ]]; then
            # 去掉后面可能跟随的 "title" (空格分隔)
            url="${url%% *}"
            # URL 解码 (将 %20 等转换为对应的字符)
            url_decoded=$(printf '%b' "${url//%/\\x}")
            
            # 转换为绝对路径
            img_path=$(realpath -m "$md_dir/$url_decoded")
            echo "$img_path" >> "$TEMP_REFS"
        fi
    done
    
    # 使用 grep 提取 HTML 图片格式 <img src="url" />
    grep -oP '<img\s+[^>]*src="\K[^"]+' "$md_file" | while read -r url; do
        if [[ "$url" != http* ]] && [[ "$url" != data:* ]]; then
            url="${url%% *}"
            url_decoded=$(printf '%b' "${url//%/\\x}")
            img_path=$(realpath -m "$md_dir/$url_decoded")
            echo "$img_path" >> "$TEMP_REFS"
        fi
    done
done

# 3. 对比列表并删除未引用的图片
if [ -s "$TEMP_IMGS" ]; then
    # 排序和去重
    sort -u "$TEMP_IMGS" > "${TEMP_IMGS}.sorted"
    touch "$TEMP_REFS"
    sort -u "$TEMP_REFS" > "${TEMP_REFS}.sorted"
    
    # 找出存在于系统但未被引用的图片
    # comm -23 比较两个已排序的文件，输出只在第一个文件中的行
    UNUSED_IMGS=$(comm -23 "${TEMP_IMGS}.sorted" "${TEMP_REFS}.sorted")
    
    if [ -z "$UNUSED_IMGS" ]; then
        echo "🎉 没有发现未使用的图片。"
    else
        deleted_count=0
        echo "$UNUSED_IMGS" | while read -r img_to_delete; do
            if [ -n "$img_to_delete" ]; then
                rm -f "$img_to_delete"
                echo "已删除: $img_to_delete"
                deleted_count=$((deleted_count + 1))
            fi
        done
        # 由于在管道中修改变量，这里通过再次计算行数来显示正确的数量
        final_count=$(echo "$UNUSED_IMGS" | wc -l)
        echo "✅ 清理完成！共删除了 $final_count 张未使用的图片。"
    fi
else
    echo "未发现任何本地图片。"
fi

# 4. 清理临时文件
rm -f "$TEMP_REFS" "$TEMP_IMGS" "${TEMP_REFS}.sorted" "${TEMP_IMGS}.sorted"
