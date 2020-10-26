import tkinter as tk

import queue
import shutil
import os
import time
import threading
from pynput import keyboard

from cpuSystem import CpuSystem
from table import Table

print("Ingrese el modo de uso: 1-Infinito, 2-Limitado, 3-Paso a paso")
gamemode=input()
if (int(gamemode)==2):
  print("Cuantas rondas de instrucciones desea ejecutar?")
  f=input()
  limit=int(f)
  print("Ejecutando: " + str(limit) + " rondas")


root = tk.Tk()

titlesL1 = ['Bloque', 'Estado', 'Dirección', 'Dato']
titlesF = ['Bloque', 'Estado', 'Dueño', 'Dirección', 'Dato']
titlesMem = ['Dirección', 'Dueño', 'Dato']

tableTitlesL1 = ['Cache L1 P1 CH1', 'Cache L1 P2 CH1',
                 'Cache L1 P3 CH2', 'Cache L1 P4 CH2']
tableTitlesF = ['Cache F CH0', 'Cache F CH1']
labelProcessorTitles = ['P1 CH0', 'P2 CH0', 'P3 CH1', 'P4 CH1']
lastInsLabel= ['P1 ', 'P2 ', 'P3 ', 'P4 ']

bgColor = '#03fcb6'

l1Arr = []
FArr = []
pArr = []
tMem = None
marker = 0
limit=10


def processProcessorLabel(storage, event, label):
  msg = storage.get().split(',')
  text = tk.StringVar()
  if msg[0] == 'READ':
    binValue = int(msg[1])
    toBin = bin(binValue)
    text.set('{},{}'.format(msg[0], toBin))
  elif msg[0] == 'CALC':
    text.set(msg[0])
  else:
    hexValue = int(msg[2])
    binValue = int(msg[1])
    toBin = bin(binValue)
    text.set('{},{},{}'.format(msg[0], "{:0b}".format(binValue), '{:04X}'.format(hexValue)))

  label.config(textvariable=text)

def confirm(cpuSystem): #set event to None to take the key argument from .bind
    CpuSystem
    print('Function successfully called!') #this will output in the shell

def processPreviousInsLabel(storage, event, label):
  msg = storage.get().split(',')
  text = tk.StringVar()
  if msg[0] == 'READ':
    binValue = int(msg[1])
    toBin = bin(binValue)
    text.set('{},{}'.format(msg[0], toBin))
  elif msg[0] == 'CALC':
    text.set(msg[0])
  else:
    hexValue = int(msg[2])
    binValue = int(msg[1])
    text.set('{},{},{}'.format(msg[0], "{:0b}".format(binValue), '{:04X}'.format(hexValue)))

  label.config(textvariable=text)


def processL1Tables(storage, event, table):
  msg = storage.get()

  for i in range(4):
    table.set(i + 1, 1, msg[i].getState())
    table.set(i + 1, 2, "{:0b}".format(int(msg[i].getTag()))) #msg[i].getTag()
    table.set(i + 1, 3, '{:04X}'.format(msg[i].getData()))



def processMemTables(storage, event, table):
  msg = storage.get()
  aux= 0

  for i in range(16):
    if msg[i].getOwner()== "CH0.P0.0" or msg[i].getOwner() == "CH0.P0.1":
      aux= "P1.CH1"
    elif msg[i].getOwner() == "CH0.P1.1" or msg[i].getOwner() == "CH0.P1.0":
      aux= "P2.CH1"
    elif msg[i].getOwner() == "CH1.P0.0" or msg[i].getOwner() == "CH1.P0.1":
      aux= "P3.CH2"
    elif msg[i].getOwner() == "CH1.P1.1" or msg[i].getOwner() == "CH1.P1.0":
      aux= "P4.CH2"
    else:
      aux= "0"

    table.set(i + 1, 1, aux)
    table.set(i + 1, 2, '{:04X}'.format(msg[i].getData()))


def createProcessorLabel():
  global pArr

  x1 = [30, 350, 670, 985]
  x2 = [170, 490, 810, 1130]

  y = 10
  # Procesor instructions
  for i in range(4):
    label = tk.Label(root)
    label.config(bg=bgColor, text='Procesador {}: '.format(
        labelProcessorTitles[i]))
    label.place(x=x1[i], y=y)

  for i in range(4):
    pLabel = tk.Label(root)

    pLabel.config(bg=bgColor)
    pLabel.place(x=x2[i], y=y)
    pArr.append(pLabel)

def createLastInsLabel():
  global pArr

  x1 = [30, 350, 670, 985]
  x2 = [170, 490, 810, 1130]

  y = 60
  # Procesor last instructions
  for i in range(4):
    label = tk.Label(root)
    label.config(bg=bgColor, text='Última instrucción de {}: '.format(
        lastInsLabel[i]))
    label.place(x=x1[i], y=y)

  for i in range(4):
    pLabel = tk.Label(root)
    pLabel.config(bg=bgColor)
    pLabel.place(x=x2[i], y=y)
    pArr.append(pLabel)


def createL1Tables():
  global l1Arr

  offset = 320
  x = [120, 440, 760, 1080]
  y1 = 80
  y2 = 100
  # L1 tables

  for i in range(4):
    title = tk.Label(root)
    title.config(bg=bgColor, text=tableTitlesL1[i])
    title.place(x=x[i], y=y1)

  for i in range(4):
    t = Table(root, 5, 4)
    t.createTable(titlesL1, '#5696fc', 'white', True, False, None)
    t.place(x=15 + (offset * i), y=y2)
    l1Arr.append(t)



def createMemoryTable():
  global tMem
  # Memory Table
  titleMem = tk.Label(root)
  titleMem.config(bg=bgColor, text='Memoria Principal')
  titleMem.place(x=570, y=330)

  tMem = Table(root, 17, 3)
  tMem.createTable(titlesMem, '#5696fc', 'white', False, True, 1)
  tMem.place(x=495, y=350)



def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False






def main():
  #print("Modo de juego": str(gamemode))
  global tMem, l1Arr, FArr, pArr
  global gamemode

  run_event = threading.Event()
  run_event.set()

  queueArr = []

  createProcessorLabel()
  createL1Tables()
  createMemoryTable()
  createLastInsLabel()
  

  for _ in range(15): #Inicial 11
    queueArr.append(queue.Queue())
  

  # Processor Labels Events
  root.bind('<<P0CH0>>', lambda e: processProcessorLabel(
      queueArr[2], e, pArr[0]))

  root.bind('<<P1CH0>>', lambda e: processProcessorLabel(
      queueArr[4], e, pArr[1]))

  root.bind('<<P0CH1>>', lambda e: processProcessorLabel(
      queueArr[7], e, pArr[2]))

  root.bind('<<P1CH1>>', lambda e: processProcessorLabel(
      queueArr[9], e, pArr[3]))
  
  # Processor Last Ins Labels Events
  root.bind('<<P0CH0L>>', lambda e: processPreviousInsLabel(
      queueArr[2], e, pArr[4]))

  root.bind('<<P1CH0L>>', lambda e: processPreviousInsLabel(
      queueArr[4], e, pArr[5]))

  root.bind('<<P0CH1L>>', lambda e: processPreviousInsLabel(
      queueArr[7], e, pArr[6]))

  root.bind('<<P1CH1L>>', lambda e: processPreviousInsLabel(
      queueArr[9], e, pArr[7]))

  # L1 Tables Events
  root.bind('<<L1CH0P0>>', lambda e: processL1Tables(
      queueArr[3], e, l1Arr[0]))

  root.bind('<<L1CH0P1>>', lambda e: processL1Tables(
      queueArr[5], e, l1Arr[1]))

  root.bind('<<L1CH1P0>>', lambda e: processL1Tables(
      queueArr[8], e, l1Arr[2]))

  root.bind('<<L1CH1P1>>', lambda e: processL1Tables(
      queueArr[10], e, l1Arr[3]))

  # Memory Table Event
  root.bind('<<MEM>>', lambda e: processMemTables(
      queueArr[0], e, tMem))

  cpu = CpuSystem(queueArr, root, limit, int(gamemode))

  def Quit(event):
    print("Interrupcion")
    cpu.setPause()

  cpu.start()




  





  
  root.bind('<Control-c>', Quit)


 




  root.configure(background=bgColor)
  root.attributes('-fullscreen', True)
  root.mainloop()




if __name__ == "__main__":
  main()

