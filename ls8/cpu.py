"""CPU functionality."""
import sys
class CPU:
   """Main CPU class."""
   def __init__(self):
       """Construct a new CPU."""
       self.register = [0] * 8
       self.ram = [0] * 256
       self.pc = 0
       self.running = False
       self.HLT = 0b00000001
       self.LDI = 0b10000010
       self.PRN = 0b01000111
       self.MUL = 0b10100010
       self.PUSH = 0b01000101
       self.POP = 0b01000110
       self.SPL = 7  # Stack Pointer location in the register
       self.branchtable = {}
       self.branchtable[self.HLT] = self.handle_hlt
       self.branchtable[self.LDI] = self.handle_ldi
       self.branchtable[self.PRN] = self.handle_prn
       self.branchtable[self.MUL] = self.handle_mul
       self.branchtable[self.PUSH] = self.handle_push
       self.branchtable[self.POP] = self.handle_pop
   def load(self):
       """Load a program into memory."""
       if len(sys.argv) != 2:
           print("usage: file.py <filename>", file=sys.stderr)
       try:
           with open(sys.argv[1]) as ff:
               lines = ff.readlines()
               program = []
               for line in lines:
                   if line[0] in "01":
                       new_line = int(line[:8], 2)
                       program.append(new_line)
           address = 0
           for instruction in program:
               self.ram[address] = instruction
               address += 1
       except FileNotFoundError:
           print(f"{sys.argv[0]}: {sys.argv[1]} not found")
           sys.exit(2)
   def alu(self, op, reg_a, reg_b):
       """ALU operations."""
       if op == "ADD":
           self.register[reg_a] += self.register[reg_b]
       #elif op == "SUB": etc
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
           print(" %02X" % self.register[i], end='')
       print()
   def run(self):
       """Run the CPU."""
       self.running = True
       while self.running:
           ir = self.ram_read(self.pc)
           self.branchtable[ir]()
   def ram_read(self, address):
       return self.ram[address]
   def ram_write(self, value, address):
       self.ram[address] = value
   def handle_hlt(self):
       self.running = False
   def handle_ldi(self):
       operand_a = self.ram_read(self.pc + 1)
       operand_b = self.ram_read(self.pc + 2)
       self.register[operand_a] = operand_b
       self.pc += 3
   def handle_prn(self):
       operand_a = self.ram_read(self.pc + 1)
       print(self.register[operand_a])
       self.pc += 2
   def handle_mul(self):
       operand_a = self.ram_read(self.pc + 1)
       operand_b = self.ram_read(self.pc + 2)
       self.register[operand_a] *= self.register[operand_b]
       self.pc += 3
   def handle_push(self):
       self.register[self.SPL] -= 1  # Decrement stack position by 1
       reg = self.ram_read(self.pc + 1)  # Get value from register
       val = self.register[reg]  # Get value from register
       self.ram_write(val, self.register[self.SPL])
       self.pc += 2
   def handle_pop(self):
       val = self.ram_read(self.register[self.SPL])  # Get value from SP
       reg = self.ram_read(self.pc + 1)  # Get register
       self.register[reg] = val  # Copy value to register
       self.register[self.SPL] += 1  # Modify SP
       self.pc += 2