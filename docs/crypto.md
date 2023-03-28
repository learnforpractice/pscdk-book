# 密码学相关函数

## assert_sha256

```python
def assert_sha256(data: bytes, hash: Checksum256):
```

## assert_sha1

```python
def assert_sha1(data: bytes, hash: Checksum160):
```

## assert_sha512

```python
def assert_sha512(data: bytes, hash: Checksum512):
```

## assert_ripemd160

```python
def assert_ripemd160(data: bytes, hash: Checksum160):
```

## sha256

```python
def sha256(data: bytes) -> Checksum256:
```

## sha1

```python
def sha1(data: bytes) -> Checksum160:
```

## sha512

```python
def sha512(data: bytes) -> Checksum512:
```

## ripemd160

```python
def ripemd160(data: bytes) -> Checksum160:
```

## recover_key

```python
def recover_key(digest: Checksum256, sig: Signature) -> PublicKey:
```

## assert_recover_key

```python
def assert_recover_key(digest: Checksum256, sig: Signature, pub: PublicKey):
```
