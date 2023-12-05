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
imm_bit_positions = {
        'ADD': None,  # Define bit positions for immediate values in respective instructions
        'ADDI': (8, 17),  # For example, immediate value in bits 8-11
        'LD': (4, 17),
        'ST': (4, 17),
        'JE': (0, 17),
        'JB': (0, 18),
        'JAE': (0, 17),
        'JBE': (0, 17),
        'JUMP': (0, 17),
        'ANDI': (8, 17), 
        # Add other instructions and their immediate value positions as needed
    }


def turnToBinary(decimalNum):
    binNum = format(decimalNum, '0{}b'.format(4))
    return binNum

def jumpOp(operand):
    binary_instruction = ""
    immValue = int(operand)
    if(immValue>= 0):
        binary_instruction = '0' + turnToBinary(immValue)
    return binary_instruction

def notJumpOp(operands):
    binary_instruction = ""
    for i, operand in enumerate(operands):
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
                # Clear bits in the specified immediate value position
                mask = (1 << (imm_bit_positions[i][1] - imm_bit_positions[i][0] + 1)) - 1
                immediate_val &= mask
                # Spread the immediate value to its designated bits
                binary_instruction += turnToBinary(immediate_val).zfill(imm_bit_positions[i][1] - imm_bit_positions[i][0] + 1)
    return binary_instruction

def assemble(instruction):
    parts = instruction.split(" ")
    op = parts[0]
    operands = parts[1:]
    
    binary_instruction = opcode[op]
    if op!="JUMP":
        binary_instruction += notJumpOp(operands)
    else: 
        binary_instruction += jumpOp(operands[0])
    return binary_instruction.ljust(18, '0')

with open('input.txt', 'r') as file:
    instructions = file.readlines()

binary_instructions = []

for instruction in instructions:
    binary_instructions.append(assemble(instruction.strip()))
print(binary_instructions)
hex_instructions = [hex(int(inst, 2))[2:].zfill(5) for inst in binary_instructions]

with open('output.txt', 'w') as file:
    file.write("v2.0 raw\n")
    file.write(' '.join(hex_instructions))

with open('output.hex', 'w') as file:
    file.write('\n'.join(hex_instructions))