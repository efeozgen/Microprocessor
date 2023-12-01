opcode = {
        'ADD': '0000',
        'ADDI': '0001',
        'LD': '0011',
        'ST': '0100',
        'CMP': '0101',
        'JE': '0110',
        'JA': '0111',
        'JB': '1000',
        'JAE': '1001',
        'JBE': '1010',
        'AND': '1011',
        'NOR': '1100',
        'ANDI': '1101',
        'NAND': '1110',
        'JUMP': '0010'
    }

def turnToBinary(decimalNum):
    binNum = format(decimalNum, '0{}b'.format(4))
    return binNum

def completer(binary_instruction):
    binary_instruction = binary_instruction.ljust(18, '0')
    return binary_instruction

def jumpOp(operand):
    binary_instruction = ""
    immValue = int(operand)
    if(immValue>= 0):
        binary_instruction = '0' + turnToBinary(immValue)
    return completer(binary_instruction)

def notJumpOp(operands):
    binary_instruction = ""
    for operand in operands:
        if operand.startswith('R'):
            if len(operand)==3:
                register_num = int(operand[1])
                binary_instruction += turnToBinary(register_num)
            else:
                register_num = int(operand[1:3])
                binary_instruction += turnToBinary(register_num)
        else:
            # Assume immediate value
            immediate_val = int(operand)
            binary_instruction += turnToBinary(immediate_val)
    return completer(binary_instruction)

def assemble(instruction):
    parts = instruction.split(" ")
    op = parts[0]
    operands = parts[1:]
    
    binary_instruction = opcode[op]
    if op!="JUMP":
        binary_instruction += notJumpOp(operands)
    else: 
        binary_instruction += jumpOp(operands[0])
    return binary_instruction

with open('input.txt', 'r') as file:
    instructions = file.readlines()

binary_instructions = []

for instruction in instructions:
    binary_instructions.append(assemble(instruction.strip()))

hex_instructions = [hex(int(inst, 2))[2:].zfill(5) for inst in binary_instructions]

with open('output.hex', 'w') as file:
    file.write("v2.0 raw\n")
    file.write(' '.join(hex_instructions))