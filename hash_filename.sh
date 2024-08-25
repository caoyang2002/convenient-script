#!/bin/bash

# 检查是否有足够的参数
if [ $# -eq 0 ]; then
  echo "使用方法: $0 [目录路径]"
  exit 1
fi

# 定义目录路径
TARGET_DIR="$1"

# 检查目录是否存在
if [ ! -d "$TARGET_DIR" ]; then
  echo "错误：目录不存在 '$TARGET_DIR'"
  exit 1
fi

# 进入目录
cd "$TARGET_DIR" || exit

# 遍历目录中的每个文件
for file in *; do
  if [ -f "$file" ]; then # 确保是文件
    # 获取文件的扩展名
    extension="${file##*.}"

    # 计算文件的 SHA-256 哈希值
    hash_value=$(sha256sum "$file" | awk '{print $1}')

    # 使用哈希值作为新文件名，保留原始扩展名
    new_filename="$hash_value.$extension"

    # 重命名文件
    mv "$file" "$new_filename"
    echo "文件 '$file' 已重命名为 '$new_filename'"
  fi
done

echo "所有文件已根据哈希值重命名。"
