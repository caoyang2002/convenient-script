#!/bin/bash
	
COMMAND="pnpm dev"
OUTPUT_LOG="output.log"
ERROR_LOG="error.log"
JSON="simons/developer-docs/apps/nextra/package.json"
APTOS_GIT="aptos-labs/developer-docs"
APTOS_GIT_REPO="https://github.com/aptos-labs/developer-docs.git"
SIMONS_GIT="simons/developer-docs"
TARGET_APP="apps/nextra"
PID_FILE="site.pid"
APTOS_PORT=3030
SIMONS_PORT=3031
SLEEP=2

echo "update json $JSON"
jq '.scripts.dev = "next -p 3031"' "$JSON"  > temp.json && mv temp.json "$JSON"
#jq '.scripts.dev = "next -p 3031"' simons/aptos-developer-docs/apps/nextra/package.json > temp.json && mv temp.json simons/aptos-developer-docs/apps/nextra/package.json

# 函数：启动命令并记录 PID
start_site() {
	cd $APTOS_GIT
	git pull $APTOS_GIT_REPO
	cd $TARGET_APP
	echo "current path is `pwd`"
    cat package.json | grep '"dev"'
    echo "Starting command: $COMMAND"
    nohup $COMMAND > "../../../$OUTPUT_LOG" 2> "../../../$ERROR_LOG" &
    
    local pid=$!
    echo $pid > "../../../$PID_FILE"
    echo "Command started successfully with PID: $pid"
    
    echo "sleep $SLEEP" 
    # 短暂等待，确保服务有足够的时间启动并监听端口
    sleep "$SLEEP"
    
    #检查端口状态，确保服务已启动并监听指定端口
    check_port "$APTOS_PORT"
    # --------------------------
    cd ../../../..
    echo "current path is `pwd`"
    # --------------------------
    cd $SIMONS_GIT
	cd $TARGET_APP
	echo "current path is `pwd`"
    cat package.json | grep '"dev"'
    echo "Starting command: $COMMAND"
    nohup $COMMAND > "../../../$OUTPUT_LOG" 2> "../../../$ERROR_LOG" &
    
    local pid=$!
    echo $pid > "../../../$PID_FILE"
    echo "Command started successfully with PID: $pid"
    
    echo "sleep $SLEEP" 
    # 短暂等待，确保服务有足够的时间启动并监听端口
    sleep "$SLEEP"
    check_port "$SIMONS_PORT"
}

# 函数：检查端口是否正在使用
check_port() {
    local PORT="$1"
    lsof -i :"$PORT"
    echo $?
    echo "checking $PORT"
    if  `lsof -i :"$PORT"` > /dev/null; then
        print_color "\033[31m" "Error: Port $PORT is not in use. Program may not be running."
        exit 1
    else
        print_color "\033[32m" "Success: Port $PORT is active. Program is running."
    fi
}

# 函数：输出带有颜色的文本
print_color() {
    local color=$1
    local message=$2
    echo -e "${color}${message}"
}

start_site  

print_color "\033[39m" "EXIT"
