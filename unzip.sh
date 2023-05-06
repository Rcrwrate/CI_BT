#!/bin/bash

# 解压缩函数
function extract_archive() {
  local archive="$1"
  local destination="$2"

  if [[ "$archive" == *.zip ]]; then
    unzip -n "$archive" -d "$destination"
  elif [[ "$archive" == *.7z ]]; then
    7z x "$archive" -o"$destination" -y
  fi
}

# 遍历文件夹中的所有文件
function process_files() {
  local dir="$1"

  for file in "$dir"/*; do
    # 如果是压缩包则解压
    if [[ "$file" == *.zip || "$file" == *.7z ]]; then
      # 创建目标文件夹
      filename=$(basename "$file" | cut -f 1 -d '.')
      mkdir "$dir/$filename"
      # 解压到目标文件夹
      extract_archive "$file" "$dir/$filename"
      # 递归处理目标文件夹下的文件
      process_files "$dir/$filename"
    fi
  done
}

# 指定要遍历的文件夹
dir="./image"

# 调用函数处理文件夹中的压缩包
process_files "$dir"
