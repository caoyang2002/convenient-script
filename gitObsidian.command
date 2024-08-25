#! /bin/bash


#current_dir=$(pwd)
#
#cd /Users/caoyang/Documents/Obsidian\ Vault
#echo 开始添加仓库
#git add . 
#echo 添加动作注释
#git commit -m "update"
#git push origin master
#cd "$current_dir"
#echo 按任意键退出...
#read -n 1
#echo 已退出

current_dir=$(pwd)
cd /Users/caoyang/Documents/Obsidian\ Vault
# 获取当前时间
current_time=$(date +"%Y-%m-%d %T")
echo "当前时间是：$current_time"
# 获取所有有更改的文件列表
changed_files=$(git status --short | awk '{print $2}')
echo "发生更改的文件是：$changed_files"
# 添加所有更改的文件到暂存区
echo "添加所有更改的文件到暂存区..."
git add .
# 构建提交信息
commit_message="docs(update): update, $current_time\n\nChanged files:\n"
for file in $changed_files
do
    commit_message="$commit_message- $file\n"
done
# 提交更改
echo "提交更改..."
echo -e "$commit_message" | git commit -F -
# 推送更改到远程仓库
echo "推送更改到远程仓库..."
git push origin master
cd "$current_dir"
echo "按任意键退出..."
read -n 1
echo "已退出"


