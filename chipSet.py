import threading
import queue
import time

from bus import Bus
from cache.controllerAux import ControllerAux


class ChipSet(threading.Thread):

  def __init__(self, chipNumber, extLock, queueMemIn, queueMemOut, Fqueue1, Fqueue2, guiQueues, mainwin, gameMode):
    threading.Thread.__init__(self)

    self._chipNumber = chipNumber
    self._chipName = "CH{}".format(chipNumber)
    self._lock = threading.Lock()

    self._buses = []
    self._threads = []

    self._queuesIn = queue.Queue()
    self._queuesOut = []

    self._queueMemIn = queueMemIn
    self._queueMemOut = queueMemOut
    self._extLock = extLock

    self._Fqueue1 = Fqueue1
    self._Fqueue2 = Fqueue2

    self._guiQueues = guiQueues
    self._mainwin = mainwin

    self._gameMode = int(gameMode)
    

    self._controller = ControllerAux(self._chipName)

  def _broadcast(self, data):
    for i in range(2):
      self._queuesOut[i].put(data)

  def _broadcastOnlyOne(self, data, owner):
    if owner == "P0":
      self._queuesOut[1].put(data)
    elif owner == "P1":
      self._queuesOut[0].put(data)

  def _startBuses(self):

    for _ in range(2):
      self._queuesOut.append(queue.Queue())

    self._buses.append(
        Bus("P" + str(0), self._chipNumber, self._queuesIn,
             self._queuesOut[0], self._lock, self._mainwin, self._guiQueues[1:3], self._gameMode))
    self._buses.append(
        Bus("P" + str(1), self._chipNumber, self._queuesIn,
             self._queuesOut[1], self._lock, self._mainwin, self._guiQueues[3:5], self._gameMode))
    
    self._buses[0].start()
    self._buses[1].start()

  def run(self):
    self._startBuses()
    counter = 0

    for i in range(2):
      self._queuesOut[i].put("Ready")

    while True:

      busPetition = self._queuesIn.get()
      busSplit = busPetition.split(',')

      # Cache F control
      owner = "{}.{}.{}".format(
          self._chipName, busSplit[0], int(busSplit[1]) % 2)

      busReturn, extFPetition = self._controller.moesiMachineL1(
          busSplit[3], int(busSplit[1]), int(busSplit[2]), owner)

      extFPetition = "{},{},{}".format(extFPetition, busSplit[1], owner)

      # Queue to main memory
      memoryMsg = "{},{},{},{},{}".format(
          busReturn, owner, busSplit[1], busSplit[2], self._chipName)

      self._extLock.acquire()
      self._queueMemOut.put(memoryMsg)
      self._extLock.release()

      memReturn = self._queueMemIn.get()

      # Queue to External F
      self._Fqueue1.put(extFPetition)

      extFReturn = self._Fqueue2.get().split(',')
      #signal, direction, extowner
      # Process external petition
      writeMissF = self._controller.moesiMachineExtF(
          extFReturn[0], int(extFReturn[1]), extFReturn[2])

      # broadcast signal and direction
      if writeMissF:
        print("Alerta de Write Miss")
        self._broadcast("{},{}".format("WM", extFReturn[1]))
      else:
        self._broadcastOnlyOne("{},{}".format(
            busSplit[3], busSplit[1]), busSplit[0])

      # Set processor data in case of Read Miss
      if busSplit[3] == "RM":
        print("Alerta de Read Miss")
        if memReturn is not None:
          self._controller.writeCache(
              int(busSplit[1]), memReturn, [owner])
        if busSplit[0] == "P0":
          if busReturn == "READ" and memReturn is not None:
            self._buses[0].writeCache(int(busSplit[1]), memReturn)
          else:
            self._buses[0].writeCache(int(busSplit[1]), busReturn)

        elif busSplit[0] == "P1":
          if busReturn == "READ" and memReturn is not None:
            self._buses[1].writeCache(int(busSplit[1]), memReturn)
          else:
            self._buses[1].writeCache(int(busSplit[1]), busReturn)

      counter += 1

      self._guiQueues[2].put_nowait(self._buses[0].getCache().getLines())
      self._mainwin.event_generate('<<L1CH{}P0>>'.format(self._chipNumber))

      self._guiQueues[4].put_nowait(self._buses[1].getCache().getLines())
      self._mainwin.event_generate('<<L1CH{}P1>>'.format(self._chipNumber))

      self._guiQueues[0].put_nowait(self._controller.getCache().getLines())
      self._mainwin.event_generate('<<FCH{}>>'.format(self._chipNumber))
