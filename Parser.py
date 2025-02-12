class Parser:
    def __init__(self, filename):
        """Abre o arquivo e lê todas as linhas, removendo comentários e espaços extras"""
        with open(filename, "r") as file:
            self.lines = [line.split("//")[0].strip() for line in file.readlines()]
        self.lines = [line for line in self.lines if line]  # Remove linhas vazias
        self.current_command = None
        self.index = -1

    def hasMoreCommands(self):
        """Retorna True se ainda houver comandos a serem processados"""
        return self.index < len(self.lines) - 1

    def advance(self):
        """Lê o próximo comando"""
        self.index += 1
        self.current_command = self.lines[self.index]

    def commandType(self):
        """Retorna o tipo do comando"""
        if self.current_command.startswith("push"):
            return "C_PUSH"
        elif self.current_command.startswith("pop"):
            return "C_POP"
        elif self.current_command in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
            return "C_ARITHMETIC"
        else:
            return "C_UNKNOWN"

    def arg1(self):
        """Retorna o primeiro argumento do comando"""
        if self.commandType() == "C_ARITHMETIC":
            return self.current_command
        return self.current_command.split()[1]

    def arg2(self):
        """Retorna o segundo argumento do comando (somente para push/pop)"""
        return int(self.current_command.split()[2]) if self.commandType() in ["C_PUSH", "C_POP"] else None
