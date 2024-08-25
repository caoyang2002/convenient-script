#!/bin/bash

# 脚本使用方法
if [ "$#" -ne 3 ]; then
        echo "使用方法：$0 源目录(旧的文件)   目标目录（新的文件）   需要比较的路径"
    echo "例如：$0 origin/dir double/dir dir/text/folder"
    exit 1
fi

# 读取参数作为文件路径
orig_dir="$1"
doub_dir="$2"
path="$3"

# 先去 aptos 下面去 pull 一下
cd "$orig_dir"
git pull
cd ../.. 

# 拼接完整的路径
ab_path_orig="$orig_dir/$path"
ab_path_doub="$doub_dir/$path"

# 确保目标子路径存在
if [ ! -d "$ab_path_orig" ] || [ ! -d "$ab_path_doub" ]; then
    echo "错误：指定的源目录或目标目录下的子路径不存在。"
    exit 1
fi

# 获取源路径和目标路径下的所有文件
existence_orig=($(find "$ab_path_orig" -type f))
existence_doub=($(find "$ab_path_doub" -type f))

# 创建输出目录和文件
output_dir="diff"
mkdir -p "$output_dir"
output_file="$output_dir/$(date +%Y-%m-%d).md"

# 创建数组用于存放不同的文件
diff_files=()
same_files=()
only_origin=()

# 创建 diff_file 函数，比较两个文件的差异
function diff_file() {
    local orig_file="$1"
    local doub_file="$2"
    local relative_file="${orig_file#$ab_path_orig}"

    if [ ! -f "$doub_file" ]; then
        # echo "# 文件 \`$relative_file\` 仅存在于源目录中。" >> "$output_file"
        only_origin+=("$relative_file")
        return
    fi
   
    if diff -q "$orig_file" "$doub_file" > /dev/null; then
        # echo "# 文件 \`$relative_file\` 在两个目录中相同。" >> "$output_file"
        same_files+=("$relative_file")
    else
        # echo "# 文件 \`$relative_file\` 在两个目录中存在差异：" >> "$output_file"
        # echo "\`\`\`\`">> "$output_file"
        diff -u "$orig_file" "$doub_file" >> "$output_file"
        # echo "\`\`\`\`">> "$output_file"

        # 首先，执行 diff 命令并将其输出存储在变量 diff_output 中
        diff_output=$(diff -u "$orig_file" "$doub_file")

        # 然后，将格式化的文本和 diff 命令的输出一起作为数组的一个元素
        # echo "relative_file is $relative_file"
        diff_content="\`$relative_file\`

- [ ] 完成

\`\`\`\`diff
$diff_output
\`\`\`\`"

        # echo "$diff_content"
        # 将 diff_content 添加到 diff_files 数组中
        #diff_files+=("$diff_content")
        diff_files+=("$diff_content")
    fi
}
# 创建 outputfile 函数，输出不同文件、仅存在于源目录的文件和相同文件的列表

function outputfile() {
    # 清空输出文件，以覆盖模式开始写入
    > "$output_file"

    # 遍历不同的文件数组并输出
    if [ ${#diff_files[@]} -ne 0 ]; then
        echo "# 不同的文件" >> "$output_file"
        for file in "${diff_files[@]}"; do
            echo "## $file" >> "$output_file"
            # echo "```diff" >> "$output_file"
            # diff -u "${ab_path_orig}$file" "${ab_path_doub}$file" >> "$output_file"
            # echo "$?"
            # echo "```" >> "$output_file"
            # echo -e "\n" >> "$output_file"
        done
    fi

    # 遍历仅存在于源目录的文件数组并输出
    if [ ${#only_origin[@]} -ne 0 ]; then
        echo "# 仅存在于源目录中的文件" >> "$output_file"
        for file in "${only_origin[@]}"; do
            echo "## \`$file\`" >> "$output_file"
        done
    else
         echo "# 没有仅存在于目录中的文件" >> "$output_file"
    fi

    # 遍历相同的文件数组并输出
    if [ ${#same_files[@]} -ne 0 ]; then
        echo "# 相同的文件" >> "$output_file"
        for file in "${same_files[@]}"; do
            echo "## \`$file\`" >> "$output_file"
        done
    fi
}


# 比较文件内容差异，并输出到文件
for orig_file in "${existence_orig[@]}"; do
    doub_file="${ab_path_doub}${orig_file#$ab_path_orig}"
    diff_file "$orig_file" "$doub_file"
    outputfile
done

echo "比较完成。结果已保存到 '$output_file'。"
