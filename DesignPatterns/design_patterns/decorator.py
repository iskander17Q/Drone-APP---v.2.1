def make_bold(fn):
    def wrapper(*args, **kwargs):
        return '<b>' + fn(*args, **kwargs) + '</b>'
    return wrapper


@make_bold
def greet(name):
    return f'Hello, {name}'


def main():
    print(greet('World'))


if __name__ == '__main__':
    main()
