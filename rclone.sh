#!/bin/bash


while getopts "p:" opt; do
  case $opt in
    p)
      path="$OPTARG"
      ;;
    \?)
      echo "无效的选项: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "选项 -$OPTARG 需要一个参数." >&2
      exit 1
      ;;
  esac
done

if [[ $path == "Upload"* ]]; then
  rclone --config=rclone.conf copyto local:image "Save:$path" --log-level INFO
else
  echo "The Remote does not start with 'Upload'"
fi
