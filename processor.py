import numpy as np
import time
import threading




def binary_to_decimal(binary): 
    decimal = 0 
    binary = list(str(binary)) #convert binary to a list 
    binary = binary[::-1]      #reverse the list 
    power = 0   #declare power variable (for 1st elem == 0) 
    for number in binary: 
        if number == '1': 
            decimal += 2**power     
        power += 1 #increase power by 1    
    return decimal

class Processor(threading.Thread):
  def __init__(self, name, chipNumber, storageOut, storageIn, mainwin, guiQueue, gameMode):
    threading.Thread.__init__(self)

    self._name = name
    self._chipNumber = chipNumber
    self._instructions = ["READ", "CALC", "WRITE"]
    self._storageOut = storageOut
    self._storageIn = storageIn
    self._intHistory = []

    self._mainwin = mainwin
    self._guiQueue = guiQueue

    self._gameMode = gameMode
    self._triggerFlag=False





  def run(self):

    counter = 0
   # manual= True

    while True:

        self._storageIn.get()


        if self._gameMode != 3:

            instr = round(np.random.normal(1, 1)) % 3
            direction = round(np.random.normal(8, 4)) % 16
            dirValue = round(np.random.normal(32768, 10000)) % 65536
            cpuSignal = self._instructions[instr]

            message = "{},{},{},{}".format(
            self._name, cpuSignal, direction, dirValue)

            

            self._storageOut.put(message)

            self._guiQueue.put_nowait(
                '{},{},{}'.format(cpuSignal, direction, dirValue))
            self._mainwin.event_generate(
                '<<{}CH{}>>'.format(self._name, self._chipNumber))

            

            if counter !=0:
                self._guiQueue.put_nowait(
                    tmp)
                self._mainwin.event_generate(
                    '<<{}CH{}L>>'.format(self._name, self._chipNumber))
            
            tmp= '{},{},{}'.format(cpuSignal, direction, dirValue)
            self._intHistory.append(tmp)

            time.sleep(3)

            counter += 1
        
        else:
            
            if self._triggerFlag==True:
                nice=input("Digite la inst para el procesador "+ str(self._name)+ ": ")
                instr=nice
                #time.sleep(30)
                if instr == "WRITE" or "write":
                    instr = 2
                    nice2=input("Donde quiere escribir?: "+ str(self._name))
                    direction = binary_to_decimal(nice2)
                    nice3=input("Que valor quiere escribir?: "+ str(self._name))
                    dirValue = int(nice3, 16)
                    cpuSignal = self._instructions[instr]
                elif instr == "READ" or instr == "read":
                    instr= 0
                    nice2=input("Donde quiere leer?: "+ str(self._name))
                    direction = binary_to_decimal(nice2)
                    dirValue = round(np.random.normal(32768, 10000)) % 65536
                    cpuSignal = self._instructions[instr]
                else:
                    instr = 1
                    direction=9
                    dirValue=1
                    cpuSignal = self._instructions[instr]
            else:
                instr = round(np.random.normal(1, 1)) % 3
                direction = round(np.random.normal(8, 4)) % 16
                dirValue = round(np.random.normal(32768, 10000)) % 65536
                cpuSignal = self._instructions[instr]

                    

            message = "{},{},{},{}".format(
            self._name, cpuSignal, direction, dirValue)

            

            self._storageOut.put(message)

            self._guiQueue.put_nowait(
                '{},{},{}'.format(cpuSignal, direction, dirValue))
            self._mainwin.event_generate(
                '<<{}CH{}>>'.format(self._name, self._chipNumber))

            

            if counter !=0:
                self._guiQueue.put_nowait(
                    tmp)
                self._mainwin.event_generate(
                    '<<{}CH{}L>>'.format(self._name, self._chipNumber))
            
            tmp= '{},{},{}'.format(cpuSignal, direction, dirValue)
            self._intHistory.append(tmp)

            time.sleep(3)

            counter += 1
            

        
"""
        if self._gameMode == 3:
            patito= input("Desea ingresar instrucciones en este ciclo? (Y/n)")
            if patito == "Y" or patito == "y":
                manual=True
            else:
                manual=False
"""
    