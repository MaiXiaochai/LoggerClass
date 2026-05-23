# LoggerClass

用`Python`内置的`logging`库封装的日志功能。按日志文件大小卷动备份，简单易用。`class`版。

### 使用说明

1. #### 日志样式
    ```shell
    [ 2021-01-29 13:49:34,180 ][ INFO ][ 4 ]
    ```
    + ##### 样式说明
        + 时间：`[ 2021-01-29 13:49:34,180 ]`
        + 日志级别：`[ INFO ]`
        + 日志内容：`[ 4 ]`

2. #### 参数说明
    + ##### 所有参数均为可选参数
    + ##### 参数详解
        + ##### `log_dir`
            + 日志文件存放的目录
            + 默认值：同级目录下的`logs`目录
        + ##### `filename`
            + 日志文件的名称
            + 默认值：调用方文件名`.log`（如从 `demo.py` 调用，则日志文件为 `demo.py.log`）
        + ##### `max_size`
            + 单个日志文件最大值(单位`MB`)，达到这个值会自动进行备份
            + 默认值：`64`
        + ##### `backup_count`
            + 日志文件最大备份数量(不包含`.log`后缀的文件)
            + 默认值：`8`

3. #### 使用例子
   [example.py（点击跳转到源码）](example.py)
   ```python
   from logger import Logger
   
   
   def demo():
       from time import sleep
   
       log = Logger().log
   
       for i in range(5):
           sleep(0.5)
           log.info(i)
   
   
   if __name__ == '__main__':
       demo()
   
   """
   example.py.log 内容：
   [ 2021-01-29 13:49:32,178 ][ INFO ][ 0 ]
   [ 2021-01-29 13:49:32,679 ][ INFO ][ 1 ]
   [ 2021-01-29 13:49:33,180 ][ INFO ][ 2 ]
   [ 2021-01-29 13:49:33,680 ][ INFO ][ 3 ]
   [ 2021-01-29 13:49:34,180 ][ INFO ][ 4 ]
   """
   ```
