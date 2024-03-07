"""The ComplexField class provides a strongly typed descriptor containing
  complex numbers."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations
from typing import Any
from vistutils.fields import ImmutableDescriptor


class ComplexField(ImmutableDescriptor):
  """The ComplexField class provides a strongly typed descriptor containing
  complex numbers."""

  __default_value__ = None
  __fallback_value__ = 0j

  def __init__(self, *args, **kwargs) -> None:
    ImmutableDescriptor.__init__(self, complex, *args, **kwargs)
    for arg in args:
      if isinstance(arg, complex) and self.__default_value__ is None:
        self.__default_value__ = arg
        break

  def getDefaultValue(self) -> Any:
    """Returns the default value."""
    if self.__default_value__ is None:
      return self.__fallback_value__
    return self.__default_value__

  def __get__(self, instance: object, owner: type, **kwargs) -> complex:
    """Returns the value of the descriptor."""
    return ImmutableDescriptor.__get__(self, instance, owner, **kwargs)
