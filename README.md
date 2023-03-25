# QNSync
七牛云实时同步工具

## 特性
- WatchDog实时更新
- 支持自定义同步bucket_name与根目录
- 更多特性有待开发...

## 使用
- `pip install qnsync` or `pip3 install qnsync`
- `cd /work/dir`
- `qnsync` (or `nohup qnsync &`)

## 参数
- `--help` 显示帮助并退出
- `--path /path/to/the/config.json` 指定`config.json`（默认为当前目录下的`config.json`）

## `config.json`
```json
{
    "access_key": "access_key",
    "secret_key": "secret_key",
    "bucket_name": "bucket_name",
    "monitor_path": "/work/dir/",
    "base_dir": "/"
}
```
- `access_key`: 七牛云的`AK`
- `secret_key`: 七牛云的`SK`
- `bucket_name`: 七牛云的储存空间名
- `monitor_path`: 监控的目录
- `base_dir`: 七牛云储存的根目录

## 仓库
- `PyPi`: [https://pypi.org/project/qnsync/](https://pypi.org/project/qnsync/)
- `GitHub`: [https://github.com/Gingmzmzx/qnsync](https://github.com/Gingmzmzx/qnsync)