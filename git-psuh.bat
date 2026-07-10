@echo off
title GIT一键提交
color 3
echo 当前目录：%cd%
echo
git init
:: 添加所有变更
git add .
:: 输入提交信息（默认当前时间）
set filename=%date:~0,4%-%date:~5,2%-%date:~8,2%_%time:~0,2%:%time:~3,2% 一键提交
set /p commit_msg=请输入提交说明(回车默认时间):
if "%commit_msg%"=="" set commit_msg=%filename%
:: 提交到当前分支
git commit -m "%commit_msg%"
git push origin HEAD
pause