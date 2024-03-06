"""MutableDescriptor provides a descriptor implementation supporting
values of mutable types. This means that the setter does not replace the
value of the descriptor on some instance, but instead applies an update to
the value. Subclasses must implement this update method for it to be
available. For example by implementing overloading the __set__ method. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistutils.fields import CoreDescriptor


class MutableDescriptor(CoreDescriptor):
  """MutableDescriptor provides a descriptor implementation supporting
  values of mutable types. This means that the setter does not replace the
  value of the descriptor on some instance, but instead applies an update to
  the value. Subclasses must implement this update method for it to be
  available. For example by implementing overloading the __set__ method. """

  def __set__(self, instance: object, value: object) -> None:
    """Sets the value of the descriptor"""
    raise NotImplementedError(self._getFieldName())
