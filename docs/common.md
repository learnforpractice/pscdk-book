# 其它常用智能合约函数

## is_account

声明：

```python
def is_account(account: Name ) -> bool:
    ...
```

说明：

用来判断账号存不存在

## has_auth

声明：

```python
def has_auth(account: Name) -> bool:
    ...
```

说明：

用来判断是否有指定账号的`active`权限

## require_auth/require_auth2

声明：

```python
def require_auth(account: Name):
    ...

def require_auth2(account: Name, permission: Name):
    ...
```

说明：

这两个函数在账号不存在或者没有检测到有指定账号的权限时都会抛出异常，不同的是`require_auth`为检测是否存在`active`权限，而`require_auth2`可以检测指定的权限。

## publication_time/current_time

## check

示例代码：

```python
from chain.action import has_auth, require_auth, require_auth2, is_account
from chain.contract import Contract

@contract(main=True)
class MyContract(Contract):

    def __init__(self):
        super().__init__()

    @action('test')
    def test(self):
        has_auth(n"hello")

        require_auth(n"hello")
        require_auth2(n"hello", n"active")

        print(is_account(n"hello"))
        print(is_account(n"hello"))
        return

@export
def apply(receiver: u64, first_receiver: u64, action: u64) -> None:
    from C import __init_codon__() -> i32
    __init_codon__()
    c = MyContract(receiver, first_receiver, action)
    c.apply()
```

编译：
```
python-contract build common_example.codon
```

测试代码：

```python
def test_common():
    t = init_test('common_example')
    ret = t.push_action('hello', 'test', {}, {'hello': 'active'})
    t.produce_block()
    logger.info("++++++++++%s\n", ret['elapsed'])
```

测试：

```
ipyeos -m pytest -s -x test.py -k test_common
```

输出：
```
[(hello,test)->hello]: CONSOLE OUTPUT BEGIN =====================
True
True

[(hello,test)->hello]: CONSOLE OUTPUT END   =====================
```
