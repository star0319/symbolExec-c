# coding:utf8
from z3 import *

# 首先创建一个求解器
s = Solver()

'''
比如我们想求解这么一个问题
a ！=0
b=0


非  2（a+b）-4 ！=0
我们想看看符合要求的a，b的整数解有哪些？
'''

# 定义两个变量
a = Int('a')
b = Int('b')

# 在求解器中定义约束条件
s.add(a != 0)
s.add(b == 0)
s.add(  (2*(a+b)-4 )==0)

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
