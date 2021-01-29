# LoggerClass

用`Python`内置的`logging`库封装的日志功能。按日志文件大小卷动备份，简单易用。`class`版。

### 使用说明

1. #### 日志样式
    ```shell
    [ 2021-01-29 13:49:34,180 ][ INFO ][ example.py:demo:22 ][ 4 ]
    ```
    + 样式说明
        + 时间：`[ 2021-01-29 13:49:34,180 ]`
        + 日志级别：`[ INFO ]`
        + 文件名:函数名:行号：`[ example.py:demo:22 ]`
        + 日志内容：`[ 4 ]`

2. #### 参数说明
    + 所有参数均为可选参数

      |`NO` | 参数名 | 默认值| 作用 |
      |---|  ---  | ---  | --- |
      | 1  | `log_dir`        |同级目录下的`logs`目录 | 日志文件存在的目录    |
      | 2  | `filename`       |默认为所在文件名(带后缀)`.log` | 日志文件的名称  |
      | 3  | `max_size`       |`256`(单位`MB`) | 单个日志文件最大大小，超过这个大小会自动进行备份|
      | 4  | `backup_count`   |4 | 日志文件最大备份数量(不包含`.log`后缀的文件)|

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
   logger.py.log 内容：
   [ 2021-01-29 13:49:32,178 ][ INFO ][ example.py:demo:22 ][ 0 ]
   [ 2021-01-29 13:49:32,679 ][ INFO ][ example.py:demo:22 ][ 1 ]
   [ 2021-01-29 13:49:33,180 ][ INFO ][ example.py:demo:22 ][ 2 ]
   [ 2021-01-29 13:49:33,680 ][ INFO ][ example.py:demo:22 ][ 3 ]
   [ 2021-01-29 13:49:34,180 ][ INFO ][ example.py:demo:22 ][ 4 ]
   """
   ```
