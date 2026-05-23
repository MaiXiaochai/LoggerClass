# LoggerClass

基于 Python 内置 `logging` 封装的日志类。按文件大小自动卷动备份，简单够用。

## 快速开始

```python
from logger import Logger

log = Logger().log
log.info("你好")
```

输出：
```
[ 2026-05-24 06:32:38,778 ][ INFO ][ 你好 ]
```

## 日志格式

```
[ 时间 ][ 级别 ][ 内容 ]
```

可通过 `self.formatter` 自定义，详见下方"高级配置"。

## 参数

所有参数均为可选。

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `log_dir` | `str` | 调用方同级 `logs/` 目录 | 日志文件存放目录 |
| `filename` | `str` | 调用方文件名 `.log` | 如从 `demo.py` 调用则为 `demo.py.log` |
| `max_size` | `float \| int` | `64` | 单个日志文件最大值，单位 MB |
| `backup_count` | `int` | `8` | 备份文件数量（不含当前 `.log` 文件） |

## 高级配置

实例化后可直接修改以下属性，在首次调用 `.log` 前设置即可：

```python
logger = Logger()
logger.log_level = DEBUG        # 日志器级别，≥ 此级别才处理
logger.file_log_level = INFO    # 写入文件的级别
logger.print_level = WARNING    # 屏幕输出的级别
logger.formatter = "[ %(asctime)s ][ %(levelname)s ][ %(message)s ]"
logger.encoding = "utf-8"

log = logger.log
```

## 使用场景

### 自定义路径和大小

```python
log = Logger(
    log_dir="./my_logs",
    filename="app.log",
    max_size=128,      # 128MB
    backup_count=5
).log
```

### 仅输出到屏幕特定级别

```python
logger = Logger()
logger.print_level = WARNING  # 屏幕只显示 WARNING 及以上

log = logger.log
log.debug("不会显示")
log.info("不会显示")
log.warning("会显示")
```

### 多实例独立日志

```python
# 每个实例有独立的日志文件，互不干扰
api_log = Logger(filename="api").log
db_log = Logger(filename="database").log

api_log.info("API 请求")
db_log.error("数据库错误")
```
