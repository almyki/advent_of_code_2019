
filename = 'AdventOfCode_2019_5.txt'

with open(filename) as f:
    codes_list = [int(code) for line in f for code in line.strip().split(',')]

class IntcodeComputer():
    """Process codes into code blocks and carry out operations."""
    
    def __init__(self, codes):
        self.codes = codes
        self.outputs = []

    def get_code_block(self, pos, opcode):
        """Get code block based on position in codes, sized based on opcode."""
        if opcode == 99:
            print('99 IS THE END')
            block_size = 0
            return [self.codes[pos]]
        elif opcode in (1, 2, 7, 8):
            block_size = 4
        elif opcode in (5, 6):
            block_size = 3
        elif opcode in (3, 4):
            block_size = 2
        else:
            print('OPCODE')
            print(opcode)
        code_block = self.codes[pos:pos+block_size]
        print(f'Pos: {str(pos)} \n{str(pos+block_size)}')
        print('Get a Code Block: ')
        print(code_block)
        return code_block

    def get_opcode(self, code):
        """Get the opcode string from a codeblock."""
        opcode = int(str(code)[-2:])
        return opcode

    def get_modes(self, code_block):
        """Get the two modes for a code block's parameters."""
        # FUCK YOU INDEX ERRORS, LIST COMPS, AND EVEN YOU LAMBDAS I DON'T NEED PRETTY
        # 0 = pos mode
        # 1 = imm mode
        modes, mode_codes = [0, 0], list(reversed(str(code_block[0])))[2:]
        x = 0
        for mode in mode_codes:
            modes[x] = int(mode)
            x += 1
        print('Get modes: ')
        print(modes)
        return modes

    def get_values(self, code_block):
        """
        Get the value for each code based on if it's position mode (pos_mode) or 
        immediate mode (imm_mode) and its position in the code block.
        """
        pos_mode, imm_mode = 0, 1
        x, values = 1, []
        modes = self.get_modes(code_block)
        for mode in modes:
            if mode == pos_mode:
                values.append(int(self.codes[code_block[x]]))
            elif mode == imm_mode:
                values.append(int(code_block[x]))
            else: print('Error: Not a valid mode.')
            x += 1
        print('Get values: ')
        print(values)
        return values 

    def do_operation_get_pos(self, pos, code_block, opcode_input=5):
        opcode = self.get_opcode(code_block[0])
        modes = self.get_modes(code_block)
        if opcode == 99:
            print('We have reached THE END.')
            return # ends the program.
        elif opcode == 1: # adds value 1 and 2, then puts it in pos 3.
            values = self.get_values(code_block)
            self.codes[code_block[3]] = values[0] + values[1]
            print('The values being added together, then the result of adding them in pos 3: ')
            print(values)
            print(self.codes[code_block[3]])
            return pos + 4
        elif opcode == 2: # multiplies value 1 and 2, then puts it in pos 3.
            values = self.get_values(code_block)
            self.codes[code_block[3]] = values[0] * values[1]
            print('The values being multiplied together, then the result of multiplying them in pos 3: ')
            print(values)
            print(self.codes[code_block[3]])
            return pos + 4
        elif opcode == 3: # places an input into pos 1.
            self.codes[code_block[1]] = opcode_input
            #assert("This should be " + str(opcode_input) + ': ' + str(self.codes[code_block[1]]))
            return pos + 2
        elif opcode == 4: # outputs the number at pos 1 or imm 1 to an outputs list.
            if modes[0] == 0:
                output = self.codes[code_block[1]]
            else:
                output = code_block[1]
            self.outputs.append(output)
            # If the output != 0, the program ends and returns the output.
            if output != 0:
                finish_msg = f'THE FINAL OUTPUT IS: {str(output)}. \nTotal outputs: '
                print(self.outputs)
                return finish_msg
            return pos + 2

        # jump-if-true. If param 1 != 0, jump to the pos of param2 else pass.
        elif opcode == 5:
            # assert pos not in len(self.codes), "testing assert and opcode 5"
            print('\nthe position after checking if it\'s opcode 5')
            print(pos)
            values = self.get_values(code_block)
            if values[0] != 0:
                pos = values[1]
                return pos
            else:
                return pos + 3
        # jump-if-false. If param1 == 0, jump to pos of param2 else pass.
        elif opcode == 6:
            values = self.get_values(code_block)
            if values[0] == 0:
                pos = values[1]
                return pos
            else:
                return pos + 3
        # less than. if param1 < param2, store 1 in pos of param3 else store 0
        elif opcode == 7:
            values = self.get_values(code_block)
            if values[0] < values[1]:
                self.codes[code_block[3]] = 1
            else:
                self.codes[code_block[3]] = 0
            return pos + 4
        # equals. If param1 == param2, store 1 in pos of param3 else store 0.
        elif opcode == 8:
            values = self.get_values(code_block)
            if values[0] == values[1]:
                self.codes[code_block[3]] = 1
            else:
                self.codes[code_block[3]] = 0
            return pos + 4
        else: #If an opcode is invalid, the program went wrong.
            print('The opcode is wrong.')



puzzle_input = IntcodeComputer(codes_list)
pos = 0
opcode = puzzle_input.get_opcode(puzzle_input.codes[0])

print('codes list length')
print(len(codes_list))
print(puzzle_input.codes[6])

while True:
    # Get code block starting at pos.
    code_block = puzzle_input.get_code_block(pos, opcode)
    
    # Perform operations on this code block and return next pos.
    pos = puzzle_input.do_operation_get_pos(pos, code_block)
    if type(pos) != int:
        print(code_block)
        print(pos)
        break

    # Get the opcode for the next code block from the number at new pos.
    opcode = puzzle_input.get_opcode(puzzle_input.codes[pos])
    print(puzzle_input.outputs)

