---
comments: true
---

# Codon代码与C代码的相互调用

## 在Codon代码里调用C代码
```python
from C import say_hello(cobj, int) -> None

```

## 在C代码里调用Codon代码
```python
@export
def print_string(a: cobj， len: int) -> int:
    return int(strlen(a))
```
