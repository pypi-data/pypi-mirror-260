"""IntField provides a strongly typed descriptor field for integers"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from vistutils.fields import ImmutableDescriptor


class IntField(ImmutableDescriptor):
  """The IntField class provides a strongly typed descriptor containing
  integers."""

  __default_value__ = None
  __fallback_value__ = 0

  def __init__(self, *args, **kwargs) -> None:
    ImmutableDescriptor.__init__(self, int, *args, **kwargs)
    for arg in args:
      if isinstance(arg, int) and self.__default_value__ is None:
        self.__default_value__ = arg
        break

  def getDefaultValue(self) -> Any:
    """Returns the default value."""
    if self.__default_value__ is None:
      return self.__fallback_value__
    return self.__default_value__
