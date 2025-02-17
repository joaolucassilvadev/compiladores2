class CodeWriter:
    def __init__(self, asm_file_obj):
        self.asm_file_obj = asm_file_obj  # Usa o arquivo já aberto
        self.label_counter = 0  # Inicializa o contador de rótulos

    def write(self, command):
        cmd_type, segment, value = command
        print(f"Gerando código para: {cmd_type} {segment} {value}")

        if cmd_type == 'push' and segment == 'constant':
            self.asm_file_obj.write(f"@{value} // push constant {value}\n")
            self.asm_file_obj.write("D=A\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("M=D\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("M=M+1\n")

        elif cmd_type == 'add':
            self.asm_file_obj.write("@SP // add\n")
            self.asm_file_obj.write("M=M-1\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write("A=A-1\n")
            self.asm_file_obj.write("M=D+M\n")

        elif cmd_type == 'eq':
            label = f"JEQ_Main_{self.label_counter}"
            self.asm_file_obj.write(f"@SP // eq\n")
            self.asm_file_obj.write("AM=M-1\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("AM=M-1\n")
            self.asm_file_obj.write("D=M-D\n")
            self.asm_file_obj.write(f"@{label}\n")
            self.asm_file_obj.write("D;JEQ\n")
            self.asm_file_obj.write("D=1\n")
            self.asm_file_obj.write(f"({label})\n")
            self.asm_file_obj.write("D=D-1\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("M=D\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("M=M+1\n")
            self.label_counter += 1

        elif cmd_type == 'lt':
            label = f"JLT_Main_{self.label_counter}"
            self.asm_file_obj.write(f"@SP // lt\n")
            self.asm_file_obj.write("AM=M-1\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("AM=M-1\n")
            self.asm_file_obj.write("D=M-D\n")
            self.asm_file_obj.write(f"@{label}_TRUE\n")
            self.asm_file_obj.write("D;JLT\n")
            self.asm_file_obj.write("D=0\n")
            self.asm_file_obj.write(f"@{label}_FALSE\n")
            self.asm_file_obj.write("0;JMP\n")
            self.asm_file_obj.write(f"({label}_TRUE)\n")
            self.asm_file_obj.write("D=-1\n")
            self.asm_file_obj.write(f"({label}_FALSE)\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("M=D\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("M=M+1\n")
            self.label_counter += 1

        elif cmd_type == 'gt':
            label = f"JGT_Main_{self.label_counter}"
            self.asm_file_obj.write(f"@SP // gt\n")
            self.asm_file_obj.write("AM=M-1\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("AM=M-1\n")
            self.asm_file_obj.write("D=M-D\n")
            self.asm_file_obj.write(f"@{label}_TRUE\n")
            self.asm_file_obj.write("D;JGT\n")
            self.asm_file_obj.write("D=0\n")
            self.asm_file_obj.write(f"@{label}_FALSE\n")
            self.asm_file_obj.write("0;JMP\n")
            self.asm_file_obj.write(f"({label}_TRUE)\n")
            self.asm_file_obj.write("D=-1\n")
            self.asm_file_obj.write(f"({label}_FALSE)\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("M=D\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("M=M+1\n")
            self.label_counter += 1

        elif cmd_type == 'sub':
            self.asm_file_obj.write("@SP // sub\n")
            self.asm_file_obj.write("M=M-1\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write("A=A-1\n")
            self.asm_file_obj.write("M=M-D\n")

        elif cmd_type == 'neg':
            self.asm_file_obj.write("@SP // neg\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("A=A-1\n")
            self.asm_file_obj.write("M=-M\n")

        elif cmd_type == 'and':
            self.asm_file_obj.write("@SP // and\n")
            self.asm_file_obj.write("AM=M-1\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write("A=A-1\n")
            self.asm_file_obj.write("M=D&M\n")

        elif cmd_type == 'or':
            self.asm_file_obj.write("@SP // or\n")
            self.asm_file_obj.write("AM=M-1\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write("A=A-1\n")
            self.asm_file_obj.write("M=D|M\n")

        elif cmd_type == 'not':
            self.asm_file_obj.write("@SP // not\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("A=A-1\n")
            self.asm_file_obj.write("M=!M\n")

        elif cmd_type == 'pop' and segment == 'local':
            self.asm_file_obj.write(f"@LCL // pop local {value}\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write(f"@{value}\n")
            self.asm_file_obj.write("D=D+A\n")
            self.asm_file_obj.write("@R13\n")
            self.asm_file_obj.write("M=D\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("M=M-1\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write("@R13\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("M=D\n")
        
        elif cmd_type == 'pop' and segment == 'argument':
            self.asm_file_obj.write(f"@ARG // pop argument {value}\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write(f"@{value}\n")
            self.asm_file_obj.write("D=D+A\n")
            self.asm_file_obj.write("@R13\n")
            self.asm_file_obj.write("M=D\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("M=M-1\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write("@R13\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("M=D\n")
        
        elif cmd_type == 'pop' and segment == 'this':
            self.asm_file_obj.write(f"@THIS // pop this {value}\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write(f"@{value}\n")
            self.asm_file_obj.write("D=D+A\n")
            self.asm_file_obj.write("@R13\n")
            self.asm_file_obj.write("M=D\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("M=M-1\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write("@R13\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("M=D\n")
        
        elif cmd_type == 'pop' and segment == 'that':
            self.asm_file_obj.write(f"@THAT // pop that {value}\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write(f"@{value}\n")
            self.asm_file_obj.write("D=D+A\n")
            self.asm_file_obj.write("@R13\n")
            self.asm_file_obj.write("M=D\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("M=M-1\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write("@R13\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("M=D\n")
    
        elif cmd_type == 'pop' and segment == 'temp':
            self.asm_file_obj.write(f"@SP // pop temp {value}\n")
            self.asm_file_obj.write("M=M-1\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write(f"@R{5 + int(value)}\n")
            self.asm_file_obj.write("M=D\n")
        
        elif cmd_type == 'push' and segment == 'local':
            self.asm_file_obj.write(f"@LCL // push local {value}\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write(f"@{value}\n")
            self.asm_file_obj.write("A=D+A\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("M=D\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("M=M+1\n")
        
        elif cmd_type == 'push' and segment == 'that':
            self.asm_file_obj.write(f"@THAT // push that {value}\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write(f"@{value}\n")
            self.asm_file_obj.write("A=D+A\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("M=D\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("M=M+1\n")
        
        elif cmd_type == 'push' and segment == 'argument':
            self.asm_file_obj.write(f"@ARG // push argument {value}\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write(f"@{value}\n")
            self.asm_file_obj.write("A=D+A\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("M=D\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("M=M+1\n")
        
        elif cmd_type == 'push' and segment == 'this':
            self.asm_file_obj.write(f"@THIS // push this {value}\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write(f"@{value}\n")
            self.asm_file_obj.write("A=D+A\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("M=D\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("M=M+1\n")

        elif cmd_type == 'push' and segment == 'temp':
            self.asm_file_obj.write(f"@R{5 + int(value)} // push temp {value}\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("M=D\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("M=M+1\n")
        
        elif cmd_type == 'pop' and segment == 'pointer':
            self.asm_file_obj.write(f"@SP // pop pointer {value}\n")
            self.asm_file_obj.write("M=M-1\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write(f"@R{3 + int(value)}\n")
            self.asm_file_obj.write("M=D\n")

        elif cmd_type == 'push' and segment == 'pointer':
            self.asm_file_obj.write(f"@R{3 + int(value)} // push pointer {value}\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("M=D\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("M=M+1\n")
        
        elif cmd_type == 'pop' and segment == 'static':
            self.asm_file_obj.write(f"@SP // pop static {value}\n")
            self.asm_file_obj.write("M=M-1\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write(f"@Main.{value}\n")
            self.asm_file_obj.write("M=D\n")

        elif cmd_type == 'push' and segment == 'static':
            self.asm_file_obj.write(f"@Main.{value} // push static {value}\n")
            self.asm_file_obj.write("D=M\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("A=M\n")
            self.asm_file_obj.write("M=D\n")
            self.asm_file_obj.write("@SP\n")
            self.asm_file_obj.write("M=M+1\n")