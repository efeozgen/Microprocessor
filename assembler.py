OPCODES = {
    'ADD': '00000',
    'AND': '00001',
    'NAND': '00010',
    'NOR': '00011',
    'ADDI': '00100',
    'ANDI': '00101',
    'LD': '00110',
    'ST': '00111',
    'CMP': '01000',
    'JUMP': '01001',
    'JE': '01010',
    'JA': '01011',
    'JB': '01100',
    'JAE': '01101',
    'JBE': '01110'
    # Add more as needed
}

REGISTER_PREFIX = 'R'
MAX_REGISTER_NUMBER = 15
IMMEDIATE_BITS = 10  # Assuming 10-bit immediate values for ADDI and JUMP

def extract_register(register_str):
    try:
        register_num = int(register_str[len(REGISTER_PREFIX):])
        if 0 <= register_num <= MAX_REGISTER_NUMBER:
            return format(register_num, '04b')
    except ValueError:
        pass
    raise ValueError(f"Invalid register: {register_str}")

def extract_immediate(immediate_str):
    try:
        immediate_value = int(immediate_str)
        return format(immediate_value, f'0{IMMEDIATE_BITS}b')
    except ValueError:
        raise ValueError(f"Invalid immediate value: {immediate_str}")

def assemble(instruction):
    parts = instruction.split()
    opcode = OPCODES.get(parts[0])
    if opcode is None:
        raise ValueError(f"Invalid opcode: {parts[0]}")

    if parts[0] in ['JUMP', 'JE', 'JA', 'JB', 'JAE', 'JBE']:
        if len(parts) != 2:
            raise ValueError(f"Invalid format for {parts[0]} instruction")
        address = extract_immediate(parts[1])
        machine_code = opcode + address
    else:
        if len(parts) != 4:
            raise ValueError(f"Invalid format for {parts[0]} instruction")
        dest_reg = extract_register(parts[1])
        src_reg1 = extract_register(parts[2])
        src_reg2 = extract_register(parts[3])
        machine_code = opcode + dest_reg + src_reg1 + src_reg2

    return format(int(machine_code, 2), '05X')

def main():
    assembly_code = [
        'ADD R5, R0, R2',
        'ADDI R3, R1, 12',
        'JUMP 3',
        'LD R5, 12',
        'ST R3, 15',
        'CMP R2, R4',
        'JE 8',
        # Add more instructions
    ]

    for instruction in assembly_code:
        try:
            machine_code = assemble(instruction)
            print(f"{instruction} -> {machine_code}")
        except ValueError as e:
            print(f"Error in '{instruction}': {e}")

if __name__ == "__main__":
    main()
