'''
Pandas-type dataframes, but with iterators.
The idea is that pandas pipeline-type code + column slicing
should work with iterators (bonus: spark and dask functionality)'''


import collections as c

class IterFrame(object):
    '''
    Iterframe class provides a pandas dataframe like interface for iterators.
    '''
    
    def __init__(self, it, cols, name='Row'):
        '''
        return an iterator with same data as the input iterator,
        with data accessable using column names specified by cols.
        '''
        self._name = name
        self._make = c.namedtuple(self._name, cols)
        self._iter = it
        

    def __iter__(self):
        for line in self._iter:
            try:
                yield self._make(*line)
            except TypeError:
                yield self._make(*(line,))

    def __next__(self):
        try:
            return self._make(*next(self._iter))
        except TypeError:
            return self._make(*(self._iter,))

    def __getitem__(self, cols):
        '''slice columns from an iterframe, returning a sliced iterframe'''
        if not isinstance(cols, tuple):
            cols = tuple(cols)
            
        it = ([x.__getattribute__(c) for c in cols] for x in self)
        return IterFrame(it, cols, self._name)

    def select(self, *cols):
        '''slice columns from an iterframe, returning a sliced iterframe'''
        # slices the columns / returns another DataIter
        it = ([x.__getattribute__(c) for c in cols] for x in self)
        return IterFrame(it, cols, self._name)
    
    def map(self, **funcargs):
        '''apply function(s) to an iterframe, returning a mapped iterframe'''
        funcs = [x for x in funcargs.items()]
        it = ([f(row) for _, f in funcs] for row in self)
        return IterFrame(it, [name for name, _ in funcs], self._name)

    def filter(self, func):
        '''apply a filter function to an iterframe, returning a filtered iterframe'''
        it = (row for row in self if func(row))
        return IterFrame(it, self._make._fields)
    
    def rename(self, **coldict):
        '''rename the columns of an iterframe, returning a new iterframe'''
        newcols = [coldict[c] for c in self._make._fields]
        return IterFrame(self._iter, newcols)
    
    
