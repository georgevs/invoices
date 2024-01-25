"""
and_ = (fn...) -> x -> bool
branch :: (fn, ...) -> fn
compose :: (fn, ...) -> fn
converge :: (fn, [fn]) -> fn
falsy :: x -> bool
group_by :: (x -> k) -> [x] -> [[k, x]]
group_value_lens :: lens [k, x]
identity :: x -> x
ifilter :: (x -> bool) -> [x] -> [x]
iflatten :: [[x], ...] -> [x, ...]
imap :: (x -> y) -> [x] -> [y]
ipick :: (k, ...) -> { k -> x } -> (x, ...)
ipicks :: ('a.b.c', ...) -> { 'a' -> { 'b' -> { 'c' -> x }}, ...} -> (x, ...)
itake :: n -> [x] -> [x]
izip :: ([x], ...) -> [y] -> [(x, ..., y)]
join_str :: d -> [x] -> 'x' + d + ...
lens store :: { view :: store -> view, set :: (x, store) -> store }
lens_over :: (lens, fn, store) -> store
lens_set :: (lens, value, store) -> store
lens_view :: (lens, store) -> view
not_ = (x -> bool) -> x -> bool
or_ = (fn...) -> x -> bool
over_group_value :: (x -> y) -> [k, x] -> [k, y]
pick :: k -> { k -> x } -> x
picks :: 'a.b.c' -> { 'a' -> { 'b' -> { 'c' -> x }}} -> x
pipe :: (fn, ...) -> fn
replace_str = (src, dst) -> x -> x
sort_by :: (x -> k) -> [x] -> [x]
strip_str :: ds -> x -> x
truthy :: x -> bool
"""

from functools import partial, reduce 
from itertools import chain, groupby, islice

pipe = lambda *fns: reduce(lambda acc, fn: lambda x: fn(acc(x)), fns)
compose = lambda *fns: pipe(*reversed(fns))
branch = lambda *fns: lambda x: (fn(x) for fn in fns)
converge = lambda fn0, fns: pipe(
    lambda x: (fn(x) for fn in fns), 
    lambda xs: fn0(*xs)
)

falsy = lambda x: not(x)
truthy = lambda x: not(falsy(x))

not_ = lambda fn: lambda x: not(fn(x))
or_ = lambda *fns: reduce(lambda acc, fn: lambda x: acc(x) or fn(x), fns)
and_ = lambda *fns: reduce(lambda acc, fn: lambda x: acc(x) and fn(x), fns)

imap = lambda fn: partial(map, fn)
ifilter = lambda fn: partial(filter, fn)
izip = lambda *xss: partial(zip, *xss)
iflatten = chain.from_iterable
itake = lambda n: lambda xs: islice(xs, n)

identity = lambda x: x

pick = lambda k: lambda x: x[k]
ipick = lambda *ks: lambda x: (x[k] for k in ks)
picks = lambda ks: reduce(lambda fn, k: lambda x: fn(x)[k], ks.split('.'), identity) 
ipicks = lambda *kss: branch(*(picks(ks) for ks in kss))
# example: pipe(ipicks('a.b','d'), izip(['x','y']), dict)({'a': {'b':2, 'c': 3 }, 'd': 4 })

lens_view = lambda lens, store: lens.view(store)
lens_set = lambda lens, value, store: lens.set(value, store)
lens_over = lambda lens, fn, store: lens_set(lens, fn(lens_view(lens, store)), store)

class group_value_lens:
  @staticmethod
  def view(group): return group[1]
  @staticmethod
  def set(value, group): return (group[0], value)

over_group_value = lambda fn: partial(lens_over, group_value_lens, fn)

sort_by = lambda fn: partial(sorted, key=fn)
group_by = lambda fn: partial(groupby, key=fn)

join_str = lambda delim: delim.join
strip_str = lambda chars = None: lambda xs: xs.strip(chars)
replace_str = lambda src, dst: lambda x: x.replace(src, dst)
