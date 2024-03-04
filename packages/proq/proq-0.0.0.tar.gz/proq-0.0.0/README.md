# Process Queue

Simplify data processing using multiprocesses and queues.

```python
import proq

# multiply by 3, keep even, count
proq.create([1,2,3,4,5]).map(lambda x: x * 3).filter(lambda x: x % 2 == 0).count()
```


```python
import proq

# Create a data queue
data1 = proq.create([1,2,3,4,5])

# multiply by 3
data2 = proc.map_(data1, lambda x: x * 3)

# keep elements divisible by 2
data3 = proc.filter_(data2, lambda x: x % 2 == 0)

# count
count = proc.count(data3)
```

# Installation

```bash
pip install proq
```

#  Development

* Download source
* Install development dependencies: `flit install -s --deps develop`
* Format code: `black .`
* Run tests: `pytest`
* Bump version in `src/proq/__init__.py`
* Build package: `flit build`
* Deploy: `flit publish`
