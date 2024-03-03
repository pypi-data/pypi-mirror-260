'''
一个简单的基于 JSON 的键-值存储类。它提供了一种方便的方法来操作 JSON 文件，与操作 Python 字典类似，但每次修改后都会自动进行持久化。
'''

from json import loads as jsonLoads
from json import dumps as jsonDumps
from pathlib import Path


class WSS:
    def __init__(self, fpath: str):
        self.fpath = Path(fpath)
        try:
            self.core = jsonLoads(self.fpath.read_text(encoding='utf8'))
        except:
            self.core = {}

    def _save(self):
        if not self.fpath.parent.exists():
            self.fpath.parent.mkdir(parents=True)
        self.fpath.write_text(jsonDumps(self.core, ensure_ascii=False), encoding='utf8')

    def __getitem__(self, key):
        return self.core[key]

    def __setitem__(self, key, value):
        self.core[key] = value
        self._save()

    def update(self, *args, **kwargs):
        self.core.update(*args, **kwargs)
        self._save()

    def keys(self): return self.core.keys()

    def values(self): return self.core.values()

    def items(self): return self.core.items()

    def pop(self, *args, **kwargs):
        result = self.core.pop(*args, **kwargs)
        self._save()
        return result

    def get(self, key, default=None):
        return self.core.get(key, default)
    
    def setdefault(self, key, default=None):
        if key in self.core:
            return self.core[key]
        else:
            result = self.core.setdefault(key, default)
            self._save()
            return result

    def __ior__(self, other):
        self.core |= other
        self._save()
        return self

    def __len__(self):
        return len(self.core)

    def __iter__(self):
        return self.core.__iter__()


'''
# 教程

## 初始化

首先，初始化一个实例：

```python
store = WSS('path/to/your/file.json')
```

## 增加键

要增加一个键，只需像操作字典那样赋值：

```python
store['new_key'] = 'new_value'
```

此操作将立即写入文件。

## 删除键

使用 `pop` 方法删除指定的键并返回其值：

```python
removed_value = store.pop('key_to_remove')
```

如果指定的键不存在，`pop` 会抛出一个 `KeyError` 。如果你想避免这个错误并在键不存在时返回一个默认值，你可以这样做：

```python
removed_value = store.pop('key_to_remove', default_value)
```

## 更新键

使用 `update` 方法一次更新多个键：

```python
store.update({'key1': 'updated_value1', 'key2': 'updated_value2'})
```

或者你可以简单地为每个键分别赋值：

```python
store['key1'] = 'updated_value1'
```

## 查询键

要查询键的值，只需像操作字典那样：

```python
value = store['key_to_query']
```

如果该键不存在，此操作会抛出一个 `KeyError` 。为避免错误，你可以使用 `get` 方法：

```python
value = store.get('key_to_query', 'default_value')
```

## 其他常用方法

- 获取所有的键、值或键值对：

  ```python
  keys = store.keys()
  values = store.values()
  items = store.items()
  ```
- 如果键不存在，则设置其默认值：

  ```python
  store.setdefault('absent_key', 'default_value')
  ```
  如果键 `absent_key` 不存在于 `WSS` 中，它将被添加，并赋予 `default_value` 作为值。
- 合并两个 `WSS` 对象或字典：

  ```python
  other_data = {'key5': 'value5'}
  store |= other_data
  ```
  这将把 `other_data` 的内容合并到 `store` 中，如果有任何重复的键，`store` 中的值将被 `other_data` 中的值覆盖。
- 获取 `WSS` 对象中的项数：

  ```python
  length = len(store)
  ```
- 迭代 `WSS` 对象中的键：

  ```python
  for key in store:
      print(key)
  ```
'''