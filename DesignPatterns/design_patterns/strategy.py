class Strategy:
    def sort(self, data):
        raise NotImplementedError


class BubbleSort(Strategy):
    def sort(self, data):
        # naive bubble for demo
        arr = list(data)
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr


class PythonSort(Strategy):
    def sort(self, data):
        return sorted(data)


class Sorter:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    def perform(self, data):
        return self.strategy.sort(data)


def main():
    data = [5,3,1,4,2]
    print('bubble ->', Sorter(BubbleSort()).perform(data))
    print('py sort ->', Sorter(PythonSort()).perform(data))


if __name__ == '__main__':
    main()
