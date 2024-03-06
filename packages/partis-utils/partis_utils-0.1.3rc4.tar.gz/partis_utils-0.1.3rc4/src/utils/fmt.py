# -*- coding: UTF-8 -*-
from __future__ import annotations
import sys
import os
import gc
import inspect
import weakref
from inspect import getframeinfo, stack
import logging
import pprint
import traceback
import linecache
import re
from copy import copy, deepcopy
from datetime import datetime

import rich
import rich.highlighter
import rich.console
from rich.text import (
  Span,
  Lines,
  Text )

from collections import (
  namedtuple,
  deque)
from collections.abc import (
  Mapping,
  Sequence,
  Set,
  Iterable )

log = logging.getLogger(__name__)

# NOTE: this console should only be used where operation on Text needs it,
# not for rendering
_console = rich.console.Console(
  color_system = 'standard',
  force_terminal = False,
  force_jupyter = False,
  force_interactive = False,
  soft_wrap = False,
  tab_size = 2,
  width = 100,
  height = 100,
  no_color = False)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ReprHighlighter(rich.highlighter.RegexHighlighter):
  """Notes: slight modifications to the patterns in rich.highlighter.ReprHighlighter"""

  base_style = "repr."
  highlights = [
    r"(?P<tag_start><)(?P<tag_name>[-\w.:|]*)(?P<tag_contents>[\w\W]*?)(?P<tag_end>>)",
    r"(?P<attrib_name>[a-zA-Z_][a-zA-Z0-9_]{0,50}(\.[a-zA-Z_][a-zA-Z0-9_]{0,50})+)",
    # r'(?P<attrib_name>[\w_]{1,50})=(?P<attrib_value>"?[\w_]+"?)?',
    r"(?P<brace>[][{}()])",
    rich.highlighter._combine_regex(
      r"(?P<ipv4>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})",
      r"(?P<ipv6>([A-Fa-f0-9]{1,4}::?){1,7}[A-Fa-f0-9]{1,4})",
      r"(?P<eui64>(?:[0-9A-Fa-f]{1,2}-){7}[0-9A-Fa-f]{1,2}|(?:[0-9A-Fa-f]{1,2}:){7}[0-9A-Fa-f]{1,2}|(?:[0-9A-Fa-f]{4}\.){3}[0-9A-Fa-f]{4})",
      r"(?P<eui48>(?:[0-9A-Fa-f]{1,2}-){5}[0-9A-Fa-f]{1,2}|(?:[0-9A-Fa-f]{1,2}:){5}[0-9A-Fa-f]{1,2}|(?:[0-9A-Fa-f]{4}\.){2}[0-9A-Fa-f]{4})",
      r"(?P<uuid>[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})",
      r"(?P<call>[\w.]*?)\(",
      r"\b(?P<bool_true>True)\b|\b(?P<bool_false>False)\b|\b(?P<none>None)\b",
      r"(?P<ellipsis>\.\.\.)",
      r"(?P<number_complex>(?<!\w)(?:\-?[0-9]+\.?[0-9]*(?:e[-+]?\d+?)?)(?:[-+](?:[0-9]+\.?[0-9]*(?:e[-+]?\d+)?))?j)",
      r"(?P<number>(?<!\w)\-?[0-9]+\.?[0-9]*(e[-+]?\d+?)?\b|0x[0-9a-fA-F]*)",
      r"(?P<path>([-\w._+]+)?(/[-\w._+]+)*\/)(?P<filename>[-\w._+]*)?",
      r"(?<![\\\w])(?P<literal>\`.*?(?<!\\)\`)",
      r"(?<![\\\w])(?P<str>b?'''.*?(?<!\\)'''|b?'.*?(?<!\\)'|b?\"\"\".*?(?<!\\)\"\"\"|b?\".*?(?<!\\)\")",
      r"(?P<url>(file|https|http|ws|wss)://[-0-9a-zA-Z$_+!`(),.?/;:&=%#]*)" ) ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class LiteralHighlighter(rich.highlighter.RegexHighlighter):

  base_style = ""
  highlights = [
    rich.highlighter._combine_regex(
      r"(?P<punctuate>[\]\[\{\}\(\)\.\,\'\"\`:\/@\*?=&])",
      r"(?P<omit>\~\~\~)" ) ]

repr_patterns = ReprHighlighter.highlights

repr_rec = re.compile('|'.join(repr_patterns))

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def do_pprint( value ):
  if isinstance( value, dict ) or isinstance( value, list ) or isinstance( value, tuple ):
    return True

  return False

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def as_rich(msg):
  if isinstance(msg, Text):
    msg = msg.copy()

  else:
    if isinstance(msg, str):
      msg = inspect.cleandoc(msg)

    else:
      msg = fmt_obj(
        msg,
        width = 100,
        height = 1 )

    msg = Text(msg)


  return msg

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def rich_time(time):

  time = datetime.fromtimestamp(time)

  return (
    Text(f"{time.year:04d}-{time.month:02d}-{time.day:02d}",
      'date')
    + Text(" ", 'none')
    + Text(
      f"{time.hour:02d}:{time.minute:02d}:{time.second:02d}",
      'time')
    + ( Text(
      f".{time.microsecond:06d}",
      'time_us') if time.microsecond > 0.0 else Text('') ) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def fmt_src_line( obj ):
  """Formats source file and line of a given object

  Returns
  -------
  text : str

    File /path/to/file, Line #
  """

  src_line = ""

  try:
    src_line += f"File {inspect.getfile(obj)}"

    try:
      src_line += f", Line {inspect.getsourcelines(obj)[1]}"
    except:
      pass
  except:
    pass

  return src_line

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def join_attr_path(parts):
  path = parts[0]

  if isinstance(path, int):
    path = f"[{path}]"

  for k in parts[1:]:
    if isinstance(k, int):
      path += f"[{k}]"
    else:
      path += f".{k}"

  return path

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def split_attr_path(path):
  return re.sub(r'\]', '', re.sub(r'\[', '.', path)).split('.')

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def split_lines( text ):
  """Split a string into lines.

  Note: this differs from str.splitlines to return ['',] for an empty string
  instead of raising an exception.
  """
  if not isinstance( text, (str, Text) ):
    raise ValueError(f"must be string: {text}")

  if len(text) == 0:
    return [type(text)(''),]

  if isinstance(text, Text):
    return text.split('\n')

  return text.splitlines()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def wrap_lines(text, width):
  return [ w for t in split_lines(text) for w in wrap_line(t, width) ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def wrap_line(text, width):

  if isinstance(text, Text):
    return text.wrap(_console, width = width)

  return textwrap.wrap(str(text), width = width)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def indent_lines(
  n,
  lines,
  *,
  mark = "",
  ind = "",
  start = 0 ):
  """Indents each line of a string, adding a marker at the begining of the first line

  Parameters
  ----------
  n : int
    Number of spaces to indent each line
  lines : str | list[str]
    Message to indent, of one or more lines
  mark : string
    Marker of first line
  start : int
    Indents lines starting at this line
  """

  if n == 0:
    return lines

  if not mark:
    mark = ind

  is_str = False

  if isinstance( lines, (str, Text) ):
    is_str = True
    lines = split_lines( lines )

  elif len(lines) == 0:
    return lines

  cls = type(lines[0])
  mark = cls(" " * ( max(0, n - len(mark) ) )) + mark
  ind = cls(" " * ( max(0, n - len(ind) ) )) + ind

  if not isinstance( lines, (list, rich.text.Lines) ):
    raise ValueError(f"lines must be string or list of strings: {type(lines)}")

  _lines = lines[start:]

  if len(_lines) > 0:
    _lines[0] = mark + _lines[0]

  _lines[1:] = [ ind + s for s in _lines[1:] ]

  lines[start:] = _lines

  if is_str:
    return cls("\n").join( lines )
  else:
    return lines

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def line_segment( text, sep, offset ):
  """finds contiguous sequence of characters at the position
  """

  #
  segs = re.split( sep, text )
  nseg = len(segs)
  ncols = [ (len(s) + 1) for s in segs ]

  ends = copy(ncols)

  for i in range(1, nseg):
    ends[i] = ends[i-1] + ends[i]

  starts = [ (b - w) for b,w in zip(ends, ncols) ]

  for idx, (start, end) in enumerate(zip(starts, ends)):
    if (offset >= start) and (offset < end):
      return idx, segs[ idx ]

  return None

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def fmt_base_or_type(
  obj,
  sleft = '\'',
  sright = '\'',
  tleft = '`',
  tright = '`' ):
  """Formats into a type-name for non-trivial objects, except bool, int, float, str
  """

  if isinstance( obj, type ):
    return tleft + obj.__name__ + tright

  if isinstance( obj, str ):
    return sleft + obj + sright

  if any( isinstance( obj, t ) for t in [ bool, int, float, complex ] ):
    return str(obj)

  return tleft + type(obj).__name__ + tright


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def fmt_array( obj ):
  """Format information about array-like objects.

  This uses duck-typing to determine if the object is array-like, with support
  for GPU device array objects such as PyCUDA.

  Returns
  -------
  fmt : str | None
    May return ``None`` if the object does not appear to be an array
  """

  name = type(obj).__name__

  args = list()
  kwargs = dict()
  array_like = False
  values = ''

  shape = getattr(obj, 'shape', None)

  if isinstance(shape, (tuple,list)):
    if len(obj.shape) == 0:
      # format as scalar
      return None

    kwargs['shape'] = obj.shape
    array_like = True

    try:
      if len(shape) == 1 and shape[0] <= 10:
        args.append(str(obj))
    except Exception:
      traceback.print_exc()
      pass

  else:
    try:
      length = len(obj)
      if isinstance(length, int):
        kwargs['length'] = length

        if length <= 10:
          args.append(str(obj))
    except Exception:
      pass

  # numpy.ndarray, array.array, memoryview, ...
  for attr in ['dtype', 'typecode']:
    dtype = getattr(obj, attr, None)
    if dtype is not None:
      kwargs[attr] = str(dtype)
      # dtype alone not enough to say its an array
      # array_like = True
      break

  # various 'flags' that affect array behaviour (memoryview, numpy, GPUArray)
  _flags = [
    ('writable', 'W'),
    ('WRITEABLE', 'W'),
    ('readonly', 'R'),
    ('OWNDATA', 'O'),
    ('aligned', 'A'),
    ('ALIGNED', 'A'),
    ('f_contiguous', 'F'),
    ('F_CONTIGUOUS', 'F'),
    ('c_contiguous', 'C'),
    ('C_CONTIGUOUS', 'C')]

  flags = list()

  for f, short in _flags:

    try:
      if getattr(obj.flags, f):
        flags.append(short)
        array_like = True
        continue
    except:
      pass

    try:
      if obj.flags[f]:
        flags.append(short)
        array_like = True
        continue
    except:
      pass

    try:
      if getattr(obj, f):
        flags.append(short)
        array_like = True
        continue
    except:
      pass

  if not array_like:
    return None

  if len(flags) > 0:
    kwargs['flags'] = '|'.join(set(flags))

  _kwargs = ", ".join(args + [f"{k}={v}" for k,v in kwargs.items()])

  return f"{name}({_kwargs})"

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def fmt_limit( v, width = -1, height = -1 ):
  """Creates string representation limited in width (columns) and/or height (lines)

  Parameters
  ----------
  obj : obj | list[ obj ]


  Parameters
  ----------
  text : obj | list[ obj ]
  """

  if isinstance( v, list ):
    return [ fmt_limit(_v, width, height ) for _v in v ]

  try:
    v = str(v)
  except:
    try:
      return v.__name__
    except:
      try:
        return v.__class__.__name__
      except:
        return f"{type(v)} id({id(v)})"

  v = split_lines( v )

  if len(v) == 1:
    _v = v[0]

    if width > 0 and len(_v) > width:
      # limit the width of one line
      i0 = ( width + 1 ) // 2
      i1 = max( i0, len(_v) - ( width // 2 ) )
      _v = _v[:i0] + "|...|" + _v[i1:]

      v[0] = _v

  else:

    if height > 0 and len(v) > height:

      if height < 3:
        # not enough lines to include ellipses
        v = v[:height]

      elif len(v) > height:
        # limit the number of lines
        j0 = ( height + 1 ) // 2
        j1 = max( j0, len(v) - ( height // 2 ) )

        # fill middle line with an ellipses indicating skipped lines
        v = v[:j0] + [ "...", ] +  v[j1:]

      # limit the width of each line (ignore height)
      v = [ fmt_limit( _v, width ) for _v in v ]

  v = "\n".join(v)

  return v



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def fmt_iterable(
  obj,
  begin = '[ ',
  end = ' ]',
  empty = "",
  sep = ', ',
  sep_2 = ', ',
  sep_term_n = ', ',
  **fargs ):

  if isinstance( obj, str ):
    return obj

  if not isinstance( obj, Iterable ):
    return fmt_base_or_type(obj, **fargs)

  elements = [ fmt_base_or_type(x, **fargs) for x in obj ]

  if len(elements) == 0:
    fmt = empty

  elif len(elements) == 1:
    fmt = elements[0]

  elif len(elements) == 2:
    fmt = sep_2.join(elements)

  else:
    fmt = sep.join(elements[:-1]) + sep_term_n + elements[-1]

  return begin + fmt + end

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def fmt_iterable_or( obj, **fargs ):
  return fmt_iterable(
    obj = obj,
    begin = '',
    end = '',
    empty = "",
    sep = ', ',
    sep_2 = ' or ',
    sep_term_n = ', or ',
    **fargs )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def fmt_iterable_and( obj, **fargs ):
  return fmt_iterable(
    obj = obj,
    begin = '',
    end = '',
    empty = "",
    sep = ', ',
    sep_2 = ' and ',
    sep_term_n = ', and ',
    **fargs )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class f:
  """Formatting utility class

  If string, the argument is interpreted as a format string, substituting
  args and kwargs using `.format(*args, **kwargs)`. Evaluation of the formatter
  is delayed until the __str__ function is called on the instance.

  .. code-block:: python

    logging.debug( f("hello {who}", who = "world") )

  If a callable, it is expected the instance to be used as a function decorator.
  The callable (such as a logging function) is expected to call __str__, at which
  point the decorated function is evaluated, using the return value as the string
  representation. In this case, the extra args and kwargs are passed to the callable,
  instead of being used as formatting arguments.

  For example, to create a logging debug message, evaluating the debug code
  only when debug level logging is enabled

  .. code-block:: python

    @f( logging.debug )
    def debug_message():
      return f("some {} {}", "debug", "info")

  .. code-block:: python

    try:
      raise Exception("some exception")
    except:

      @f( logging.debug, exc_info = True )
      def debug_message():
        return f("some extra {}", "debugs")

  Parameters
  ----------
  arg : str, callable
    string, format string, or logging callable
  *args
    positional arguments passed to formatter

  **kwargs
    key-word arguments passed to formatter
  """
  #-----------------------------------------------------------------------------
  def __init__( self, arg, *args, **kwargs ):
    self._arg = arg
    self._args = args
    self._kwargs = kwargs
    self._func = None

  #-----------------------------------------------------------------------------
  def __str__( self ):

    if self._func is not None:
      # call function to generate message
      return str(self._func())

    if len(self._args) > 0 or len(self._kwargs) > 0:

      # format dictionaries
      args = [
        pprint.pformat(arg) if do_pprint( arg ) else arg
        for arg in self._args ]

      kwargs = { kw: pprint.pformat(arg) if do_pprint( arg ) else arg
        for kw,arg in self._kwargs.items() }

      return self._arg.format( *args, **kwargs )
    else:
      return self._arg

  #-----------------------------------------------------------------------------
  def __call__( self, func ):
    """Use instance as function decorator
    """

    # function to generate the actual message
    self._func = func

    # _arg here is interpreted as the logger to emit the message to, expecting
    # it to call str( ... ) on `self` if the message is to be logged
    self._arg( self, *self._args, **self._kwargs )

    # may be used as function decorator, so return function
    return func

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StringFunction(str):
  """A string that is evaluated from a function
  """
  #-----------------------------------------------------------------------------
  def __new__( cls, func = None ):
    return str.__new__( cls )

  #-----------------------------------------------------------------------------
  def __init__( self, func = None ):
    str.__init__( self )

    self._func = func

  #-----------------------------------------------------------------------------
  def __add__( self, *args, **kwargs ):
    return str.__add__(self._str, *args, **kwargs)

  #-----------------------------------------------------------------------------
  def __contains__( self, *args, **kwargs ):
    return str.__contains__(self._str, *args, **kwargs)

  #-----------------------------------------------------------------------------
  def __eq__( self, *args, **kwargs ):
    return str.__eq__(self._str, *args, **kwargs)

  #-----------------------------------------------------------------------------
  def __ne__( self, *args, **kwargs ):
    return str.__ne__(self._str, *args, **kwargs)

  #-----------------------------------------------------------------------------
  def __ge__( self, *args, **kwargs ):
    return str.__ge__(self._str, *args, **kwargs)

  #-----------------------------------------------------------------------------
  def __gt__( self, *args, **kwargs ):
    return str.__gt__(self._str, *args, **kwargs)

  #-----------------------------------------------------------------------------
  def __le__( self, *args, **kwargs ):
    return str.__le__(self._str, *args, **kwargs)

  #-----------------------------------------------------------------------------
  def __lt__( self, *args, **kwargs ):
    return str.__lt__(self._str, *args, **kwargs)

  #-----------------------------------------------------------------------------
  def __format__( self, *args, **kwargs ):
    return str.__format__(self._str, *args, **kwargs)

  #-----------------------------------------------------------------------------
  def __mod__( self, *args, **kwargs ):
    return str.__mod__(self._str, *args, **kwargs)

  #-----------------------------------------------------------------------------
  def __mul__( self, *args, **kwargs ):
    return str.__mul__(self._str, *args, **kwargs)

  #-----------------------------------------------------------------------------
  def __reduce__( self, *args, **kwargs ):
    return str.__reduce__(self._str, *args, **kwargs)

  #-----------------------------------------------------------------------------
  def __reduce_ex__( self, *args, **kwargs ):
    return str.__reduce_ex__(self._str, *args, **kwargs)

  #-----------------------------------------------------------------------------
  def __rmod__( self, *args, **kwargs ):
    return str.__rmod__(self._str, *args, **kwargs)

  #-----------------------------------------------------------------------------
  def __rmul__( self, *args, **kwargs ):
    return str.__rmul__(self._str, *args, **kwargs)

  #-----------------------------------------------------------------------------
  def __sizeof__( self, *args, **kwargs ):
    return str.__sizeof__(self._str, *args, **kwargs)

  #-----------------------------------------------------------------------------
  def __len__( self ):
    return str.__len__(self._str)

  #-----------------------------------------------------------------------------
  def __str__( self ):
    return str.__str__( self._str )

  #-----------------------------------------------------------------------------
  def __repr__( self ):
    return str.__repr__(self._str)

  #-----------------------------------------------------------------------------
  def __hash__( self ):
    return str.__hash__( self._str )

  #-----------------------------------------------------------------------------
  def __iter__( self ):
    return str.__iter__( self._str )

  #-----------------------------------------------------------------------------
  def __getattribute__( self, name ):

    _func = object.__getattribute__( self, '_func' )

    if _func is None:
      _str = ""
    else:
      _str = str(_func())

    if name == '_str':
      return _str

    try:
      return getattr( _str, name )
    except AttributeError:
      # raise normal looking attribute error
      raise AttributeError("'{}' object has no attribute '{}'".format(
        self.__class__.__name__,
        name ) )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def _fmt_obj(
  obj,
  width = None,
  height = None,
  multiline = False,
  method = str):


  try:

    if isinstance(obj, type):
      # obj = get_origin(obj) or obj

      # if type(obj) is not type:
      #   return f"`{obj.__name__}` <{type(obj).__name__}>"

      # format type classes
      return f"{obj.__name__}"

    arr_str = fmt_array(obj)

    if arr_str:
      # check for array-like first, since some array interfaces (e.g. PyCUDA)
      # may not be recognized specifically as a sequence
      return arr_str

    if isinstance( obj, str ):
      if '\n' in obj or repr_rec.fullmatch(obj):
        # don't quote multiline strings, or strings that are a common representation
        return obj

      if "'" in obj:
        # use double quote if the string contains single quotes
        # NOTE: even if there is a mix of single/double quotes,
        return '"' + obj + '"'

      # default to single quotes
      return "'" + obj + "'"

    elif isinstance( obj, Sequence ):

      _obj = ", ".join([fmt_obj(v, width = width, height = height, method = method) for v in obj ])

      if isinstance( obj, tuple ):
        if len(obj) == 1:
          return "(" + _obj + ",)"
        else:
          return "(" + _obj + ")"
      else:
        return "[" + _obj + "]"

    elif isinstance( obj, Mapping ):
      if multiline and len(obj) > 1:
        return '{\n' + indent_lines( 2, ',\n'.join([
          fmt_obj(k) + " : " + fmt_obj(v, width = width, height = height, multiline = multiline, method = method)
          for k, v in obj.items() ]) ) + " }"

      else:
        return '{' + ', '.join([
          fmt_obj(k) + ": " + fmt_obj(v, width = width, height = height, multiline = multiline, method = method)
          for k, v in obj.items() ]) + "}"


    else:
      return method(obj)

  except:
    # import traceback
    # traceback.print_exc()
    # log.exception( f"Could not format object", exc_info = True )
    pass

  try:
    return str(obj.__name__)
  except:
    pass

  try:
    return f"id({id(obj)}) <{type(obj).__name__}>"
  except:
    pass

  return "<unknown>"

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def fmt_obj(
  obj,
  width = None,
  height = None,
  multiline = False,
  method = str):
  """Formats a general Python object into a string for the purpose of logging or error

  This is nearly guaranteed to return a string without raising any exception,
  with multiple fallbacks if standard formatting fails.

  Parameters
  ----------
  obj : object
  width : None | int
    Maximum final number of columns per line.
    If exceeded, a line will be divided into a head and tail with ellipses
    marking the ommitted text.
  height : None | int
    Maximum final number of lines.
    If exceeded, lines will be divided into a head and tail with ellipses
    marking the ommitted text.
  multiline : bool
    Formats sequences and mappings with each item on a separate line.
    Otherwise all items are formatted onto a single line.
  """

  obj_str = _fmt_obj(
    obj,
    width = width,
    height = height,
    multiline = multiline,
    method = method)

  if not ( width or height ):
    return obj_str

  lines = split_lines( obj_str )

  if height and len(lines) > height:
    if height > 2:
      j0 = (height - 1) // 2
      j1 = len(lines) - j0

      lines = lines[:j0] + ["~~~"] + lines[j1:]

    elif height == 2:
      lines = lines[:1] + lines[-1:]
    else:
      lines = lines[:1]

  if width and width > 4:
    for j, v in enumerate(lines):
      if len(v) > width:
        i0 = (width - 3) // 2
        i1 = len(v) - i0
        lines[j] = v[:i0] + "~~~" + v[i1:]

  return '\n'.join(lines)

#===============================================================================
Tree = namedtuple('Tree', ['depth', 'size', 'total', 'left', 'items', 'right'])

TRUNCATED = '…'
GROUP_ENDS = [
  ('[', ']'),
  ('(', ')'),
  ('{', '}'),
  ('"', '"'),
  ("'", "'"),
  ("`", "`")]

GROUP_CHARS = ''.join(set([c for ends in GROUP_ENDS for c in ends]))
TOKEN_PATTERN = re.compile(rf'([:,{TRUNCATED}{re.escape(GROUP_CHARS)}])', re.U)

GROUP_END_MAP = {k:v for k,v in GROUP_ENDS}
CLOSE_CHARS = ''.join(GROUP_END_MAP.values())
OPEN_CHARS = ''.join(GROUP_END_MAP.keys())

#===============================================================================
class Tree:
  __slots__ = ['depth', 'left', 'center', 'right', 'size', 'total']

  #-----------------------------------------------------------------------------
  def __init__(self, depth, left, center, right):
    self.depth = depth
    self.left = left
    self.center = tuple(center)
    self.right = right
    self.size = len(left) + len(right) + sum(len(v) for v in self.center if isinstance(v, str))
    self.total = self.size + sum(v.total for v in self.center if isinstance(v, Tree))

  #-----------------------------------------------------------------------------
  def fmt(self, join_lines = True, idx = ()):
    lines = deque()
    lines.append(f"{'  '*self.depth}* depth= {self.depth}, size= {self.size}, total= {self.total} ({self.total-self.size}), idx = {idx}")
    lines.append(f"{'  '*self.depth}{self.left}")

    for i, v in enumerate(self.center):
      if isinstance(v, Tree):
        lines.extend(v.fmt(join_lines = False, idx = idx + (i,)))
      else:
        lines.append(f"{'  '*self.depth}  |{v}")

    lines.append(f"{'  '*self.depth}{self.right}")

    if join_lines:
      return '\n'.join(lines)

    return lines

  #-----------------------------------------------------------------------------
  def limit(self, limit: int) -> Tree:
    """Collapse tree back to string while limiting total string length
    """

    if self.total <= limit:
      return self

    if limit <= 0:
      return Tree(
        depth = self.depth,
        left = self.left,
        center = [TRUNCATED],
        right = self.right)

    # attempt to split the difference in how much to truncate groups in the tree
    size = self.size
    group_size = self.total - size
    num_groups = sum([isinstance(v, Tree) for v in self.center])

    center = deque()

    for v in self.center:
      if limit <= 0:
        break

      balanced_limit = limit - min(limit, size, group_size)//2
      size_limit = min(size, balanced_limit)
      group_limit = limit - size_limit

      # print(f"limit= {limit}, size= {size}/{self.size}, group_size= {group_size}/{self.total-self.size}, num_groups= {num_groups}, balanced_limit= {balanced_limit}")

      if isinstance(v, Tree):
        weighted_limit = max(
          1 if group_limit > 0 else 0,
          group_limit//min(num_groups, 2))

        # weighted_limit = group_limit
        # print(f"  weighted_limit= {weighted_limit}")
        _v = v.limit(weighted_limit)
        num_groups -= 1
        group_size -= v.total
        limit -= limited_append(group_limit, center, _v)

      elif v in ':,':
        limit -= limited_append(size_limit, center, v)
        size -= len(v)
      else:
        size -= len(v)

        if size_limit <= 0:
          # out of space for current level
          limit -= limited_append(size_limit, center, TRUNCATED)

        else:
          text = trim_text(size_limit, v)
          # print(f"{'  '*self.depth} << {text} << {v}")
          limit -= limited_append(size_limit, center, text)

    # if self.depth > 0 and len(center) == 2 and center[-1] == TRUNCATED:
    #   return TRUNCATED

    return Tree(
      depth = self.depth,
      left = self.left,
      center = center,
      right = self.right)

  #-----------------------------------------------------------------------------
  def unparse(self,
      tokens: deque = None,
      join_tokens = True):

    if tokens is None:
      tokens = deque()

    tokens.append(self.left)

    for v in self.center:
      if isinstance(v, Tree):
        v.unparse(tokens, False)
      else:
        tokens.append(v)

    tokens.append(self.right)

    if join_tokens:
      return ''.join(tokens)

    return tokens

  #-----------------------------------------------------------------------------
  def __len__(self):
    return self.total

  #-----------------------------------------------------------------------------
  def __eq__(self, other):
    if other == TRUNCATED and len(self.center) == 1 and self.center[0] == TRUNCATED:
      return True

    return NotImplemented

#===============================================================================
def trim_multiline(text: str) -> str:
  """Trim multiline string to just first and last line
  """
  lines = text.splitlines()
  if len(lines) == 1:
    return text

  return f"{lines[0]}{TRUNCATED}{lines[-1]}"

#===============================================================================
def trim_text(limit: int, text: str) -> str:
  """Trim a string down to given length
  """
  if len(text) <= limit:
    return text

  if limit < 5:
    return TRUNCATED

  return text[:limit-1]+TRUNCATED

#===============================================================================
def group_descent(
    tokens: deque[str],
    left: str = '',
    right: str = '',
    depth: int = 0) -> Tree:
  """Use recursive descent to form a tree of group structures
  """

  items = deque()

  while tokens:
    token = tokens.popleft()

    if len(token) == 1:
      if right and token == right:
        break
      elif token in OPEN_CHARS:
        items.append(group_descent(tokens, token, GROUP_END_MAP[token], depth+1))
      else:
        items.append(trim_multiline(token))
    else:
      items.append(trim_multiline(token))
  else:
    # did not find the closing token, avoid inserting one that didn't exist
    right = ''

  return Tree(
    depth = depth,
    left = left,
    center = items,
    right = right)

#===============================================================================
def limited_append(limit: int, tokens: deque[str], token: str|Tree) -> int:
  if not token:
    return 0

  if limit <= 0:
    # out of space for current level
    token = TRUNCATED

  truncated = token == TRUNCATED

  prev_truncated = len(tokens) > 0 and (
    (isinstance(tokens[-1], str) and tokens[-1].endswith(TRUNCATED))
    or tokens[-1] == TRUNCATED)

  if truncated and prev_truncated:
    # combine repeated truncations
    if isinstance(tokens[-1], Tree):
      # replace with plain truncation
      tokens.pop()
      tokens.append(TRUNCATED)

    return 0

  if len(tokens) > 1:
    prev_2, prev_1 = tokens[-2], tokens[-1]

    if prev_2 == TRUNCATED and prev_1 == ':':
      # If the key was truncated, don't bother adding the value, just truncate the
      # full key-value pair
      tokens.pop()
      tokens.pop()
      tokens.append(TRUNCATED)
      return -1

    if prev_2 == ',' and prev_1 == TRUNCATED and token == ',':
      # collapse successive truncated separators: , TRUNCATED ,
      tokens.pop()
      return -1

    if prev_2 == TRUNCATED and prev_1 == ',' and token == TRUNCATED:
      # collapse successive truncated separators: TRUNCATED , TRUNCATED
      tokens.pop()
      tokens.pop()
      tokens.append(TRUNCATED)
      return -1

  tokens.append(token)
  return len(token)

#===============================================================================
def collapse_text(limit: int, text: str) -> str:
  """Limit string to a given total length by collapsing nested groupings
  """
  limit = max(0, limit)

  if len(text) <= limit:
    return text

  # NOTE: removes all pure-whitespace tokens
  tokens = deque([v for v in TOKEN_PATTERN.split(text) if v.strip()])

  tree = group_descent(tokens)
  return tree.limit(limit).unparse()
