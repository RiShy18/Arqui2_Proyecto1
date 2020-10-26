import queue
import threading
import time

from cache.snooperL1 import SnooperL1
from processor import Processor


class Bus(threading.Thread):
  def __init__(self, name, chipNumber, busQueueOut, busQueueIn, lock, mainwin, guiQueues, gameMode):
    threading.Thread.__init__(self)

    self.cpuQueueOut = queue.Queue()
    self.cpuQueueIn = queue.Queue()
    self.busQueueIn = busQueueIn
    self.busQueueOut = busQueueOut
    self.thread = 0
    self.lock = lock
    self.name = name

    self.chipNumber = chipNumber

    self.mainwin = mainwin
    self.guiQueues = guiQueues
    self.gameMode = gameMode


    self.cacheController = SnooperL1('CH{}{}'.format(chipNumber, name))
    self.cpu = Processor(
        name, chipNumber, self.cpuQueueOut, self.cpuQueueIn, self.mainwin, self.guiQueues[0], self.gameMode)
    
    self.cpu.start()

  def writeCache(self, direction, value):
    self.cacheController.writeCache(direction, value)

    self.guiQueues[1].put_nowait(self.cacheController.getCache().getLines())
    self.mainwin.event_generate(
        '<<L1CH{}{}>>'.format(self.chipNumber, self.name))

  def getCache(self):
    return self.cacheController.getCache()

  def run(self):
    counter = 0
    while True:

      busMsg = self.busQueueIn.get()

      if busMsg != "Ready":
        msgSplit = busMsg.split(',')
        self.cacheController.moesiMachineBus(
            msgSplit[0], int(msgSplit[1]), self.name)
        self.guiQueues[1].put_nowait(
            self.cacheController.getCache().getLines())
        self.mainwin.event_generate(
            '<<L1CH{}{}>>'.format(self.chipNumber, self.name))

      self.cpuQueueIn.put("Ready")
      cpu_msg = self.cpuQueueOut.get().split(',')

      # Check processor signals
      busDataOut = self.cacheController.moesiMachineProcessor(
          cpu_msg[1], int(cpu_msg[2]), int(cpu_msg[3]), self.name)

      self.lock.acquire()

      # Write to bus
      self.busQueueOut.put("{},{},{},{}".format(
          cpu_msg[0], cpu_msg[2], cpu_msg[3], busDataOut))

      self.lock.release()

      counter += 1

      self.guiQueues[1].put_nowait(
          self.cacheController.getCache().getLines())
      self.mainwin.event_generate(
          '<<L1CH{}{}>>'.format(self.chipNumber, self.name))