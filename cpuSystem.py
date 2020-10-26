import threading
import queue
import time

from chipSet import ChipSet
from mainMemory import MainMemory


class CpuSystem(threading.Thread):

  def __init__(self, guiQueues, mainwin, limit, gameMode):
    threading.Thread.__init__(self)

    self._guiQueues = guiQueues
    self._mainwin = mainwin
    self._Limit=False
    self._flag = False #Pause event
    #self._flag.set() #As True
    self._triggerins=False
    self.endThread= limit
    self._running = threading.Event() # Used to stop the thread identification
    self._running.set() # Set running to True
    self.gameMode= int(gameMode)

    self._chipQueueIn = []
    self._chipQueueOut = queue.Queue()

    self._memory = MainMemory()
    self._chipLock = threading.Lock()

    self._Fqueue1 = queue.Queue()
    self._Fqueue2 = queue.Queue()

    self.stopped = False

    self._chips = []
    #var=gameMode
    if self.gameMode==2:
      print("OKAY")
  

  

  def _startChips(self):
    for _ in range(2):
      self._chipQueueIn.append(queue.Queue())

    self._chips.append(
        ChipSet(0, self._chipLock, self._chipQueueIn[0], self._chipQueueOut,
             self._Fqueue1, self._Fqueue2, self._guiQueues[1:6], self._mainwin, self.gameMode))

    self._chips.append(
        ChipSet(1, self._chipLock, self._chipQueueIn[1], self._chipQueueOut,
             self._Fqueue2, self._Fqueue1, self._guiQueues[6:11], self._mainwin, self.gameMode))

    self._chips[0].start()
    self._chips[1].start()
  
  def setPause(self):
    if self._flag==False:
      self._flag = True # Set to False to block the thread
      print("Pausando")
    else:
      self._flag= False
  
  def resume(self):
        self._flag = False # Set to True, let the thread stop blocking
  
  #def stop(self):
  #      self._flag.set() # Resume the thread from the suspended state, if it is already suspended
  #      self._running.clear() # Set to False


  def run(self):
      self._startChips()
      counter = 0
      var=self.gameMode

      if int(var)==2:
          #print("OKAY2")
          while int(var)==2 and counter//4 < self.endThread: 
            #while self._flag != False:

              
      

              memoryPetition = self._chipQueueOut.get().split(',')

              time.sleep(1)
              memoryReturn = self._memory.controlMemory(
                  memoryPetition[0], memoryPetition[1], int(memoryPetition[2]),
                  int(memoryPetition[3]), memoryPetition[4])

              if memoryPetition[4] == "CH0":
                self._chipQueueIn[0].put(memoryReturn)
              elif memoryPetition[4] == "CH1":
                self._chipQueueIn[1].put(memoryReturn)
            

              self._guiQueues[0].put_nowait(self._memory.getMem())
              self._mainwin.event_generate('<<MEM>>')

                  

              counter += 1

              print("Counter = {}".format(counter) + """ 
                                                        """)
      
      elif var==1:

          while True:
              memoryPetition = self._chipQueueOut.get().split(',')

              time.sleep(1)
              memoryReturn = self._memory.controlMemory(
                  memoryPetition[0], memoryPetition[1], int(memoryPetition[2]),
                  int(memoryPetition[3]), memoryPetition[4])

              if memoryPetition[4] == "CH0":
                self._chipQueueIn[0].put(memoryReturn)
              elif memoryPetition[4] == "CH1":
                self._chipQueueIn[1].put(memoryReturn)
            

              self._guiQueues[0].put_nowait(self._memory.getMem())
              self._mainwin.event_generate('<<MEM>>')

              counter += 1

              print("Counter = {}".format(counter) + """ 
                                                        """)

              if self._flag==True:
                while True:
                  if self._flag==False:
                    break
      
      elif var==3:


          while True:

              ok=input("Desea ingresar instrucciones este ciclo? Y/n:" + """
                                                                            """)
              if ok== "Y" or ok == "y":
                self._chips[0]._buses[0].cpu._triggerFlag=True
                self._chips[0]._buses[1].cpu._triggerFlag=True
                self._chips[1]._buses[0].cpu._triggerFlag=True
                self._chips[1]._buses[1].cpu._triggerFlag=True
              else:
                self._chips[0]._buses[0].cpu._triggerFlag=False
                self._chips[0]._buses[1].cpu._triggerFlag=False
                self._chips[1]._buses[0].cpu._triggerFlag=False
                self._chips[1]._buses[1].cpu._triggerFlag=False 
              #ok=input("Presione enter para ver los cambios :3")
              memoryPetition = self._chipQueueOut.get().split(',')

              memoryReturn = self._memory.controlMemory(
                  memoryPetition[0], memoryPetition[1], int(memoryPetition[2]),
                  int(memoryPetition[3]), memoryPetition[4])

              if memoryPetition[4] == "CH0":
                self._chipQueueIn[0].put(memoryReturn)
              elif memoryPetition[4] == "CH1":
                self._chipQueueIn[1].put(memoryReturn)
            

              self._guiQueues[0].put_nowait(self._memory.getMem())
              self._mainwin.event_generate('<<MEM>>')

              counter += 1

              print("Counter = {}".format(counter) + """ 
                                                        """)

              if self._flag==True:
                while True:
                  if self._flag==False:
                    break

                  

              
