"""The ImmutableDescriptor provides a descriptor supporting immutable
values. This means that the setter will always discard the existing value
on the given instance, before replacing it with the new value. Although
subclasses can reimplement the setter function, the default implementation
provides type checking making this descriptor strongly typed. To make use
of this feature, the instance must be initialized with a type and
optionally a default value.

Acceptable signatures:
import ImmutableDescriptor as Immut
class Owner:
  #  Example

  field = Immut(fieldType: type)  # type, no default value
  field2 = Immut(fieldType: type, defVal: object)  # type, default value
  field3 = Immut(defVal: object, )  # default value, inferred type

For each of the above a keyword argument provided takes precedence.
Multiple types given will cause an error. Multiple non-types are likewise
prohibited. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistutils.fields import CoreDescriptor
from vistutils.waitaminute import typeMsg


class ImmutableDescriptor(CoreDescriptor):
  """The ImmutableDescriptor provides a descriptor supporting immutable
  values. This means that the setter will always discard the existing value
  on the given instance, before replacing it with the new value. Although
  subclasses can reimplement the setter function, the default implementation
  provides type checking making this descriptor strongly typed."""

  __field_type__ = None

  def __init__(self, *args) -> None:
    """Initializes the descriptor"""
    CoreDescriptor.__init__(self, *args)
    if not args:
      raise ValueError('Received no arguments!')
    if len(args) == 1:
      if isinstance(args[0], type):
        self.__defVal = None
        self.__valType = args[0]
      else:
        self.__defVal = args[0]
        self.__valType = type(args[0])
    elif len(args) == 2:
      if isinstance(args[0], type):
        if isinstance(args[1], args[0]):
          self.__valType = args[0]
          self.__defVal = args[1]
        else:
          e = typeMsg(args[0], args[1], args[0])
          raise TypeError(e)
      elif isinstance(args[1], type):
        if isinstance(args[0], args[1]):
          self.__valType = args[1]
          self.__defVal = args[0]
        else:
          e = typeMsg(args[1], args[0], args[1])
          raise TypeError(e)
      else:
        e = """Received no types and multiple arguments!"""
        raise ValueError(e)
    else:
      e = """Received too many arguments!"""
      raise ValueError(e)

  def _getFieldType(self, ) -> type:
    """Getter-function for getting the field type"""
    return self.__valType

  def __get__(self, instance: object, owner: type, **kwargs) -> object:
    """Returns the value of the descriptor"""
    if instance is None:
      return self
    pvtName = self._getPrivateName()
    if getattr(instance, pvtName, None) is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      setattr(instance, pvtName, self._getDefaultValue())
      return self.__get__(instance, owner, _recursion=True, **kwargs)
    value = getattr(instance, pvtName)
    fieldType = self._getFieldType()
    if isinstance(value, fieldType):
      return value
    e = typeMsg('value', value, fieldType)
    raise TypeError(e)

  def __set__(self, instance: object, value: object) -> None:
    """Sets the value of the descriptor"""
    if isinstance(value, self._getFieldType()):
      return setattr(instance, self._getPrivateName(), value)
    e = typeMsg('value', value, self._getFieldType())
    raise TypeError(e)

  def __delete__(self, instance: object) -> None:
    """Deletes the value of the descriptor"""
    if hasattr(instance, self._getPrivateName()):
      return delattr(instance, self._getPrivateName())
    e = """Tried to delete field named: '%s', but the instance given: '%s' 
    has no such attribute!"""
    raise AttributeError(e % (self._getFieldName(), instance))

  def _getDefaultValue(self) -> object:
    """Returns the default value"""
    if self.__defVal is not None:
      if isinstance(self.__defVal, self._getFieldType()):
        return self.__defVal
      e = typeMsg('defaultValue', self.__defVal, self._getFieldType())
      raise TypeError(e)
    e = """This instance of ImmutableDescriptor provides no default value!"""
    raise ValueError(e)
