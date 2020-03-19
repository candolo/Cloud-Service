class Message:
    def __init__(self, data):
        splitted_data = data.split()
        self.command = splitted_data[0]
        splitted_data.pop(0)
        self.arguments = splitted_data

    def setCommand(self, command):
        self.command = command

    def setArguments(self, arguments):
        self.arguments = arguments

    def getCommand(self):
        return self.command

    def getArguments(self):
        return self.arguments

    def toArray(self):
        message_to_array = [self.command]
        for i in range(len(self.arguments)):
            message_to_array.append(self.arguments[i])
        return message_to_array

    def toString(self):
        message_to_string = self.command
        for i in range(len(self.arguments)):
            message_to_string += " " + self.arguments[i]
        message_to_string += "\n"
        return message_to_string

    def printMessage(self):
        message_to_print = "Command: " + self.command + "\nArguments:"
        for i in range(len(self.arguments)):
            message_to_print += "\n" + str(i+1) + ": " + self.arguments[i]
        print(message_to_print)