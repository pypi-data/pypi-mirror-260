"""TextField provides a strongly typed descriptor containing text."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from vistutils.fields import MutableDescriptor


class TextField(MutableDescriptor):
  """The TextField class provides a strongly typed descriptor containing
  text."""

  __default_value__ = None
  __fallback_value__ = ''

  def __init__(self, *args, **kwargs) -> None:
    MutableDescriptor.__init__(self, str, *args, **kwargs)
    for arg in args:
      if isinstance(arg, str) and self.__default_value__ is None:
        self.__default_value__ = arg
        break

  def __get__(self, instance: object, owner: type, **kwargs) -> str:
    """Returns the value of the descriptor."""
    return MutableDescriptor.__get__(self, instance, owner, **kwargs)
