#!/bin/bash

last_file=""
last_time=""

if [ "$#" -ne 1 ]; then
    echo "使用方法: $0 <目录路径>"
    TARGET_DIR="simons/developer-docs/apps/nextra/pages/zh"
else
    TARGET_DIR="$1"

fi

if [ -z "$TARGET_DIR" ]; then
    echo "参数太多或目录路径为空"
    exit 1
fi


# 检查提供的路径是否存在且是目录
if [ ! -d "$TARGET_DIR" ]; then
    echo "错误：提供的路径不存在或不是一个目录。"
    exit 1
fi

# echo "进入路径: $TARGET_DIR"
# 进入目标目录
# cd "$TARGET_DIR"

# 初始化一个空数组
file_paths=()

# 使用find命令查找当前目录及其子目录下的所有文件，并将其路径添加到数组中
while IFS= read -r -d '' file; do
    file_paths+=("$file")
done < <(find "$TARGET_DIR" -type f -print0)

# 打印所有文件路径
for path in "${file_paths[@]}"; do
    # echo "检查文件 $path"
    # 获取文件的修改时间，并转换为 UNIX 时间戳
    mod_time=$(stat -f "%m" "$path")
    # echo "修改时间：$mod_time"
    # 字符串比较需要使用双括号
    if (( mod_time > last_time )); then
        last_time=$mod_time  # 更新 last_time 变量
        last_file="$path"   # 更新 last_file 变量
    fi
done

# 打印最后修改的文件和时间
if [ -n "$last_file" ]; then
    echo "最后修改的文件是：$last_file"
    echo "最后修改时间是：$(date -r "$last_time" +"%Y-%m-%d %H:%M:%S")"
else
    echo "没有找到文件。"
fi

cd "$TARGET_DIR"
# 使用basename命令获取文件名
#filename=$(basename "$last_file")
filename=$(echo "$last_file" | sed 's/^[^/]*\///')
echo "filename is $filename"
echo "last_file is $last_file"
cd ../../../..
echo "current local is `pwd`"
prefix="developer-docs/"
git_file="${filename#$prefix}"
echo "git add file is $git_file"
git add "$git_file"
git commit -m "update file $git_file"
git push
