class OldLogger:
    def write(self, message):
        print('OLD LOG:', message)


class LoggerAdapter:
    def __init__(self, old_logger):
        self.old = old_logger

    def log(self, msg):
        self.old.write(msg)


def main():
    old = OldLogger()
    adapted = LoggerAdapter(old)
    adapted.log('Adapter pattern in action')


if __name__ == '__main__':
    main()
