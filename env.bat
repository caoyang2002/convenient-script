@echo off
SET "NEW_PATH=C:\Windows\System32;C:\Program Files\Google\Chrome\Application;C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.3;C:\Program Files\Git\bin;C:\Program Files\nodejs;C:\Program Files\Pandoc\"

REM 检查是否存在该路径
FOR /F "usebackq tokens=2*" %%A IN (`REG QUERY "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path 2^>nul`) DO (
    IF "%%A"=="Path" (
        SET "CURRENT_PATH=%%B"
    )
)

REM 将新路径添加到现有的PATH环境变量
SET "UPDATED_PATH=%CURRENT_PATH%;%NEW_PATH%"

REM 使用reg命令更新注册表中的PATH环境变量
REG ADD "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /d "%UPDATED_PATH%" /f

echo Updated PATH environment variable successfully.
pause