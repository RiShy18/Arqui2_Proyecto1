import numpy as np



class MemoryLine:
  def __init__(self):
    self._owner = 0
    self._data = 0

  def getOwner(self):
    return self._owner

  def setOwner(self, owner):
    self._owner = owner

  def getData(self):
    return self._data

  def setData(self, data):
    self._data = data


class MainMemory:
  def __init__(self):
    self._mem = []


    for _ in range(16):
      self._mem.append(MemoryLine())

  def controlMemory(self, signal, owner, direction, value, chip):
    if signal == "WRITE":
      self._mem[direction].setData(value)
      self._mem[direction].setOwner("{}".format(owner))


    elif signal == "READ":

      return self._mem[direction].getData()

  def getMem(self):
    return self._mem
