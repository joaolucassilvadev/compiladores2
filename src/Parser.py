class Parser:
    def __init__(self, file_path):
        with open(file_path, "r") as file:
            self.commands = [
                line.split("//")[0].strip() for line in file.readlines()
                if line.strip() and not line.startswith("//")
            ]
        self.current_index = -1

    def has_more_commands(self):
        return self.current_index + 1 < len(self.commands)

    def advance(self):
        self.current_index += 1
        parts = self.commands[self.current_index].split()
        command = parts[0]
        arg1 = parts[1] if len(parts) > 1 else None
        arg2 = parts[2] if len(parts) > 2 else None
        return command, arg1, arg2
