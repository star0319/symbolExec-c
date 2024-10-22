# coding:utf8
from z3 import *

# 首先创建一个求解器
s = Solver()

'''
比如我们想求解这么一个问题
x + y = 5
x >= 2
y >= 2
我们想看看符合要求的x，y的整数解有哪些？
'''

# 定义两个变量
x = Int('x')
y = Int('y')

# 在求解器中定义约束条件
s.add(x >= 2)
s.add(y >= 2)
s.add(x + y == 5)

# 我们调用求解器的check()方法来判别约束集合是否能得到可行解，如果可行，给出结果
print(s.check())
if s.check():
    m = s.model()
    print(m)

'''
输出：
sat
[y = 2, x = 3]
'''
