class CacheLineAux:
  def __init__(self):
    self._tag = 0
    self._data = 0
    self._state = "SI"
    self._owners = []

  def getTag(self):
    return self._tag

  def setTag(self, tag):
    self._tag = tag

  def getData(self):
    return self._data

  def setData(self, data):
    self._data = data

  def getState(self):
    return self._state

  def setState(self, state):
    self._state = state

  def getOwners(self):
    return self._owners

  def setOwners(self, owners):
    self._owners = owners

  def appendOwner(self, owner):
    if owner not in self._owners:
      self._owners.append(owner)

  def cleanOwners(self):
    self._owners.clear()


class CacheAux:
  def __init__(self):
    self._lines = []

    for _ in range(8):
      self._lines.append(CacheLineAux())

  def getLine(self, direction):
    for line in self._lines:
      if line.getTag() == direction:
        return line

  def getLineByIndex(self, direction):
    return self._lines[direction % 8]

  def setLineByIndex(self, index, state, owners, tag, data):
    self._lines[index].setTag(tag)
    self._lines[index].setData(data)
    self._lines[index].setState(state)
    self._lines[index].setOwners(owners)

  def getLines(self):
    return self._lines

  def printCache(self):
    for i in range(8):
      print("{}, {}, {}, {}".format(
          self._lines[i].getState(),
          self._lines[i].getOwners(),
          self._lines[i].getData(),
          self._lines[i].getTag()
      ))
