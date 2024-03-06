"""TextField provides a strongly typed descriptor containing text."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from vistutils.fields import TypedField


class TextField(TypedField):
  """The TextField class provides a strongly typed descriptor containing
  text."""

  __default_value__ = None
  __fallback_value__ = ''

  def __init__(self, *args, **kwargs) -> None:
    for arg in args:
      if isinstance(arg, str):
        TypedField.__init__(self, str, arg)
        break
    else:
      TypedField.__init__(self, str, )

  def getDefaultValue(self) -> Any:
    """Returns the default value."""
    if self.__default_value__ is None:
      return self.__fallback_value__
    return self.__default_value__
