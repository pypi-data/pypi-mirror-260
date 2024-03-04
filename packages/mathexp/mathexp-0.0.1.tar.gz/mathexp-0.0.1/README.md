# MATHematical EXPeriments: `mathexp`

The `mathexp` repo contains a general set symbolic expression utilities, mostly for extending the capabilities of `sympy`. The repo also contains a set of executable scripts for performing various mathematical experiments. Caveat lector.

## Installation

```bash
pip install mathexp
```

## Sample Usage

### Working with integer partitions

```python
from maths.comb import partition

partition.from_str('3+2+1')
>> > IntegerPartition([3, 2, 1])
```

More documentation to come.
