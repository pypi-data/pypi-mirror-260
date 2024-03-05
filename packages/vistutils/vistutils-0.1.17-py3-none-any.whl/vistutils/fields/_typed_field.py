"""TypedField provides a strongly typed descriptor class"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from logging import warning
from typing import Any

from vistutils.fields import CoreDescriptor
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg


class TypedField(CoreDescriptor):
  """TypedField provides a strongly typed descriptor class"""

  @classmethod
  def _parseArgs(cls, *args, **kwargs) -> dict:
    """Parses the positional arguments"""
    defVal = kwargs.get('defVal', None)
    valType = kwargs.get('valType', None)
    if defVal is not None and valType is not None:
      if args:
        w = """The TypedField constructor received keyword arguments 
        defining both the default value and the value type. The additional 
        positional arguments are ignored."""
        warning(w)
      return {'defVal': defVal, 'valType': valType}
    if defVal is not None and valType is None:
      return {'defVal': defVal, 'valType': type(defVal)}
    if valType is not None and defVal is None:
      if isinstance(valType, type):
        for arg in args:
          if isinstance(arg, type):
            w = """The TypedField constructor received both a positional 
            argument and a keyword argument defining the value type. The 
            positional argument is ignored."""
            warning(w)
          if isinstance(arg, valType):
            return {'defVal': arg, 'valType': valType}
        else:
          return {'valType': valType, 'defVal': None}
      else:
        e = typeMsg('valType', valType, type)
        raise TypeError(e)
    #  defVal is None and valType is None
    if len(args) == 1:
      if isinstance(args[0], type):
        return {'valType': args[0], 'defVal': None}
      return {'defVal': args[0], 'valType': type(args[0])}
    if len(args) == 2:
      typeArg, defValArg = None, None
      for arg in args:
        if isinstance(arg, type):
          if typeArg is not None:
            e = """The TypedField constructor received two positional 
            arguments, but both are types. This ambiguity is prohibited."""
            raise TypeError(e)
          typeArg = arg
        else:
          if defValArg is not None:
            e = """The TypedField constructor received two positional 
            arguments, neither of which are types. This ambiguity is 
            prohibited."""
            raise TypeError(e)
          defValArg = arg
      if isinstance(defValArg, typeArg):
        return {'defVal': defValArg, 'valType': typeArg}
      e = typeMsg('defVal', defValArg, typeArg)
      raise TypeError(e)
    if len(args) > 2:
      e = """The TypedField constructor received more than two positional 
      arguments. This is prohibited."""
      raise TypeError(e)

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the TypedField"""
    CoreDescriptor.__init__(self, *args, **kwargs)
    parsed = self._parseArgs(*args, **kwargs)
    self.__default_value__ = parsed['defVal']
    self.__field_type__ = parsed['valType']

  def _getDefaultValue(self) -> Any:
    """Returns the default value."""
    if self.__default_value__ is not None:
      if isinstance(self.__default_value__, self._getFieldType()):
        return self.__default_value__
      e = typeMsg('defaultValue',
                  self.__default_value__,
                  self._getFieldType())
      raise TypeError(e)
    e = """This instance of TypedField provides no default value!"""
    raise ValueError(e)

  def _getFieldType(self) -> type:
    """Returns the field type."""
    if self.__field_type__ is not None:
      return self.__field_type__
    e = """This instance of TypedField provides no field type!"""
    raise ValueError(e)

  def _instantiate(self, instance: object, owner: type = None) -> None:
    """Instantiates the field"""
    setattr(instance, self._getPrivateName(), self._getDefaultValue())

  def __get__(self, instance: object, owner: type, **kwargs) -> Any:
    """Returns the value of the field"""
    if instance is None:
      return self
    pvtName = self._getPrivateName()
    if getattr(instance, pvtName, None) is not None:
      value = getattr(instance, pvtName)
      if isinstance(value, self._getFieldType()):
        return value
      e = typeMsg('value', value, self._getFieldType())
      raise TypeError(e)
    if kwargs.get('_recursion', False):
      raise RecursionError
    self._instantiate(instance, owner)
    return self.__get__(instance, owner, _recursion=True)

  def __set__(self, instance: object, value: object) -> None:
    """Sets the value of the field"""
    if isinstance(value, self._getFieldType()):
      return setattr(instance, self._getPrivateName(), value)
    e = typeMsg('value', value, self._getFieldType())
    raise TypeError(e)

  def __delete__(self, instance: object) -> None:
    """Deletes the value of the field"""
    pvtName = self._getPrivateName()
    if hasattr(instance, pvtName):
      return delattr(instance, pvtName)
    e = """The instance: '%s' has no attribute at given name: '%s'!"""
    raise AttributeError(monoSpace(e % (instance, pvtName)))
