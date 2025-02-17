import sys
from Parser import Parser
from CodeWriter import CodeWriter

class VMTranslator:
    def __init__(self, vm_file, asm_file):
        self.vm_file = vm_file
        self.asm_file = asm_file
        self.parser = Parser(vm_file)

        self.asm_file_obj = open(self.asm_file, 'w')
        self.code_writer = CodeWriter(self.asm_file_obj)

    def translate(self):
        while self.parser.has_more_commands():
            command = self.parser.advance()
            if command:
                self.code_writer.write(command)

        self.asm_file_obj.close()

def main():
    vm_file = sys.argv[1]
    asm_file = vm_file.replace('.vm', '.asm')

    translator = VMTranslator(vm_file, asm_file)
    translator.translate()

if __name__ == "__main__":
    main()