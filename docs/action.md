---
comments: true
---

# Inline Actions

In smart contracts, you can also initiate an action, which is called an inline action. Keep in mind that actions are asynchronous, meaning that the contract code corresponding to the inline action will only be called after the entire code is executed. If the called contract does not define the relevant action or the account does not have a deployed contract, the call will have no effect, but no exception will be thrown. Empty inline actions like these are not entirely useless, as they can serve as on-chain logs for application queries.

Here is the complete code of the `Action` class in `action.codon`:

```python
@packer
class Action(object):
    account: Name
    name: Name
    authorization: List[PermissionLevel]
    data: bytes

    def __init__(self, account: Name, name: Name, data: bytes=bytes()):
        self.account = account
        self.name = name
        self.authorization = [PermissionLevel(account, n'active')]
        self.data = data

    def __init__(self, account: Name, name: Name, permission_account: Name, data: bytes=bytes()):
        self.account = account
        self.name = name
        self.authorization = [PermissionLevel(permission_account, n'active')]
        self.data = data

    def __init__(self, account: Name, name: Name, permission_account: Name, permission_name: Name, data: bytes=bytes()):
        self.account = account
        self.name = name
        self.authorization = [PermissionLevel(permission_account, permission_name)]
        self.data = data

    def __init__(self, account: Name, name: Name, authorization: List[PermissionLevel], data: bytes=bytes()):
        self.account = account
        self.name = name
        self.authorization = authorization
        self.data = data

    def send(self):
        raw = pack(self)
        send_inline(raw.ptr, u32(raw.len))

    def send(self, data: T, T: type):
        self.data = pack(data)
        raw = pack(self)
        send_inline(raw.ptr, u32(raw.len))
```

This class has three `__init__` functions, which should be used according to needs. The following initialization function should be the most commonly used:

```python
def __init__(self, account: Name, name: Name, data: bytes=bytes())
```

This function uses `active` authorization by default.

The following initialization function specifies which account's authorization to use, and also uses the `active` authorization of the account by default:

```python
def __init__(self, account: Name, name: Name, permission_account: Name, data: bytes=bytes())
```

If a contract uses other authorizations, the following initialization function can be used:

```python
def __init__(self, account: Name, name: Name, permission_account: Name, permission_name: Name, data: bytes=bytes()):
```

If an account has multiple authorizations, the following initialization function can be used:

```python
def __init__(self, account: Name, name: Name, authorization: List[PermissionLevel], data: bytes=bytes()):
```

Example:

```python
# action_example.codon
from packer import pack
from chain.action import Action, PermissionLevel
from chain.contract import Contract

@packer
class Person:
    name: str
    height: u64
    def __init__(self, name: str, height: u64):
        self.name = name
        self.height = height

@contract(main=True)
class MyContract(Contract):

    def __init__(self):
        super().__init__()

    @action('test')
    def test(self):
        a = Action(n'hello', n'test2')
        print('++++send test2 action')
        a.send("1 alice")

        a = Action(n'hello', n'test2', n'hello')
        print('++++send test2 action')
        a.send("2 alice")

        a = Action(n'hello', n'test2', n'hello', n'active')
        print('++++send test2 action')
        a.send("3 alice")

        a = Action(n'hello', n'test2', [PermissionLevel(n"hello", n"active")])
        print('++++send test2 action')
        a.send("4 alice")

        a = Action(n'hello', n'test3')
        print('++++send test3 action')
        a.send(Person("alice", 175u64))
        return

    @action('test2')
    def test2(self, name: str):
        print('++++=name:', name)

    @action('test3')
    def test3(self, name: str, height: u64):
        print('++++=name:', name, 'height:', height)
```

Please note that in order to call inline actions in the contract, the virtual permission `eosio.code` must be added to the `active` permission of the account, and in the test code, the following function is used to add this virtual permission to the `active` permission.

```python
def update_auth(chain, account):
    a = {
        "account": account,
        "permission": "active",
        "parent": "owner",
        "auth": {
            "threshold": 1,
            "keys": [
                {
                    "key": 'EOS6AjF6hvF7GSuSd4sCgfPKq5uWaXvGM2aQtEUCwmEHygQaqxBSV',
                    "weight": 1
                }
            ],
            "accounts": [{"permission":{"actor":account,"permission": 'eosio.code'}, "weight":1}],
            "waits": []
        }
    }
    chain.push_action('eosio', 'updateauth', a, {account:'active'})
```