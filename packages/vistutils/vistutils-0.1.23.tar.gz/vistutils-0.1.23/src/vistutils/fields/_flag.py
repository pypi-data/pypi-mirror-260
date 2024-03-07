"""Flag provides a boolean descriptor implementation."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistutils.fields import ImmutableDescriptor


class Flag(ImmutableDescriptor):
  """The Flag class provides a strongly typed descriptor containing
  booleans."""

  __default_value__ = None
  __fallback_value__ = False

  def __init__(self, *args) -> None:
    ImmutableDescriptor.__init__(self, bool, *args)
    for arg in args:
      if isinstance(arg, bool) and self.__default_value__ is None:
        self.__default_value__ = arg
        break

  def getDefaultValue(self) -> bool:
    """Returns the default value."""
    if self.__default_value__ is None:
      return self.__fallback_value__
    return self.__default_value__
