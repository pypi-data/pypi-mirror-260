"""FontField provides a field for selecting a font."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from vistutils.fields import unParseArgs
from vistutils.parse import maybe
from vistutils.waitaminute import typeMsg


class CoreDescriptor:
  """CoreDescriptor provides a singleton descriptor on the descriptor
  types."""

  __field_name__ = None
  __field_owner__ = None
  __positional_args__ = None
  __keyword_args__ = None

  def __set_name__(self, owner: type, name: str) -> None:
    """Sets the field name and owner."""
    self.__field_name__ = name
    self.__field_owner__ = owner

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the descriptor."""
    self.__positional_args__ = args
    self.__keyword_args__ = kwargs

  def _getFieldName(self) -> str:
    """Getter-function for getting the field name."""
    if self.__field_name__ is None:
      e = """Field name not defined!"""
      raise AttributeError(e)
    if isinstance(self.__field_name__, str):
      return self.__field_name__
    e = typeMsg('__field_name__', self.__field_name__, str)
    raise TypeError(e)

  def _getPrivateName(self) -> str:
    """Getter-function for getting the private name."""
    return '_%s' % self._getFieldName()

  def _getFieldOwner(self) -> type:
    """Getter-function for getting the field owner."""
    if self.__field_owner__ is None:
      e = """Field owner not defined!"""
      raise AttributeError(e)
    if isinstance(self.__field_owner__, type):
      return self.__field_owner__
    e = typeMsg('__field_owner__', self.__field_owner__, type)
    raise TypeError(e)

  def _instantiate(self, instance: object, ) -> None:
    """Please note that the core descriptor provides no implementation of
    this method. """
    raise AttributeError(self._getFieldName())

  def __get__(self, instance: object, owner: type, **kwargs) -> Any:
    """Returns the font or the descriptor."""
    if instance is None:
      return self
    pvtName = self._getPrivateName()
    if getattr(instance, pvtName, None) is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._instantiate(instance)
      return self.__get__(instance, owner, _recursion=True)
    if hasattr(instance, pvtName):
      return getattr(instance, pvtName)
    return self

  def __set__(self, instance: object, value: Any) -> None:
    """Sets the field."""
    args, kwargs = unParseArgs(value)
    self.__positional_args__ = args
    self.__keyword_args__ = kwargs

  def _getPrivateArgsName(self) -> str:
    """Getter-function for getting the private args name."""
    return '__%s_args__' % self._getFieldName()

  def _getPrivateArgs(self) -> tuple:
    """Getter-function for getting the private args."""
    return maybe(self.__positional_args__, [])

  def _getPrivateKwargsName(self) -> str:
    """Getter-function for getting the private kwargs name."""
    return '__%s_kwargs__' % self._getFieldName()

  def _getPrivateKwargs(self) -> tuple:
    """Getter-function for getting the private args."""
    return maybe(self.__keyword_args__, {})

  def _getFieldArgs(self) -> tuple:
    """Getter-function for getting the positional arguments."""
    return self.__positional_args__

  def _getFieldKwargs(self) -> dict:
    """Getter-function for getting the keyword arguments."""
    return self.__keyword_args__

  def _getArgs(self, instance: object) -> list:
    """Getter-function for getting the positional arguments."""
    return [*self._getPrivateArgs(), *self._getFieldArgs()]

  def _getKwargs(self, instance: object) -> dict:
    """Getter-function for getting the keyword arguments."""
    return {**self._getPrivateKwargs(), **self._getFieldKwargs()}
