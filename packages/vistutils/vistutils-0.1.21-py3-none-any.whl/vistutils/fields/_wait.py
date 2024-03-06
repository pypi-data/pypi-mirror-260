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

  __explicit_creator__ = None

  def __init__(self, base: Any, *args, **kwargs):
    """Initializes the descriptor"""
    if isinstance(base, type):
      self._setFieldType(base)
    elif callable(base):
      self._setCreator(base)
    CoreDescriptor.__init__(self, *args, **kwargs)

  def _setCreator(self, creator: Callable) -> Callable:
    """Sets the creator of the descriptor"""
    self.__explicit_creator__ = creator
    return creator

  def _getCreator(self, instance: object=None) -> Callable:
    """Returns the creator of the descriptor"""
    if self.__explicit_creator__ is not None:
      if callable(self.__explicit_creator__):
        return self.__explicit_creator__
      e = typeMsg('__explicit_creator__', self.__explicit_creator__,
                  'Callable')
      raise TypeError(e)
    fieldType = self._getFieldType()
    if getattr(fieldType, 'getDefault', None) is not None:
      creator = getattr(fieldType, 'getDefault')
      if callable(creator):
        return creator
      e = typeMsg('getDefault', creator, 'Callable')
      raise TypeError(e)
    return fieldType()

  def _instantiate(self, instance: object) -> None:
    """Instantiates the descriptor"""
    creator = self._getCreator(instance)
    value = creator()
    pvtName = self._getPrivateName()
    setattr(instance, pvtName, value)

  def __set__(self, instance: object, value: Any) -> None:
    """Sets the value of the descriptor"""
    fieldType = self._getFieldType()
    if getattr(fieldType, 'apply', None) is None:
      e = """The Wait descriptor requires a default value to be defined. 
      The default value is defined through the getDefault method of the 
      field type."""
      raise AttributeError(e)
    pvtName = self._getPrivateName()
    try:
      fieldType.apply(instance, value)
    except Exception as e:
      e = """Trying to apply '%s' to field '%s' of type '%s' encountered 
      the error.""" % (value, pvtName, fieldType)
      raise RuntimeError(e) from e

  def __delete__(self, instance) -> None:
    """Deletes the value of the descriptor"""
    e = """The Wait descriptor does not support deleting the value of the 
    descriptor. The value is defined at the time of creating the owning 
    class, and cannot be changed."""
    raise AttributeError(e)