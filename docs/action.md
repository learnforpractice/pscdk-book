# Action在智能合约的使用

在智能合约中也可以发起一个action，这样的action称之为内联action(inline action)。需要注意的是，action是异步的，也就是说，只有在整个代码执行完后，区块链的代码才会调用对应的action。

示例：

```python
# action_example.codon
from packer import pack
from chain.action import Action
from chain.contract import Contract

@contract(main=True)
class MyContract(Contract):

    def __init__(self):
        super().__init__()

    @action('test')
    def test(self):
        a = Action(n'hello', n'test2', pack("alice"))
        print('++++send test2 action')
        a.send()
        return

    @action('test2')
    def test2(self, name: str):
        print('++++=name:', name)

@export
def apply(receiver: u64, first_receiver: u64, action: u64) -> None:
    from C import __init_codon__() -> i32
    __init_codon__()
    c = MyContract(receiver, first_receiver, action)
    c.apply()
```

测试代码：

```python
def test_action():
    t = init_test('action_example')
    ret = t.push_action('hello', 'test', {}, {'hello': 'active'})
    t.produce_block()
    logger.info("++++++++++%s", ret['elapsed'])
```

输出：

```
debug 2023-03-28T08:13:02.312 thread-0  apply_context.cpp:30          print_debug          ]
[(hello,test)->hello]: CONSOLE OUTPUT BEGIN =====================
++++send test2 action

[(hello,test)->hello]: CONSOLE OUTPUT END   =====================

debug 2023-03-28T08:13:02.312 thread-0  apply_context.cpp:30          print_debug          ] 
[(hello,test2)->hello]: CONSOLE OUTPUT BEGIN =====================
++++=name: alice

[(hello,test2)->hello]: CONSOLE OUTPUT END   =====================
```
可以看到，这里先调用了`test`这个在Transaction里指定了的Action，然后调用了`test2`这个Action，但是`test2`这个action并没有在Transaction里指定，而是在智能合约里发起的。

