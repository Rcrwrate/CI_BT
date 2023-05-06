#!/bin/bash

# 指定要遍历的文件夹
dir="./image"

# 遍历文件夹中的所有文件
for file in "$dir"/*
do
  # 判断文件是否为压缩包（zip 或 7z）
  if [[ "$file" == *.zip || "$file" == *.7z ]]
  then
    # 解压文件到以文件名命名的文件夹中
    filename=$(basename "$file" | cut -f 1 -d '.')
    mkdir "$dir/$filename"
    if [[ "$file" == *.zip ]]
    then
      unzip -n "$file" -d "$dir/$filename"
    else
      7z x "$file" -o"$dir/$filename" -y
    fi
  fi
done
