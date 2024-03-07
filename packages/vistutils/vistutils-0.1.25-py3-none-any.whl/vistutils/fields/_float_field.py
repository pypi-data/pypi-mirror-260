"""FloatField provides a strongly typed descriptor containing floats."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistutils.fields import ImmutableDescriptor


class FloatField(ImmutableDescriptor):
  """The FloatField class provides a strongly typed descriptor containing
  floats."""

  __default_value__ = None
  __fallback_value__ = 0.0

  def __init__(self, *args) -> None:
    """Initializes the FloatField"""
    ImmutableDescriptor.__init__(self, float, *args)
    for arg in args:
      if isinstance(arg, float) and self.__default_value__ is None:
        self.__default_value__ = arg
        break

  def getDefaultValue(self) -> float:
    """Returns the default value."""
    if self.__default_value__ is None:
      return self.__fallback_value__
    return self.__default_value__

  def __get__(self, instance: object, owner: type, **kwargs) -> float:
    """Returns the value of the descriptor."""
    return ImmutableDescriptor.__get__(self, instance, owner, **kwargs)
