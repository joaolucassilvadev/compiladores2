class CodeWriter:
    def __init__(self, output_file):
        self.output_file = output_file
        self.label_counter = 0

    def write(self, command, arg1, arg2):
        asm_code = ""

        if command == "push":
            asm_code = self.write_push(arg1, arg2)
        elif command == "pop":
            asm_code = self.write_pop(arg1, arg2)
        elif command == "add":
            asm_code = self.write_add()
        elif command == "sub":
            asm_code = self.write_sub()
        elif command == "and":
            asm_code = self.write_and()
        elif command == "or":
            asm_code = self.write_or()
        elif command == "neg":
            asm_code = self.write_neg()
        elif command == "not":
            asm_code = self.write_not()
        elif command == "eq":
            asm_code = self.write_eq()
        elif command == "lt":
            asm_code = self.write_lt()
        elif command == "gt":
            asm_code = self.write_gt()
        elif command == "label":
            asm_code = f"({arg1})\n"
        elif command == "if-goto":
            asm_code = f"@SP\nAM=M-1\nD=M\n@{arg1}\nD;JGT\n"
        elif command == "goto":
            asm_code = f"@{arg1}\n0;JMP\n"
        elif command == "function":
            asm_code = self.write_function(arg1, int(arg2))
        elif command == "return":
            asm_code = self.write_return()

        self.output_file.write(asm_code)

    def write_push(self, segment, value):
        if segment == "constant":
            return f"@{value}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif segment == "local":
            return f"@LCL\nD=M\n@{value}\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif segment == "argument":
            return f"@ARG\nD=M\n@{value}\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif segment == "this":
            return f"@THIS\nD=M\n@{value}\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif segment == "that":
            return f"@THAT\nD=M\n@{value}\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif segment == "temp":
            return f"@{5+int(value)}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif segment == "pointer":
            address = "R3" if int(value) == 0 else "R4"
            return f"@{address}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif segment == "static":
            return f"@Main.{value}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        return ""

    def write_pop(self, segment, value):
        if segment == "local":
            return f"@LCL\nD=M\n@{value}\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n"
        elif segment == "argument":
            return f"@ARG\nD=M\n@{value}\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n"
        elif segment == "this":
            return f"@THIS\nD=M\n@{value}\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n"
        elif segment == "that":
            return f"@THAT\nD=M\n@{value}\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n"
        elif segment == "temp":
            return f"@{5+int(value)}\nD=A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n"
        elif segment == "pointer":
            address = "R3" if int(value) == 0 else "R4"
            return f"@SP\nAM=M-1\nD=M\n@{address}\nM=D\n"
        elif segment == "static":
            return f"@SP\nAM=M-1\nD=M\n@Main.{value}\nM=D\n"
        return ""

    def write_add(self):
        return "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D+M\n"

    def write_sub(self):
        return "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M-D\n"

    def write_and(self):
        return "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D&M\n"

    def write_or(self):
        return "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D|M\n"

    def write_neg(self):
        return "@SP\nA=M-1\nM=-M\n"

    def write_not(self):
        return "@SP\nA=M-1\nM=!M\n"

    def write_eq(self):
        self.label_counter += 1
        return f"""@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@EQ_TRUE_{self.label_counter}
D;JEQ
D=0
@EQ_END_{self.label_counter}
0;JMP
(EQ_TRUE_{self.label_counter})
D=-1
(EQ_END_{self.label_counter})
@SP
A=M
M=D
@SP
M=M+1
"""

    def write_lt(self):
        self.label_counter += 1
        return f"""@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@LT_TRUE_{self.label_counter}
D;JLT
D=0
@LT_END_{self.label_counter}
0;JMP
(LT_TRUE_{self.label_counter})
D=-1
(LT_END_{self.label_counter})
@SP
A=M
M=D
@SP
M=M+1
"""

    def write_gt(self):
        self.label_counter += 1
        return f"""@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@GT_TRUE_{self.label_counter}
D;JGT
D=0
@GT_END_{self.label_counter}
0;JMP
(GT_TRUE_{self.label_counter})
D=-1
(GT_END_{self.label_counter})
@SP
A=M
M=D
@SP
M=M+1
"""
    
    def write_function(self, function_name, num_locals):
        asm_code = f"({function_name})\n"
        for _ in range(num_locals):
            asm_code += "@0\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        return asm_code

    def write_return(self):
        return ("@LCL\nD=M\n@R13\nM=D\n"
                "@5\nA=D-A\nD=M\n@R14\nM=D\n"
                "@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n"
                "@ARG\nD=M+1\n@SP\nM=D\n"
                "@R13\nAM=M-1\nD=M\n@THAT\nM=D\n"
                "@R13\nAM=M-1\nD=M\n@THIS\nM=D\n"
                "@R13\nAM=M-1\nD=M\n@ARG\nM=D\n"
                "@R13\nAM=M-1\nD=M\n@LCL\nM=D\n"
                "@R14\nA=M\n0;JMP\n")
