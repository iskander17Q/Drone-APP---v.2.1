class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.value = kwargs.get('value', 0)
        return cls._instance


def main():
    a = Singleton(value=10)
    b = Singleton(value=20)
    print('a.value', a.value)
    print('b.value', b.value)
    print('a is b ->', a is b)


if __name__ == '__main__':
    main()
