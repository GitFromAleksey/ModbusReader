import json
import re

CONFIG_FILE_NAME = 'bms_config.json'

KEY_SERIAL_PORT  = 'serial_port'
KEY_DEVICE_ID    = 'device_id'
KEY_MODBUS_REGS  = 'modbus_regs'
KEY_INPUT_REGS   = 'input_regs'
KEY_HOLDING_REGS = 'holding_regs'

KEY_REG_NAME = 'reg_name'
KEY_REG_ADDR = 'reg_addr'
KEY_REG_TYPE = 'reg_type'
KEY_REG_SIZE = 'reg_size'
KEY_REG_VALUE = 'reg_value'

RE_PATT_HEX_DIGIT = re.compile(r'0x[a-fA-F0-9]+')

CONFIG_STRUCT = None

CONFIG_DEFAULT_STRUCT = { 
    KEY_SERIAL_PORT : 'COM1',
    KEY_DEVICE_ID   : 32,
    KEY_MODBUS_REGS : { 
        KEY_INPUT_REGS : 
        [ 
            { 
                KEY_REG_NAME  : 'name_1',
                KEY_REG_ADDR  : '1',
                KEY_REG_TYPE  : 'uint16',
                KEY_REG_SIZE  : 1,
                KEY_REG_VALUE : 0
            },
            { 
                KEY_REG_NAME  : 'name_2',
                KEY_REG_ADDR  : '2',
                KEY_REG_TYPE  : 'uint16',
                KEY_REG_SIZE  : 1,
                KEY_REG_VALUE : 0
            }
              ], 
        KEY_HOLDING_REGS: [ 
            {
                KEY_REG_NAME  : 'name_1',
                KEY_REG_ADDR  : '0x4000',
                KEY_REG_TYPE  : 'uint16',
                KEY_REG_SIZE  : 1,
                KEY_REG_VALUE : 0
            },
            {
                KEY_REG_NAME  : 'name_2',
                KEY_REG_ADDR  : '2',
                KEY_REG_TYPE  : 'uint16',
                KEY_REG_SIZE  : 1,
                KEY_REG_VALUE : 0
            }
              ] } }

# ------------------------------------------------------------------------------
def ConvertRegAddrToInt():
    global CONFIG_STRUCT
    registers = CONFIG_STRUCT.get(KEY_MODBUS_REGS)
    input     = registers.get(KEY_INPUT_REGS)
    holding   = registers.get(KEY_HOLDING_REGS)
    for hr in holding:
        res = re.search(RE_PATT_HEX_DIGIT, hr.get(KEY_REG_ADDR))
        if res:
            hr[KEY_REG_ADDR] = int(res.group(), 16)
        else:
            hr[KEY_REG_ADDR] = int(res.group())
    for ir in input:
        res = re.search(RE_PATT_HEX_DIGIT, ir.get(KEY_REG_ADDR))
        if res:
            ir[KEY_REG_ADDR] = int(res.group(), 16)
        else:
            ir[KEY_REG_ADDR] = int(res.group())

def ReadFromConfigFile() -> bool:
    global CONFIG_STRUCT
    try:
        with open(CONFIG_FILE_NAME, 'r') as f:
            modbus_descr = f.read()
            CONFIG_STRUCT = json.loads(modbus_descr)
            ConvertRegAddrToInt()
            return True
    except:
        with open(CONFIG_FILE_NAME, 'w') as f:
            f.write(json.dumps(CONFIG_DEFAULT_STRUCT, indent = 4))
            CONFIG_STRUCT = CONFIG_DEFAULT_STRUCT
            ConvertRegAddrToInt()
            return False
# ------------------------------------------------------------------------------
def GetSerialPortName() -> str:
    global CONFIG_STRUCT
    return CONFIG_STRUCT.get(KEY_SERIAL_PORT)
# ------------------------------------------------------------------------------
def GetDeviceID() -> int:
    global CONFIG_STRUCT
    return CONFIG_STRUCT.get(KEY_DEVICE_ID)
# ------------------------------------------------------------------------------
def GetHoldingRegisters():
    global CONFIG_STRUCT
    return CONFIG_STRUCT.get(KEY_MODBUS_REGS).get(KEY_HOLDING_REGS)
# ------------------------------------------------------------------------------
def GetInputRegisters():
    global CONFIG_STRUCT
    return CONFIG_STRUCT.get(KEY_MODBUS_REGS).get(KEY_INPUT_REGS)
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
ReadFromConfigFile()
# ------------------------------------------------------------------------------
