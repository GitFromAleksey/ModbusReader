import modbus_describtion as md
from pymodbus.client import ModbusSerialClient as ModbusClient

class cModbusRtuClient:

    def __init__(self,        
                 _port = 'COM1',
                _stopbits = 1,
                _bytesize = 8,
                _parity = 'N' ,
                _baudrate = 19200) -> None:
        
        self.client = ModbusClient(
                                    method = 'rtu', 
                                    port = _port, 
                                    stopbits = _stopbits, 
                                    bytesize = _bytesize, 
                                    parity = _parity , 
                                    baudrate = _baudrate, 
                                    # handle_local_echo = False,
                                    # retries = 4,
                                    # retry_on_empty = True,
                                    timeout = 0.2,
                                    strict = False # отключение жесткой паузы ожидания ответа (silent time)
                                )
        
        self.holding_regs = md.GetHoldingRegisters()
        self.input_regs   = md.GetInputRegisters()

        if self.OpenPort():
            pass # запуск потока чтения регистров

    def OpenPort(self) -> bool:
        if self.client.is_socket_open() == False:
            self.client.connect()
            return True
        return False

    def ClosePort(self):
        if self.client.is_socket_open() == True:
            self.client.close()

    def ReadOneHoldingReg(self, unit_id, reg_addr):
        if not self.client.is_socket_open():
            return (False, None)

        rh = self.client.read_holding_registers(slave=unit_id, address=reg_addr, count=1)
        if rh.isError():
            return (False, None)
        
        return (True, rh.registers[0])
    
    def ReadAllRegisters(self):
        device_id = md.GetDeviceID()
        for hr in self.holding_regs:
            self.ReadOneHoldingReg(unit_id=device_id, reg_addr = hr.get(md.KEY_REG_ADDR))