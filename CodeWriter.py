class CodeWriter:
    def __init__(self, output_file):
        """Abre o arquivo de saída para escrita"""
        self.file = open(output_file, "w")
        self.label_counter = 0  # Para rótulos únicos
        self.function_name = ""

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

    def writeLabel(self, label):
        """Escreve um rótulo"""
        self.file.write(f"({self.function_name}${label})\n")

    def writeGoto(self, label):
        """Escreve um salto incondicional"""
        self.file.write(f"@{self.function_name}${label}\n0;JMP\n")

    def writeIf(self, label):
        """Escreve um salto condicional"""
        self.file.write("@SP\nAM=M-1\nD=M\n")
        self.file.write(f"@{self.function_name}${label}\nD;JNE\n")

    def writeFunction(self, function_name, num_locals):
        """Escreve a definição de uma função"""
        self.function_name = function_name
        self.file.write(f"({function_name})\n")
        for _ in range(num_locals):
            self.file.write("@SP\nA=M\nM=0\n@SP\nM=M+1\n")

    def writeCall(self, function_name, num_args):
        """Escreve a chamada de uma função"""
        return_label = f"{function_name}$ret.{self.label_counter}"
        self.label_counter += 1
        self.file.write(f"@{return_label}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.file.write(f"@{function_name}\n0;JMP\n({return_label})\n")

    def writeReturn(self):
        """Escreve o retorno de uma função"""
        self.file.write("@LCL\nD=M\n@endFrame\nM=D\n")
        self.file.write("@5\nD=A\n@endFrame\nA=M-D\nD=M\n@retAddr\nM=D\n")
        self.file.write("@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n")
        self.file.write("@ARG\nD=M+1\n@SP\nM=D\n")
        self.file.write("@retAddr\nA=M\n0;JMP\n")

    def close(self):
        """Fecha o arquivo"""
        self.file.close()
