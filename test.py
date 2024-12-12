import numpy as np

# 仅测试用代码
def print_squares(squares):
    print(*squares)

a = np.zeros(shape=(3, 5))
a = np.rot90(a)

print(a)
