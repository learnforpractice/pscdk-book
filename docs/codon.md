## Codon和Python的差异

1. Codon是静态类型语言
Codon是Python语言的静态类型编译器，代码会直接编译成机器码(binary code)，而不是虚拟机指令(byte code)。创建类的时候会把类的内存直接分配到堆上，并且Codon的内存是靠垃圾回收机制来管理的。

2. 类的方法支持重载,例如：

```python
class SecondaryValue(object):
    def __init__(self, value: u64):
        pass

    def __init__(self, value: u128):
        pass
```

但是要注意的是，模块的函数暂时不支持函数重载

3. Codon里的int类型是64位有符号整数
这和Python里的无限整数不同，一个原因是Codon是静态类型语言，代码会直接编译成机器码(binary code)，而不是虚拟机指令(byte code)。另外一个原因是出于效率的考虑。

4. Codon的数值类型
除了int类型外，Codon中还有这几种数值类型：`u64`, `u128`, `u256`,分别用来表示64位的无符号整数，128位的无符号整数，256位的无符号整数

5. 字符串类型
Codon 目前使用的是 ASCII 字符串，不像 Python 的 unicode 字符串。

6. 字典类型
Codon 的字典类型不保留插入顺序，不像Python那样从3.6开始支持。

