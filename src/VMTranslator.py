import sys
from Parser import Parser
from CodeWriter import CodeWriter

class VMTranslator:
    def __init__(self, input_file):
        self.input_file = input_file
        self.output_file = input_file.replace(".vm", ".asm")

    def translate(self):
        parser = Parser(self.input_file)
        with open(self.output_file, "w") as output:
            code_writer = CodeWriter(output)
            
            while parser.has_more_commands():
                command, arg1, arg2 = parser.advance()
                code_writer.write(command, arg1, arg2)

if __name__ == "__main__":
    input_file = sys.argv[1]
    translator = VMTranslator(input_file)
    translator.translate()
