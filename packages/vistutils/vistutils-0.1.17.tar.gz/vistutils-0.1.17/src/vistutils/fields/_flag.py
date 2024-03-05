"""Flag provides a boolean descriptor implementation."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistutils.fields import TypedField


class Flag(TypedField):
  """The Flag class provides a strongly typed descriptor containing
  booleans."""

  __default_value__ = None
  __fallback_value__ = False

  def getFieldType(self, ) -> type:
    """Returns the field type."""
    return bool

  def getDefaultValue(self) -> bool:
    """Returns the default value."""
    if self.__default_value__ is None:
      return self.__fallback_value__
    return self.__default_value__
