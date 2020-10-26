from .cacheL1 import CacheL1



class SnooperL1:
  def __init__(self, owner):
    self.cache = CacheL1()

    self._chipOwner = owner


  def writeCache(self, direction, value):
    self.cache.setLineByIndex(direction % 4, "S", direction, value)

  def moesiMachineBus(self, signal, direction, owner):
    line = self.cache.getLine(direction)

    if line is None:
      return

    if line.getState() == 'M':
      if signal == 'RM':
        #Pasando de M a O
        self._m_to_o(line, owner)


      elif signal == 'WM':
        #Pasando de M a I
        self._m_to_i(line, owner)


    elif line.getState() == 'S':
      if signal == 'WM':
        #Pasando de S a I
        self._s_to_i(line, owner)



    elif line.getState() == 'E':
      if signal == 'WM':
        #Pasando de E a I
        self._e_to_i(line, owner)



      if signal == 'RM':
        #Pasando de E a S
        self._e_to_s(line, owner)

    elif line.getState() == 'O':
      if signal == 'WM' or signal == "RM":
        b=2+4
      else:
        #Pasando de O a I
        self._o_to_i(line,owner)

  def moesiMachineProcessor(self, signal, direction, cpu_data, owner):
    line = self.cache.getLineByIndex(direction)
    response = "NOP"

    if line.getState() == 'M':
      if signal == 'WRITE':
        #Mantiene M
        line.setData(cpu_data)
        line.setTag(direction)
        response = "WM"



    elif line.getState() == 'S':
      if signal == 'WRITE':
        #Pasando de S a M
        self._s_to_m(line, owner)
        line.setData(cpu_data)
        line.setTag(direction)
        response = "WM"


      

      elif signal == 'READ':
        #Mantiene S
        response = "RM"


    elif line.getState() == 'E':
      if signal == 'WRITE':
        #Pasando de I a E
        self._e_to_m(line,owner)
        line.setData(cpu_data)
        line.setTag(direction)
        response = "WM"
      
      elif signal == 'READ':
        #Mantiene E
        response = "RM"

      print("Exclusivo")

    elif line.getState() == 'O':
      if signal == 'WRITE':
        #Pasando de O a M
        self._o_to_m(line,owner)
        line.setData(cpu_data)
        line.setTag(direction)
        response = "WM"


      elif signal == 'READ':
        #Mantiene O
        response = "RM"

      print("Dueño")

      

    elif line.getState() == 'I':
      if signal == 'WRITE':
        #Pasando de I a M
        self._i_to_m(line, owner)
        line.setData(cpu_data)
        line.setTag(direction)
        response = "WM"

   

      elif signal == 'READ':
        #Pasando de I a E
        self._i_to_e(line, owner)
        response = "RM"


    else:
      print("Cache state error")

    return response

  def _m_to_s(self, line, owner):
    line.setState('S')
    line.setVBit(1)
    line.setDBit(0)

  def _m_to_i(self, line, owner):
    line.setState('I')
    line.setVBit(0)
    line.setDBit(0)
  
  def _m_to_o(self, line, owner):
    line.setState('O')
    line.setVBit(0)
    line.setDBit(0)
    #line.setOData(1)

  def _s_to_i(self, line, owner):
    line.setState('I')
    line.setVBit(0)
    line.setDBit(0)
  
  def _s_to_e(self, line, owner):
    line.setState('I')
    line.setVBit(1)
    line.setDBit(0)

  def _s_to_m(self, line, owner):
    line.setState('M')
    line.setVBit(1)
    line.setDBit(1)

  def _i_to_s(self, line, owner):
    line.setState('S')
    line.setVBit(1)
    line.setDBit(0)

  def _i_to_m(self, line, owner):
    line.setState('M')
    line.setVBit(1)
    line.setDBit(1)
  
  def _i_to_e(self, line, owner):
    line.setState('E')
    line.setVBit(1)
    line.setDBit(1)

  def _e_to_m(self, line, owner):
    line.setState('M')
    line.setVBit(1)
    line.setDBit(1)
  
  def _e_to_s(self, line, owner):
    line.setState('S')
    line.setVBit(1)
    line.setDBit(0)
  
  def _e_to_i(self, line, owner):
    line.setState('I')
    line.setVBit(0)
    line.setDBit(0)
  
  def _o_to_m(self, line, owner):
    line.setState('M')
    line.setVBit(1)
    line.setDBit(1)
    #line.setOData(0)
  
  def _o_to_i(self, line, owner):
    line.setState('I')
    line.setVBit(0)
    line.setDBit(0)
    #line.setOData(0)

  def getCache(self):
    return self.cache