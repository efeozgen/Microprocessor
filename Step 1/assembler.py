currentTotalBit = 4

opcode = {
        'ADD': '0000',
        'ADDI': '0100',
        'LD': '0110',
        'ST': '0111',
        'CMP': '1000',
        'JE': '1010',
        'JA': '1011',
        'JB': '1100',
        'JAE': '1101',
        'JBE': '1110',
        'AND': '0001',
        'NOR': '0011',
        'ANDI': '0101',
        'NAND': '0010',
        'JUMP': '1001'
    }

def turnToBinary(decimalNum):
    global currentTotalBit
    currentTotalBit += 4
    binNum = format(decimalNum, '0{}b'.format(4))
    print(binNum)
    return binNum

def turnImmToBinary(decimalNum):
    global currentTotalBit
    bit = 18-currentTotalBit
    binNum = format(decimalNum, '0{}b'.format(bit))
    return binNum

def jumpOp(operand):
    global currentTotalBit
    binary_instruction = ""
    immValue = int(operand)
    if(immValue>= 0):
        currentTotalBit += 1
        binary_instruction = '0' + turnImmToBinary(immValue)
    else:
        currentTotalBit += 1
        binary_instruction = '1' + turnImmToBinary(-immValue)
    return binary_instruction

def cmpOp(operands):
    global currentTotalBit
    binary_instruction = ""
    iteration = True
    for operand in operands:
        if len(operand)==3:
            if operand[len(operand)-1]==",":
                register_num = int(operand[1])
                binary_instruction += turnToBinary(register_num)
            else:
                register_num = int(operand[1:3])
                print(register_num)
                binary_instruction += turnToBinary(register_num)
        else:
            register_num = int(operand[1:3])
            print(register_num)
            binary_instruction += turnToBinary(register_num)
        if iteration:
            binary_instruction += "000000"
            iteration = False
    return binary_instruction

def notJumpOp(operands):
    binary_instruction = ""
    for operand in operands:
        if operand.startswith('R'):
            if len(operand)==3:
                if operand[len(operand)-1]==",":
                    register_num = int(operand[1])
                    binary_instruction += turnToBinary(register_num)
                else:
                    register_num = int(operand[1:3])
                    print(register_num)
                    binary_instruction += turnToBinary(register_num)
            else:
                register_num = int(operand[1:3])
                print(register_num)
                binary_instruction += turnToBinary(register_num)
        else:
            # Assume immediate value
            immediate_val = int(operand)
            binary_instruction += turnImmToBinary(immediate_val)
    return binary_instruction

def assemble(instruction):
    parts = instruction.split(" ")
    op = parts[0]
    operands = parts[1:]
    
    binary_instruction = opcode[op]
    if op!="JUMP" and op !="CMP":
        binary_instruction += notJumpOp(operands)
    elif op == "CMP":
        binary_instruction += cmpOp(operands)
    else: 
        binary_instruction += jumpOp(operands[0])
    return binary_instruction.ljust(18, '0')


with open('input.txt', 'r') as file:
    instructions = file.readlines()

binary_instructions = []

for instruction in instructions:
    currentTotalBit = 4
    binary_instructions.append(assemble(instruction.strip()))
print(binary_instructions)
hex_instructions = [hex(int(inst, 2))[2:].zfill(5) for inst in binary_instructions]

with open('output.txt', 'w') as file:
    file.write("v2.0 raw\n")
    file.write(' '.join(hex_instructions))
with open('output.hex', 'w') as file:
    file.write('\n'.join(hex_instructions))