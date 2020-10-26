import tkinter as tk


class Table(tk.Frame):
  def __init__(self, parent, rows, columns):

    tk.Frame.__init__(self, parent, background="black")
    self._widgets = []
    self._rows = rows
    self._columns = columns

  def createTable(self, titles, titleColor, color, isCache, haveOwner, ownerPosition):
    for row in range(self._rows):
      current_row = []
      for column in range(self._columns):
        if row == 0:
          if haveOwner and column == ownerPosition:
            label = tk.Label(
                self, bg=titleColor, text=titles[column], borderwidth=0, width=15, font='Helvetica 10 bold')
          else:
            label = tk.Label(
                self, bg=titleColor, text=titles[column], borderwidth=0, width=9, font='Helvetica 10 bold')
        else:
          if haveOwner and column == ownerPosition:
            label = tk.Label(self, bg=color, borderwidth=0, width=15)
          else:
            label = tk.Label(self, bg=color, borderwidth=0, width=9)
        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
        current_row.append(label)
      self._widgets.append(current_row)

    for column in range(self._columns):
      self.grid_columnconfigure(column, weight=1)

    if isCache:
      self._setBlockCache()
    else:
      self._setBlockMemory()

  def _setBlockCache(self):
    for row in range(self._rows):
      if row > 0:
        self.set(row, 0, row - 1)

  def _setBlockMemory(self):
    for row in range(self._rows):
      if row > 0:
        self.set(row, 0, format(row - 1, '#06b').replace('0b', ''))

  def set(self, row, column, value):
    widget = self._widgets[row][column]
    widget.configure(text=value)
