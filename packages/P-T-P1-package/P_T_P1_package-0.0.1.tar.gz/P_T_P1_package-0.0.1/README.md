Introduction
============

This repository contains the code for the `queues` package. The package
provides three data structures, all with a similar API:

* Stacks (LIFO Queues)
* FIFO Queues
* Ordered Queues

All three data structures are _bounded_ in order to provide more predictable
memory usage.

Usage
=====

> import queues

Stacks
------

### Initialization

Stacks must be initialized with the initial _maximum_ stack size:

```
>>> s = Stack(100)
```

Providing a maximum size that is less than or equal to 0 results in an error.

You can determine the number of items currently on the stack by calling the
`size` method:

```
>>> s.size()
```

### Insertion

Inserting a value into a stack is accomplished by using the `push` method
provided by the stack. The result value for `push` should be a boolean that
signals whether the insertion was successful.

```
>>> s.push(42) # pushes the integer (42) onto the stack
True
```

The `size` of a stack should increase by 1 after every `push`:

```
>>> s.size()
10
>>> s.push(42)
True
>>> s.size()
11
```

### Removal

Getting something from the stack is done using the `pop` method, which takes no
arguments. The result of `pop` should be the _most recently pushed_ value:

```
>>> s.push(42)
True
>>> s.pop()
42
```

Calling `pop` on a non-empty stack should reduce the size by 1.

Calling `pop` on an empty stack should result in `None`.

### Multiple removal

You can remove multiple items from the stack at once using the `pops` method,
which takes an integer as its argument. The result of `pops` is a _list_ of all
the popped elements.

```
>>> s.push(42)
True
>>> s.push(84)
True
>>> s.pops(2)
[84, 42]
```

It is okay to call `pops` with a number larger than the size of the stack, in
which case the resulting list will include all the elements of the stack and no
more.

Calling `pops(n)` on a non-empty stack should reduce the size by `n` or reduce
the size to 0.

Calling `pops` on an empty stack should result in the empty list.




FIFO Queues
-----------

### Initialization

Queues must be initialized with the initial _maximum_ size:

```
>>> q = FIFO(100)
```

Providing a maximum size that is less than or equal to 0 results in an error.

You can determine the number of items currently in the queue by calling the
`size` method:

```
>>> q.size()
```

### Insertion

Inserting a value into the queue is accomplished by using the `insert` method
provided by the queue. The result value for `insert` should be a boolean that
signals whether the insertion was successful.

```
>>> q.insert(42) # adds the integer (42) to the end of the queue
True
```

The `size` of a queue should increase by 1 after every `insert`:

```
>>> q.size()
10
>>> q.insert(42)
True
>>> q.size()
11
```

### Removal

Getting something from the queue is done using the `get` method, which takes no
arguments. The result of `get` should be the oldest value in the queue:

```
>>> q.insert(42)
True
>>> q.insert(84)
True
>>> q.get()
42
```

Calling `get` on a non-empty queue should reduce the size by 1.

Calling `get` on an empty queue should result in `None`.

### Multiple removal

You can remove multiple items from the queue at once using the `gets` method,
which takes an integer as its argument. The result of `gets` is a _list_ of all
the retrieved elements.

```
>>> q.insert(42)
True
>>> q.insert(84)
True
>>> q.gets(100000000)
[84, 42]
```

It is okay to call `gets` with a number larger than the size of the queue, in
which case the resulting list will include all the elements of the queue and no
more.

Calling `gets(n)` on a non-empty queue should reduce the size by `n` or reduce
the size to 0.

Calling `gets` on an empty queue should result in the empty list.



Ordered Queues
--------------

Ordered Queues store all of their elements _in ascending order_.

The data structure provides the same methods as the FIFO Queue,
but the behavior is slightly different.

### Initialization

OQs must be initialized with the initial _maximum_ size:

```
>>> q = OQ(100)
```

Providing a maximum size that is less than or equal to 0 results in an error.

You can determine the number of items currently in the queue by calling the
`size` method:

```
>>> q.size()
```

### Insertion

Inserting a value into the queue is accomplished by using the `insert` method
provided by the queue. The result value for `insert` should be a boolean that
signals whether the insertion was successful.

```
>>> q.insert(42) # adds the integer (42) to the queue
True
```

The `size` of a queue should increase by 1 after every `insert`:

```
>>> q.size()
10
>>> q.insert(42)
True
>>> q.size()
11
```

### Removal

Getting something from the queue is done using the `get` method, which takes no
arguments. The result of `get` should be the _smallest_ integer in the queue.

```
>>> q.insert(42)
True
>>> q.insert(21)
True
>>> q.insert(84)
True
>>> q.get()
21
```

Calling `get` on a non-empty queue should reduce the size by 1.

Calling `get` on an empty queue should result in `None`.

### Multiple removal

You can remove multiple items from the queue at once using the `gets` method,
which takes an integer as its argument. The result of `gets` is a _list_ of all
the retrieved elements.

```
>>> q.insert(42)
True
>>> q.insert(21)
True
>>> q.insert(84)
True
>>> q.gets(2)
[21, 42]
```

It is okay to call `gets` with a number larger than the size of the queue, in
which case the resulting list will include all the elements of the queue and no
more.

Calling `gets(n)` on a non-empty queue should reduce the size by `n` or reduce
the size to 0.

Calling `gets` on an empty queue should result in the empty list.

