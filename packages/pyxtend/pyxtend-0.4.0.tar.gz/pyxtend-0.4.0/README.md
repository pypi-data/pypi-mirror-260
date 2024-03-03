# pyxtend

Functions to be more productive in Python.

## struct

`struct` is for examining objects to understand their contents.

## Example 1
A simple list of integers

```python
Input: [1, 2, 3, 4, 5]
Output (without examples): {'list': ['int', 'int', 'int', '...5 total']}
Output (with examples): {'list': [1, 2, 3, '...5 total']}
```

## Example 2
A list of lists

```python
Input: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
Output (without examples): {'list': [{'list': ['int', 'int', 'int']}, {'list': ['int', 'int', 'int']}, {'list': ['int', 'int', 'int']}]}
Output (with examples): {'list': [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}
```
