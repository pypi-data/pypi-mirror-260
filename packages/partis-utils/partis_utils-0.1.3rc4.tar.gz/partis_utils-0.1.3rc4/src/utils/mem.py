# -*- coding: UTF-8 -*-

import sys
import gc
import inspect
import logging


from collections import OrderedDict as odict
from .fmt import collapse_text
from .hint import ModelHint, Loc

log = logging.getLogger(__name__)



#===============================================================================
def obj_referrer_chains(
    obj,
    max_depth = 20,
    _depth = 0,
    _visited = None,
    _ignored = None,
    _children = None):

  if _depth == 0:
    _visited = set()
    _ignored = set()
    _children = set()

  frame_id = id(sys._getframe())
  _ignored = _ignored|{frame_id}

  _visited.add(id(obj))

  _children = _children|{id(obj)}

  hints = list()

  if _depth >= max_depth:
    hints.append(ModelHint("[MAX_DEPTH]"))

  elif inspect.ismodule(obj):
    hints.append(ModelHint("[MODULE]", data = obj.__name__))

  else:
    refs = gc.get_referrers(obj)
    refs_id = id(refs)
    _ignored.add(refs_id)

    for ref in refs:
      _id = id(ref)

      if _id in _ignored or ref is obj:
        pass

      elif inspect.isroutine(ref) or inspect.ismethod(ref) or inspect.isfunction(ref):
        # pass
        code = getattr(ref, '__code__', None)
        if code is not None:
          name = code.co_name
          loc = Loc(filename = code.co_filename, line = code.co_firstlineno)
        else:
          name = getattr(ref, '__name__', '<unknown>')
          loc = None

        hints.append(ModelHint(
          f"[FUNCTION] {name}()",
          loc = loc))

      elif inspect.isframe(ref):
        code = ref.f_code
        hints.append(ModelHint(
          f"[FRAME] {code.co_name}()",
          loc = Loc(filename = code.co_filename, line = code.co_firstlineno)))

      elif _id in _visited:
        hints.append(ModelHint(
          f"[REPEATED] {type(ref).__name__} @ {id(ref)}",
          data = collapse_text(500, repr(ref))))

      elif _id in _children:
        hints.append(ModelHint(
          f"[CIRCULAR] {type(ref).__name__} @ {id(ref)}",
          data = collapse_text(500, repr(ref))))

      else:
        hints.append(obj_referrer_chains(ref, max_depth, _depth+1, _visited, _ignored, _children))

  return ModelHint(
    f"{type(obj).__name__} @ {id(obj)}",
    data = collapse_text(500, repr(obj)),
    hints = hints)
