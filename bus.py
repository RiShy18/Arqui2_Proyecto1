import queue
import threading
import time

from cache.snooperL1 import SnooperL1
from processor import Processor


class Bus(threading.Thread):
  def __init__(self, name, chipNumber, busQueueOut, busQueueIn, lock, mainwin, guiQueues, gameMode):
    threading.Thread.__init__(self)

    self._cpuQueueOut = queue.Queue()
    self._cpuQueueIn = queue.Queue()
    self._busQueueIn = busQueueIn
    self._busQueueOut = busQueueOut
    self._thread = 0
    self._lock = lock
    self._name = name

    self._chipNumber = chipNumber

    self._mainwin = mainwin
    self._guiQueues = guiQueues
    self._gameMode = gameMode


    self._cacheController = SnooperL1('CH{}{}'.format(chipNumber, name))
    self._cpu = Processor(
        name, chipNumber, self._cpuQueueOut, self._cpuQueueIn, self._mainwin, self._guiQueues[0], self._gameMode)
    
    self._cpu.start()

  def writeCache(self, direction, value):
    self._cacheController.writeCache(direction, value)

    self._guiQueues[1].put_nowait(self._cacheController.getCache().getLines())
    self._mainwin.event_generate(
        '<<L1CH{}{}>>'.format(self._chipNumber, self._name))

  def getCache(self):
    return self._cacheController.getCache()

  def run(self):
    counter = 0
    while True:

      bus_msg = self._busQueueIn.get()

      if bus_msg != "Ready":
        msgSplit = bus_msg.split(',')
        self._cacheController.moesiMachineBus(
            msgSplit[0], int(msgSplit[1]), self._name)
        self._guiQueues[1].put_nowait(
            self._cacheController.getCache().getLines())
        self._mainwin.event_generate(
            '<<L1CH{}{}>>'.format(self._chipNumber, self._name))

      self._cpuQueueIn.put("Ready")
      cpu_msg = self._cpuQueueOut.get().split(',')

      # Check processor signals
      busDataOut = self._cacheController.moesiMachineProcessor(
          cpu_msg[1], int(cpu_msg[2]), int(cpu_msg[3]), self._name)

      self._lock.acquire()

      # Write to bus
      self._busQueueOut.put("{},{},{},{}".format(
          cpu_msg[0], cpu_msg[2], cpu_msg[3], busDataOut))

      self._lock.release()

      counter += 1

      self._guiQueues[1].put_nowait(
          self._cacheController.getCache().getLines())
      self._mainwin.event_generate(
          '<<L1CH{}{}>>'.format(self._chipNumber, self._name))