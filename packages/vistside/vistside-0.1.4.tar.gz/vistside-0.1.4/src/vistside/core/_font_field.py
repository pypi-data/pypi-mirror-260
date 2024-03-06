"""FontField provides a field for selecting a font."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistutils.fields import CoreDescriptor

from vistside.core import parseFont


class FontField(CoreDescriptor):
  """The FontField class provides a field for selecting a font."""

  def _instantiate(self, instance: object) -> None:
    """Instantiates the field."""
    font = parseFont(*self._getArgs(), **self._getKwargs())
    setattr(instance, self._getPrivateName(), font)
