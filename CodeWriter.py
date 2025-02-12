class CodeWriter:
    def __init__(self, output_file):
        """Abre o arquivo de saída para escrita"""
        self.file = open(output_file, "w")
        self.label_counter = 0  # Para rótulos únicos

    def writeArithmetic(self, command):
        """Escreve o código Assembly para operações aritméticas e lógicas"""
        if command in ["add", "sub", "and", "or"]:
            op = {"add": "+", "sub": "-", "and": "&", "or": "|"}[command]
            self.file.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=M" + op + "D\n")
        elif command in ["neg", "not"]:
            op = {"neg": "-", "not": "!"}[command]
            self.file.write("@SP\nA=M-1\nM=" + op + "M\n")
        elif command in ["eq", "gt", "lt"]:
            jump = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}[command]
            label_true = f"LABEL_TRUE_{self.label_counter}"
            label_end = f"LABEL_END_{self.label_counter}"
            self.label_counter += 1
            self.file.write(
                "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n"
                f"@{label_true}\nD;{jump}\n"
                "@SP\nA=M-1\nM=0\n"
                f"@{label_end}\n0;JMP\n"
                f"({label_true})\n"
                "@SP\nA=M-1\nM=-1\n"
                f"({label_end})\n"
            )

    def writePushPop(self, command, segment, index):
        """Escreve o código Assembly para push e pop"""
        if command == "C_PUSH":
            if segment == "constant":
                self.file.write(f"@{index}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment in ["local", "argument", "this", "that"]:
                segment_map = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}
                self.file.write(
                    f"@{index}\nD=A\n@{segment_map[segment]}\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
                )
            elif segment == "static":
                self.file.write(f"@Foo.{index}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment == "temp":
                self.file.write(f"@{5 + index}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment == "pointer":
                pointer_map = {0: "THIS", 1: "THAT"}
                self.file.write(f"@{pointer_map[index]}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

        elif command == "C_POP":
            if segment in ["local", "argument", "this", "that"]:
                segment_map = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}
                self.file.write(
                    f"@{index}\nD=A\n@{segment_map[segment]}\nD=M+D\n@R13\nM=D\n"
                    "@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n"
                )
            elif segment == "static":
                self.file.write(f"@SP\nAM=M-1\nD=M\n@Foo.{index}\nM=D\n")
            elif segment == "temp":
                self.file.write(f"@SP\nAM=M-1\nD=M\n@{5 + index}\nM=D\n")
            elif segment == "pointer":
                pointer_map = {0: "THIS", 1: "THAT"}
                self.file.write(f"@SP\nAM=M-1\nD=M\n@{pointer_map[index]}\nM=D\n")

    def close(self):
        """Fecha o arquivo"""
        self.file.close()
