"""The timerFactory creates the QTimer instances used in the application. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QTimer, Qt
from vistutils.parse import maybe
from vistutils.text import stringList

from morevistside.core import Precise


def _parseArgs(*args, **kwargs) -> dict:
  """timerFactory creates a QTimer instance. """
  epochKwarg, shotKwarg, timerTypeKwarg = None, None, None
  epochArg, shotArg, timerTypeArg = None, None, None
  epochDefault, shotDefault, timerTypeDefault = 100, False, Precise
  epochKeys = stringList("""epoch, length, interval, time""")
  shotKeys = stringList("""shot, singleShot""")
  notShotKeys = stringList("""repeat, again""")
  timerTypeKeys = stringList("""timerType, precision, accuracy""")
  names = stringList("""epoch, shot, notShot, timerType""")
  keyArgs = dict(epoch=None, timerType=None)
  Keys = [epochKeys, shotKeys, notShotKeys, timerTypeKeys]
  types = [int, bool, bool, Qt.TimerType]
  for (keys, name, type_,) in zip(Keys, names, types):
    for key in keys:
      if key in kwargs:
        if isinstance(kwargs[key], type_):
          keyArgs[name] = kwargs[key]
  if 'shot' in keyArgs and 'notShot' in keyArgs:
    e = 'Both shot and notShot are present in the arguments.'
    raise ValueError(e)
  if 'shot' in keyArgs:
    shotKwarg = keyArgs['shot']
  elif 'notShot' in keyArgs:
    shotKwarg = not keyArgs['notShot']
  epochKwarg = keyArgs['epoch']
  timerTypeKwarg = keyArgs['timerType']
  for arg in args:
    if isinstance(arg, int) and epochArg is None:
      epochArg = arg
    if isinstance(arg, bool) and shotArg is None:
      shotArg = arg
    if isinstance(arg, Qt.TimerType) and timerTypeArg is None:
      timerTypeArg = arg
  epoch = maybe(epochKwarg, epochArg, epochDefault)
  shot = maybe(shotKwarg, shotArg, shotDefault)
  timerType = maybe(timerTypeKwarg, timerTypeArg, timerTypeDefault)
  return dict(epoch=epoch, shot=shot, timerType=timerType)


def parseTimer(*args, **kwargs) -> dict:
  """The timerFactory creates a QTimer instance. """
  parsed = _parseArgs(*args, **kwargs)
  timer = QTimer()
  timer.setInterval(parsed['epoch'])
  timer.setTimerType(parsed['timerType'])
  timer.setSingleShot(parsed['shot'])
  return timer
