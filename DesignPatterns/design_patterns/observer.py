class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, obs):
        self._observers.append(obs)

    def notify(self, msg):
        for o in self._observers:
            o.update(msg)


class PrintObserver:
    def update(self, msg):
        print('Observer got:', msg)


def main():
    s = Subject()
    s.attach(PrintObserver())
    s.notify('Event happened')


if __name__ == '__main__':
    main()
