"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
CMP = 0b10100111
JMP = 0b01010100
JNE = 0b01010110
JEQ = 0b01010101

SP = 7
#ltf = less than flag, gtf = greater than flag, etf = equals to flag
#flags are if a paticular bit is set
ltf = 0b100
gtf = 0b010
etf = 0b001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
         
        self.pc = 0 #Program Counter
        self.reg = [0] * 8 #8 general purpose registers
        self.ram = [0] * 256 #Hold 256 bytes of memory
        self.flags = 0b001 #set to equal true
         

    def load(self, progname):
        """Load a program into memory."""

        #progname = sys.argv[1]

        # with open(progname) as f:
        #     for line in f:
        #         line = line.split("#")[0]
        #         line = line.strip()
        #           
        #         if line == '':
        #           continue
        #        
        #         val = int(line, 2)
        #         #print(val)
        #         memory[address] = val
        #         addresss += 1

        # sys.exit(0)

        address = 0
        progname = sys.argv[1]
        with open(progname) as f:
            for line in f:
                line = line.split("#")[0]
                line = line.strip()

                if line == "":
                    continue

                val = int(line, 2)
                self.ram[address] = val
                address +=1




    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == CMP:
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flags = ltf
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flags = gtf
            else:
                self.flags = etf                
        else:
            raise Exception("Unsupported ALU operation")
        

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            #instruction = memory[pc]
            opcode = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            #Save_Reg
            if opcode == LDI:
                #Value = memory[pc+1]
                #reg_num = memory[pc+2]
                self.reg[operand_a] = operand_b
                #3 Byte instruction
                self.pc +=3
            elif opcode == PRN:
                #reg_num = memory[pc + 1]
                #print (register[reg_num])
                print(self.reg[operand_a])
                #2 byte instruction 
                self.pc +=2
            elif opcode == MUL:
                self.alu(opcode, operand_a, operand_b)
                self.pc +=3
            elif opcode == PUSH:
                self.reg[SP] -= 1
                reg = self.ram[self.pc + 1]
                val = self.reg[reg]
                self.ram[self.reg[SP]] = val
                self.pc += 2
            elif opcode == POP:
                val = self.ram[self.reg[SP]]
                reg = self.ram[self.pc + 1]
                self.reg[reg] = val
                self.reg[SP] += 1
                self.pc += 2
            elif opcode == CMP:
                self.alu(opcode, operand_a, operand_b)
                self.pc +=3
            elif opcode == JMP:
                #Jumps to the register
                self.pc = self.reg[operand_a]
            elif opcode == JEQ:
                #if equal flag is true, jump to the address stored in the given register
                if self.flags & etf:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif opcode == JNE:
                #if equal flag is false, jump to the address stored in the given register
                if not self.flags & etf:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif opcode == HLT:
                #BEEj, only exits if there is an error?
                sys.exit(1)

        
