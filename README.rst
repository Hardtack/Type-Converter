TypeConverter
==============

Quick and Dirty python type converter.

Install
--------

Install with pip

::

    pip install TypeConverter

Usage
------

You can define a converter with domain like following code.

::

   converter = typeconverter.Converter((list, dict, int, str))

And suppose that we have classes like following.

::

   class A(object):
       def __init__(self, v):
           self.v = v

   class B(A):
       pass

   class C(A):
       pass

   class D(object):
       def __init__(self, v):
           self.v = v

We can define convert functions like

::

   @converter.handle(A)
   def convert_A(a):
       return 'A({0!r})'.format(a.v)


   @converter.handle(B)
   def convert_B(b):
       return 'B({0})'.format(b.v)

   @converter.handle(C)
   def convert_C(c):
       return {
           'value': c,
       }

   @converter.handle(D)
   def convert_D(d):
       return d.v * 2

And we can use converter like

::

   >>> converter.convert(A('foo'))
   A('foo')
   >>> converter.convert(B('bar'))
   B(bar)
   >>> converter.convert(C('baz'))
   {'value': 'baz'}
   >>> converter.convert(D(5))
   10

Surely, we can define handlers for builtin type

::

   @converter.handle(set)
   def convert_set(v):
       return list(v)


TypeConverter also can do chained conversion

::

   class E(object):
       def __init__(self, v1, v2):
           self.v1 = v1
           self.v2 = v2

   
   @converter.handle(E)
   def convert_E(e):
       return {e.v1, e.v2}

::

   >>> converter.convert(E(1, 2))
   [1, 2]
   >>> converter.convert(E(3, 3))
   [3]


We can customize TypeConverter's type assertion

::

   class DeepConverter(typeconverter.Converter):
       def assert_type(self, obj):
           super(DeepConverter, self).assert_type(obj):
           if isinstance(obj, list):
               for item in obj:
                   self.assert_type(item)
           elif isinstnace(obj, dict):
               for k, v in dict.items():
                   self.assert_type(k)
                   self.assert_type(v)


We have to define converters for it.

::

   @converter.handle(dict):
       converted = {}
       for k, v in d.items():
           converted[converter.convert(k)] = converter.convert(v)
       return converted

   @converter.handle(list)
   def convert_list(li):
       return list(map(converter.convert, li))
