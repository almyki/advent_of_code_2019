
filename = 'AdventOfCode_2019_5.txt'

with open(filename) as f:
    codes = [int(code) for line in f for code in line.strip().split(',')]

code_block = codes

class IntcodeComputer():
    """Process codes into code blocks and carry out operations."""
    
    def __init__(self, codes):
        self.codes = codes
        self.code_blocks = self.get_code_blocks()

    def get_code_blocks(self):
        """Get the code block, sized based on opcode."""
        x, pass_block, code_blocks = 0, 0, []

        for code in self.codes:
            opcode = self.get_opcode(code)
            if pass_block > 0: 
                pass_block -= 1
            elif opcode == 1 or opcode == 2:
                code_blocks.append(self.codes[x:x+4])
                print(self.codes[x:x+4])
                pass_block = 3
            elif opcode == 3 or opcode == 4:
                code_blocks.append(self.codes[x:x+2])
                print(self.codes[x:x+2])
                pass_block = 1
            x += 1
        print('Get Code Blocks: ')
        print(code_blocks)
        return code_blocks

    def get_opcode(self, code):
        """Get the opcode string from a codeblock."""
        opcode = int(str(code)[-2:])
        return opcode

    def get_modes(self, code_block):
        """Get the two modes for a code block's parameters."""
        # FUCK YOU INDEX ERRORS, LIST COMPS, AND EVEN YOU LAMBDAS I DON'T NEED PRETTY
        modes, mode_codes = [0, 0], list(reversed(str(code_block[0])))[2:]
        x = 0
        for mode in mode_codes:
            modes[x] = int(mode)
            x += 1
        #print('Get modes: ')
        #print(modes)
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
        #print('Get values: ')
        #print(values)
        return values 

    def get_codes_outputs(self, opcode_3_input=1):
        """Carry out the operations for the code."""
        #print('\nStart Getting Codes Outputs for: ')
        #print(self.codes)
        outputs = []
        for code_block in self.code_blocks:
            opcode = self.get_opcode(code_block[0])
            #print(f'Get opcode: {str(opcode)}')
            pos = code_block[-1]
            # Opcode 99 ends the program.
            if opcode == 99: break
            # Opcode 1 adds value 1 and 2, then puts it in pos 3.
            elif opcode == 1:
                values = self.get_values(code_block)
                self.codes[pos] = values[0] + values[1]
            # Opcode 2 multiplies value 1 and 2, then puts it in pos 3.
            elif opcode == 2:
                values = self.get_values(code_block)
                self.codes[pos] = values[0] * values[1]
            # Opcode 3 places an input into pos 3.
            elif opcode == 3:
                self.codes[pos] = opcode_3_input
            # Opcode 4 outputs the number at pos 3 to an outputs list.
            elif opcode == 4:
                outputs.append(self.codes[pos])
                if self.codes[pos] != 0:
                    return outputs
            # If an opcode is invalid, the program went wrong.
            else:
                print('The opcode is wrong.')

puzzle_input = IntcodeComputer(code_block)
outputs = puzzle_input.get_codes_outputs()

print('\nOutputs: ')
print(outputs)

