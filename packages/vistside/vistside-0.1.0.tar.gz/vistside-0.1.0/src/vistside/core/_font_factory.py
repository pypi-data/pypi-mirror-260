"""The fontFactory function creates instances of QFont."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QFont
from PySide6.QtGui import QFontDatabase
from vistutils.text import stringList
from vistutils.parse import maybe


def _getFontFamilies() -> list[str]:
  """Getter-function for font families."""
  return [f.lower() for f in QFontDatabase().families()]


def resolveFontFamily(family: str, **kwargs) -> str:
  """Resolves a font family."""
  families = _getFontFamilies()
  if family.lower() in families:
    return family
  if kwargs.get('strict', True):
    e = """The name '%s' was not recognized as a font family."""
    raise NameError(e)
  return ''


def _createFont(*args, **kwargs) -> QFont:
  """Creates a QFont instance."""
  familyDefault = "Courier"
  sizeDefault = 16
  weightDefault = QFont.Weight.Normal
  familyArg, sizeArg, weightArg = None, None, None
  familyKeys = stringList("""family, fontFamily""")
  sizeKeys = stringList("""size, fontSize""")
  weightKeys = stringList("""weight, fontWeight""")
  for arg in args:
    if isinstance(arg, str):
      family = resolveFontFamily(arg, strict=False)
      if family and familyArg is None:
        familyArg = family
    elif isinstance(arg, int) and sizeArg is None:
      sizeArg = arg
  familyKwarg, sizeKwarg, weightKwarg = None, None, None
  for key in familyKeys:
    if key in kwargs and familyKwarg is None:
      familyKwarg = kwargs[key]
  for key in sizeKeys:
    if key in kwargs and sizeKwarg is None:
      sizeKwarg = kwargs[key]
  for key in weightKeys:
    if key in kwargs and weightKwarg is None:
      weightKwarg = kwargs[key]
  family = maybe(familyKwarg, familyArg, familyDefault)
  size = maybe(sizeKwarg, sizeArg, sizeDefault)
  weight = maybe(weightKwarg, weightArg, weightDefault)
  font = QFont()
  font.setFamily(family)
  font.setPointSize(size)
  font.setWeight(weight)
  return font


def parseFont(*args, **kwargs) -> QFont:
  """Parses a QFont instance."""
  return _createFont(*args, **kwargs)
