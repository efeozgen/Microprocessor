def turnToBinary(decimalNum):
    binNum = format(decimalNum, '0{}b'.format(4))
    return binNum

def assemble(instruction):
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
        # Add more opcodes as needed
    }
    
    # Tokenize instruction
    parts = instruction.split(" ")
    op = parts[0]
    operands = parts[1:]
    
    # Get opcode and convert to binary
    binary_instruction = opcode[op]
    if op!="JUMP":
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
        
        # Pad the binary instruction to 18 digits
        binary_instruction = binary_instruction.ljust(18, '0')    
        return binary_instruction
    else: 
        immediate_val = int(operands[0])
        if(immediate_val >= 0):
            binary_instruction += '0' + turnToBinary(immediate_val)    
        else:
            binary_instruction += '1' + turnToBinary(immediate_val)
        binary_instruction = binary_instruction.ljust(18, '0')    
        return binary_instruction

# Read instructions from a file
with open('input.txt', 'r') as file:
    instructions = file.readlines()

# Process each instruction
binary_instructions = []
for instruction in instructions:
    binary_instructions.append(assemble(instruction.strip()))

# Convert binary instructions to hexadecimal
hex_instructions = [hex(int(inst, 2))[2:].zfill(5) for inst in binary_instructions]

# Write hexadecimal instructions to a file
with open('output.txt', 'w') as file:
    file.write("v2.0 raw\n")
    file.write(' '.join(hex_instructions))