# iterframes: pandas dataframe like interface for iterators

* Primarily pipeline type code.
* iterators of named-tuples.
* primarily for long and narrow data.
* plays nice with itertools library.

## Usage

```
>>> import itertools as it
>>> diag = IterFrame(zip(it.count(1), it.count(1)), ['x','y'], name='Point')
>>> p = next(diag)
>>> print(p)
Point(x=1, y=1)
>>> p.x, p.y
(1, 1)
>>> s = diag.map(sum=lambda p:p.x + p.y, diff=lambda p:p.x - p.y)
>>> next(s)
Point(sum=4, diff=0)
>>> next(diag)
Point(x=5, y=5)
>>> next(diag['x'])
Point(x=6)
>>> next(diag.select('x'))
Point(x=7)
```

## TO DO:

* index slicing via filters
* groupby functionailty with an assumption of a sorted index
* create double iterators of rows and columns (?)



