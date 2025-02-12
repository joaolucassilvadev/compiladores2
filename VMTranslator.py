import sys
from Parser import Parser
from CodeWriter import CodeWriter

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 VMTranslator.py [arquivo.vm]")
        return

    input_path = sys.argv[1]
    output_path = input_path.replace(".vm", ".asm")

    parser = Parser(input_path)
    code_writer = CodeWriter(output_path)

    while parser.hasMoreCommands():
        parser.advance()
        command_type = parser.commandType()

        if command_type == "C_ARITHMETIC":
            code_writer.writeArithmetic(parser.arg1())
        elif command_type in ["C_PUSH", "C_POP"]:
            code_writer.writePushPop(command_type, parser.arg1(), parser.arg2())

    code_writer.close()

if __name__ == "__main__":
    main()
