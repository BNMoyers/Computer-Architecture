"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4 #set the last reg to the sp
        self.pc = 0
        self.sp = 7

    # op codes and handler
        self.handler = {
            0b00000001: self.handle_HLT,
            0b10000010: self.handle_LDI,
            0b10100010: self.handle_MUL,
            0b01000110: self.handle_POP,
            0b01000111: self.handle_PRN,
            0b01000101: self.handle_PUSH
        }

    def load(self, file):
        """Load a program into memory."""

        address = 0

        with open(file) as f:
            lines = f.readlines()
            lines = [
                line for line in lines if line.startswith('0') or line.startswith('1')
            ]
            program = [int(line[:8], 2) for line in lines]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    # def alu(self, op, reg_a, reg_b):
    #     """ALU operations."""

    #     if op == "ADD":
    #         self.reg[reg_a] += self.reg[reg_b]
    #     # elif op == "SUB": etc
    #     else:
    #         raise Exception("Unsupported ALU operation")

    def cu(self, op, reg_a, reg_b):
        """CU operations."""
        try:
            self.handler[op](reg_a, reg_b)
        except KeyError:
            raise Exception("No such op code")

    def handle_HLT(self, reg_a, reg_b):
        self.pc += 1
        self.running = False

    def handle_LDI(self, reg_a, reg_b):
        self.reg[reg_a] = reg_b
        self.pc += 3
    
    def handle_MUL(self, reg_a, reg_b):
        self.reg[reg_a] = (self.reg[reg_a] * self.reg[reg_b])
        self.pc += 3

    def handle_POP(self, reg_a, reg_b):
        self.reg[reg_a] = self.ram[self.sp]
        self.sp +=1
        self.pc += 2

    def handle_PRN(self, reg_a, reg_b):
        print(self.reg[reg_a])
        self.pc += 2
    
    def handle_PUSH(self, reg_a, reg_b):
        self.sp -= 1
        self.ram[self.sp] = self.reg[reg_a]
        self.pc += 2

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        # set exit condition
        self.running = True

        # while loop
        while self.running:

            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            self.cu(IR, operand_a, operand_b)

