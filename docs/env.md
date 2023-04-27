# 开发环境搭建

## 安装编译和测试所需的工具

### 直接安装开发工具包
安装pscdk包，这个包用于编译Python智能合约

```
python3 -m pip install pscdk
```

安装ipyeos包，这个包用于测试智能合约

```
python3 -m pip install ipyeos
```

### 在Docker中运行

目前，该开发工具包不支持Window和Macbook M1/M2，开发工具在这两种平台上需要利用docker来运行。

macOS平台推荐使用[OrbStack](https://orbstack.dev/download)软件来安装docker和运行docker。其它平台可以使用[Docker Desktop](https://www.docker.com/products/docker-desktop)。


下载Docker镜像

```
docker pull ghcr.io/uuosio/pscdk:latest
```

运行container:

```
docker run --entrypoint bash -it --rm -v "$(pwd)":/work -w /work -t ghcr.io/uuosio/pscdk
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
