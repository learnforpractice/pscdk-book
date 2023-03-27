# 开发环境搭建

## 安装编译和测试所需的工具

安装pscdk包，这个包用于编译Python智能合约

```
python3 -m pip install pscdk
```

安装ipyeos包，这个包用于测试智能合约

```
python3 -m pip install ipyeos
```

## 测试安装环境是否安装成功：

新建一个测试项目：

```
python-contract init mytest
```

编译合约代码：
```
python-contract build mytest.codon
```

或者直接运行`build.sh`脚本：

```bash
./build.sh
```


不出异常会生成`mytest.wasm`这个WebAssembly的二进制文件

测试：

```
ipyeos -m pytest -s -x test.py -k test_hello
```

或者直接运行测试脚本`test.sh`：

```bash
./test.sh
```

正常会看到输出：

```
hello  alice
```
