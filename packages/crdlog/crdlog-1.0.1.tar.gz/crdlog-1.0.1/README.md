## 日志记录功能包

#### 所需环境

```
python 3.10.10
```

#### 所需三方包

```
datetime (5.1)
colorlog (6.7.0)
```

#### 安装指令

```
pip install crdlog
```

#### 使用方法

```
from crdlog import log
log = log(gen_log=False).logger
log.error('Husky')
```
