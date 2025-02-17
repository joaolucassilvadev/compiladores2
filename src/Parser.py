class Parser:
    def __init__(self, vm_file):
        self.vm_file = vm_file
        self.commands = []
        self.current_command = 0

        with open(vm_file, 'r') as file:
            lines = file.readlines()
            self.commands = [line.strip() for line in lines if line.strip() and not line.startswith('//')]
        
        print(f"Comandos lidos do arquivo: {self.commands}")

    def has_more_commands(self):
        return self.current_command < len(self.commands)

    def advance(self):
        command = self.commands[self.current_command]
        self.current_command += 1
        
        parts = command.split()

        if len(parts) == 1:
            return parts[0], None, None
        elif len(parts) == 2:
            return parts[0], None, parts[1]
        elif len(parts) == 3:
            return parts[0], parts[1], parts[2]
        
        return None