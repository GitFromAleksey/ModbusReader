import modbus_describtion as md
import gui
from modbus_rtu import cModbusRtuClient
            

def main():
    # print(md.ReadFromConfigFile())
    print(md.GetSerialPortName())
    print(md.GetInputRegisters())
    print(md.GetHoldingRegisters())
    modbus = cModbusRtuClient(md.GetSerialPortName())
    modbus.ReadAllRegisters()
    gui.cBmsGUI('BMS GUI v1')

if __name__ == '__main__':
    main()
