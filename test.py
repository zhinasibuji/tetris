# 仅测试用代码
def print_squares(squares):
    print([(square.x, square.y) for square in squares])

class Dog:
    def __init__(self, name):
        self.name = name

a = [Dog(1), Dog(2), Dog("int")]

breakpoint()
for dog in a:
    if type(dog.name) == int:
        a.remove(dog)


