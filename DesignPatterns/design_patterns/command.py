class Light:
    def __init__(self):
        self.on = False

    def switch_on(self):
        self.on = True
        print('Light: ON')

    def switch_off(self):
        self.on = False
        print('Light: OFF')


class Command:
    def execute(self):
        raise NotImplementedError


class SwitchOnCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.switch_on()


class SwitchOffCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.switch_off()


class Switch:
    def __init__(self):
        self._commands = []

    def store_and_execute(self, cmd):
        self._commands.append(cmd)
        cmd.execute()


def main():
    light = Light()
    switch = Switch()
    switch.store_and_execute(SwitchOnCommand(light))
    switch.store_and_execute(SwitchOffCommand(light))


if __name__ == '__main__':
    main()
