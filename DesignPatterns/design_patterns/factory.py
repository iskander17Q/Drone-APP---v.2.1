class Animal:
    def speak(self):
        raise NotImplementedError


class Dog(Animal):
    def speak(self):
        return 'woof'


class Cat(Animal):
    def speak(self):
        return 'meow'


class AnimalFactory:
    @staticmethod
    def create(animal_type):
        if animal_type == 'dog':
            return Dog()
        if animal_type == 'cat':
            return Cat()
        raise ValueError('Unknown animal')


def main():
    for t in ['dog', 'cat']:
        a = AnimalFactory.create(t)
        print(t, '->', a.speak())


if __name__ == '__main__':
    main()
