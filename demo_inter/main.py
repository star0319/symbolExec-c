# 这是一个示例 Python 脚本。

# 按 ⌃R 执行或将其替换为您的代码。
# 按 双击 ⇧ 在所有地方搜索类、文件、工具窗口、操作和设置。

import numpy as np
import sys
from ctypes import c_int8

def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 ⌘F8 切换断点。


def test_int_8():

    # 创建一个具有特定形状的int8数组，初始化为0
    int8_array = np.zeros(shape=(1, 2), dtype=np.int8)

    print(int8_array)
    size = sys.getsizeof(int8_array)
    print("数据的大小为：", size, "字节")

    # int8_array[0][2]=254
    int8_array[0][1] = 127
    # int8_array[1][3] = 128
    print(int8_array)

    size = sys.getsizeof(int8_array)
    print("数据的大小为：", size, "字节")




    int8_array = np.zeros(shape=(1, 5), dtype=np.int8)

    print(int8_array)
    size = sys.getsizeof(int8_array)
    print("数据的大小为：", size, "字节")



    int8_array = np.zeros(shape=(3, 5), dtype=np.int8)


    print(int8_array)
    size = sys.getsizeof(int8_array)
    print("数据的大小为：", size, "字节")
    for i in range(0,3):
        for j in range(0,5):
            int8_array[i][j]=i*5+j

    print(int8_array)
    #11  01
    print(int8_array[0][3]|int8_array[0][1])
    print(int8_array[0][3] & int8_array[0][1])
    print(int8_array[0][3] ^ int8_array[0][1])
    print(int8_array[0][3]<<1)



    ##########################
    print("*****************1")


    data = [1000000 ,1000]
    size = sys.getsizeof(data)
    print("数据的大小为：", size, "字节")

    data = [1000000 ,1000000000, 100000]
    size = sys.getsizeof(data)
    print("数据的大小为：", size, "字节")

    data = [[1000000 ,1000000000, 100000]]
    size = sys.getsizeof(data)
    print("数据的大小为：", size, "字节")

    data = [[1000000 ,1000000000, 100000, 100000]]
    size = sys.getsizeof(data)
    print("数据的大小为：", size, "字节")

    data = [[1000000 ,1000000000, 100000, 100000],
            [100000 ,10000000, 10000000, 10000000],
            [100000 ,100000, 100000, 10000000]]
    size = sys.getsizeof(data)
    print("数据的大小为：", size, "字节")


    ##########################
    # print("*****************2")
    #
    # # 创建一个8位整数
    # int8_value = c_int8(0)
    # size = sys.getsizeof(int8_value)
    # print("数据的大小为：", size, "字节")
    # print(int8_value)  # 输出: c_byte(0)

def test_real_int_8():
    print("**************")
    data = [2 ,4, 10, 100]
    size = sys.getsizeof(data)
    print("数据的大小为：", size, "字节")
    dl=bytearray(data)
    size = sys.getsizeof(dl)
    print("数据的大小为：", size, "字节")
    print(dl)

    data = [2, 4, 10, 100,20,99]
    size = sys.getsizeof(data)
    print("数据的大小为：", size, "字节")
    dl = bytearray(data)
    size = sys.getsizeof(dl)
    print("数据的大小为：", size, "字节")
    print(dl)



# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # i=8
    # size = sys.getsizeof(i)
    # print("数据的大小为：", size, "字节")

    test_int_8()
    test_real_int_8()
    # print_hi('PyCharm')

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
