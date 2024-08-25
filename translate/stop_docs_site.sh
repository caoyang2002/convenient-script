jq '.scripts.dev = "next -p 3030"' simons/developer-docs/apps/nextra/package.json > temp.json && mv temp.json simons/developer-docs/apps/nextra/package.json

# aotps site
echo "Checking for processes running on port 3030..."
lsof -i :3030 | grep LISTEN

# 如果找到8080端口上的监听进程，则杀死该进程
if [ $? -eq 0 ]; then
    echo "Port 3030 is in use. Killing the process..."
    lsof -i :3030 | grep LISTEN | awk '{print $2}' | xargs -I {} kill -9 {}
    echo "Process killed."
else
    echo "No process found running on port 3030."
fi

# simons site
echo "Checking for processes running on port 3031..."
lsof -i :3031 | grep LISTEN

# 如果找到8080端口上的监听进程，则杀死该进程
if [ $? -eq 0 ]; then
    echo "Port 3031 is in use. Killing the process..."
    lsof -i :3031 | grep LISTEN | awk '{print $2}' | xargs -I {} kill -9 {}
    echo "Process killed."
else
    echo "No process found running on port 3031."
fi
