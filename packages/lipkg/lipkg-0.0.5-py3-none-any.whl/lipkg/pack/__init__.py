print("我是 顶级包：pack 下的 init文件.导入 pack 其实就是导入我 init文件!!! 所有想到通过pack调用的方法必须都导入我这个文件 I am running ... ")
pack_name = 'pack_name .顶级包：pack 下的 init文件中直接定义的属性'

# 绝对导入：from import 语法 与 import语法皆可使用
# import pack.human

# 相对导入：只能用在 from import 语法中
from . import human
from .dog import *
from . import game
from . import learn

# __all__ 只能控制当执行 from pack import * 语法时，哪些属性会被导入执行文件的名称空间中
__all__ = []


print("我是 顶级包：pack 下的 init文件， run over ...")