from tkinter import *
from tkinter import scrolledtext
import modbus_describtion as md

class cBmsGUI:

    def __init__(self, title:str) -> None:
        self.modbus = None
        self.window = Tk()
        self.window.geometry('700x950')
        self.window.title(title)

        self.holding_regs = md.GetHoldingRegisters()
        self.input_regs   = md.GetInputRegisters()

        self.AddHoldingRegisters()
        self.AddInputRegisters()

        self.window.mainloop()

    def AddHoldingRegisters(self):
        _column = 0
        _row = 0
        for hr in self.holding_regs:
            label = Label(self.window, text = hr.get(md.KEY_REG_NAME))
            label.grid(column = _column, row = _row)
            _row += 1

    def AddInputRegisters(self):
        _column = 1
        _row = 0
        for hr in self.input_regs:
            label = Label(self.window, text = hr.get(md.KEY_REG_NAME))
            label.grid(column = _column, row = _row)
            _row += 1
