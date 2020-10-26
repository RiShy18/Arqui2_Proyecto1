from .cacheAux import CacheAux


class ControllerAux:
  def __init__(self, chipOwner):
    self.cache = CacheAux()

    self._chipOwner = chipOwner



  def writeCache(self, direction, value, owner):
    self.cache.setLineByIndex(direction % 4, "SS", owner, direction, value)

  def moesiMachineExtF(self, signal, direction, extOwner):
    line = self.cache.getLine(direction)

    if signal == "" or line is None:
      return

    if line.getState() == 'SM':
      if signal == 'WMF':
        self._sm_to_si(line)


        return True

      elif signal == "RMF":
        self._sm_to_ss(line, 'E')



    elif line.getState() == 'SS':
      if signal == 'WMF':
        self._ss_to_si(line)

        return True

      elif signal == "RMF":
        line.appendOwner('E')


    elif line.getState() == 'SI':
      if signal == "RMF":
        self._si_to_ss(line, extOwner)

 

  def moesiMachineL1(self, signal, direction, cpu_data, owner):

    if signal == "NOP":
      return ("", "")

    line = self.cache.getLineByIndex(direction)
    response = ()

    if line.getState() == 'SM':
      if signal == 'RM':
        self._sm_to_ss(line, owner)
        response = (line.getData(), "")


      elif signal == 'WM':
        line.setData(cpu_data)
        line.setTag(direction)
        response = ("WRITE", "WMF")



    elif line.getState() == 'SS':
      if signal == 'WM':
        self._ss_to_sm(line, owner)
        line.setData(cpu_data)
        line.setTag(direction)
        response = ("WRITE", "WMF")


      elif signal == "RM":
        line.appendOwner(owner)
        response = (line.getData(), "RMF")



    elif line.getState() == 'SI':
      if signal == 'WM':
        self._si_to_sm(line, owner)
        line.setData(cpu_data)
        line.setTag(direction)
        response = ("WRITE", "WMF")



      elif signal == 'RM':
        self._si_to_ss(line, owner)
        response = ("READ", "RMF")


    else:
      print("Cache state error")

    return response

  def _sm_to_ss(self, line, owner):
    line.setState('SS')
    line.appendOwner(owner)

  def _sm_to_si(self, line):
    line.setState('SI')
    line.cleanOwners()

  def _ss_to_sm(self, line, owner):
    line.setState('SM')
    line.cleanOwners()
    line.appendOwner(owner)

  def _ss_to_si(self, line):
    line.setState('SI')
    line.cleanOwners()

  def _si_to_ss(self, line, owner):
    line.setState('SS')
    line.appendOwner(owner)

  def _si_to_sm(self, line, owner):
    line.setState('SM')
    line.appendOwner(owner)

  def getCache(self):
    return self.cache
