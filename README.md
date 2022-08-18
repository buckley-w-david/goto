# goto

Forbidden `goto` magic

```python
>>> from goto import goto
>>> 
>>> @goto
... def f():
...     print("a")
...     print("b")
...     f.goto("end")
...     print("c")
...     f.label("end")
...     print("d")
...     return 5

>>> f()
a
b
d
5
```
