"""Wait provides a deferred value through a descriptor allowing for it to
be defined at the time of creating the owning flass, without requiring
immediate instantiation. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from warnings import warn

from vistutils.fields import CoreDescriptor


class Wait(CoreDescriptor):
  """Wait provides a deferred value through a descriptor allowing for it to
  be defined at the time of creating the owning flass, without requiring
  immediate instantiation. """

  def __init__(self, *args, **kwargs):
    """Initializes the descriptor"""

  def __get__(self, instance: object, owner: type, **kwargs) -> Any:
    """Returns the value of the descriptor"""
    return self._defVal

  def __set__(self, instance: object, value: Any) -> None:
    """Sets the value of the descriptor"""
    e = """The Wait descriptor does not support setting the value of the 
    descriptor. The value is defined at the time of creating the owning 
    class, and cannot be changed."""
    raise AttributeError(e)

  def __delete__(self, instance) -> None:
    """Deletes the value of the descriptor"""
    e = """The Wait descriptor does not support deleting the value of the 
    descriptor. The value is defined at the time of creating the owning 
    class, and cannot be changed."""
    raise AttributeError(e)