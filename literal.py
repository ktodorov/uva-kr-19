class Literal:
    def __init__(self, number):
        int_number = int(number)
        self.negative = (int_number < 0)
        self.number = abs(int_number)

    def print(self):
        if self.negative:
            print("-", end='')
            
        print(str(self.number), end = '')